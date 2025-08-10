# pip install google-genai moviepy pillow
import argparse
import time
import pathlib
from typing import List

from google import genai
from google.genai import types, errors

from PIL import Image
from moviepy import VideoFileClip, ImageClip, concatenate_videoclips

# -- Configuration --
PROJECT_ID = "personal-358900"
LOCATION = "us-central1"
IMAGEN_MODEL = "imagen-3.0-generate-002"
VEO_MODEL = "veo-3.0-generate-preview"
OUTPUT_DIR = pathlib.Path("demos/generate_video_from_last_frame_chain/videos")
DURATION_SECONDS = 8
RESOLUTION = "1080p"

def wait_for_op(client: genai.Client, op):
    while not op.done:
        print("Waiting for generation...")
        time.sleep(10)
        op = client.operations.get(op)
    return op

def extract_last_frame_as_types_image(video_path: pathlib.Path, out_jpg_path: pathlib.Path) -> types.Image:
    # Grab the last frame just before the end
    with VideoFileClip(str(video_path)) as clip:
        frame = clip.get_frame(max(0, clip.duration - 1e-3))
    img = Image.fromarray(frame).convert("RGB")
    out_jpg_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_jpg_path, format="JPEG", quality=95)
    # Build a types.Image from raw bytes
    return types.Image(image_bytes=out_jpg_path.read_bytes(), mime_type="image/jpeg")

def save_generated_videos(op, prefix: str) -> List[pathlib.Path]:
    vids = op.response.generated_videos
    paths: List[pathlib.Path] = []
    for i, v in enumerate(vids, start=1):
        out = OUTPUT_DIR / f"{prefix}_{i:02d}.mp4"
        v.video.save(out)
        print(f"Saved video: {out}")
        paths.append(out)
    return paths

def concatenate_videos(paths: List[pathlib.Path], out_path: pathlib.Path) -> None:
    clips = [VideoFileClip(str(p)) for p in paths]
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(str(out_path), codec="libx264", audio=False)
    for c in clips:
        c.close()
    final.close()

def main():
    parser = argparse.ArgumentParser(description="Imagen → chained Veo videos")
    parser.add_argument("--scene-prompt", required=True)
    parser.add_argument("--video-prompt", action="append", required=True)
    parser.add_argument("--duration", type=int, default=DURATION_SECONDS)
    parser.add_argument("--resolution", default=RESOLUTION, choices=["720p", "1080p"])
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(api_version="v1"),
    )

    # 1) Generate initial image
    print("Generating start image with Imagen…")
    img_resp = client.models.generate_images(
        model=IMAGEN_MODEL,
        prompt=args.scene_prompt,
        config=types.GenerateImagesConfig(number_of_images=1),
    )
    if not img_resp.generated_images:
        raise RuntimeError("Imagen did not return an image.")
    start_img = img_resp.generated_images[0].image
    first_image_path = OUTPUT_DIR / "start_image.jpg"
    start_img.save(first_image_path)
    print(f"Start image saved: {first_image_path}")

    # 2) First video
    segment_paths: List[pathlib.Path] = []
    print("Generating video 1 with Veo…")
    op = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=args.video_prompt[0],
        image=start_img,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            duration_seconds=args.duration,
            resolution=args.resolution,
        ),
    )
    op = wait_for_op(client, op)
    first_segment = save_generated_videos(op, "segment_01")
    segment_paths.extend(first_segment)

    # Prep starter frame for next segment
    starter_img_path = OUTPUT_DIR / "segment_0101.jpg"
    prev_last_frame_image = extract_last_frame_as_types_image(first_segment[-1], starter_img_path)
    print(f"Saved next starter frame: {starter_img_path}")

    # 3) Remaining videos
    for idx, prompt in enumerate(args.video_prompt[1:], start=2):
        print(f"Generating video {idx} with Veo…")
        op = client.models.generate_videos(
            model=VEO_MODEL,
            prompt=prompt,
            image=prev_last_frame_image,
            config=types.GenerateVideosConfig(
                number_of_videos=1,
                duration_seconds=args.duration,
                resolution=args.resolution,
            ),
        )
        op = wait_for_op(client, op)
        seg = save_generated_videos(op, f"segment_{idx:02d}")
        segment_paths.extend(seg)

        starter_img_path = OUTPUT_DIR / f"segment_{idx:02d}01.jpg"
        prev_last_frame_image = extract_last_frame_as_types_image(seg[-1], starter_img_path)
        print(f"Saved next starter frame: {starter_img_path}")

    # 4) Concatenate all
    final_path = OUTPUT_DIR / "combined.mp4"
    print("Concatenating all segments…")
    concatenate_videos(segment_paths, final_path)
    print(f"Final combined video saved: {final_path}")

if __name__ == "__main__":
    main()
