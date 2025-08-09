# pip install google-genai
import argparse
import time
import pathlib
from google import genai
from google.genai import types, errors

# -- Configuration --
PROJECT_ID = "personal-358900"
LOCATION = "us-central1"
IMAGEN_MODEL = "imagen-3.0-generate-002"
VEO_MODEL = "veo-3.0-generate-preview"  # preview variant works with image input
OUTPUT_DIR = pathlib.Path("demos/generate_video_from_image/videos")
DURATION_SECONDS = 8
RESOLUTION = "1080p"  # or "720p"

def wait_for_op(client, op):
    while not op.done:
        print("Waiting for generation...")
        time.sleep(10)
        op = client.operations.get(op)
    return op

def main():
    parser = argparse.ArgumentParser(description="Imagen → Veo pipeline")
    parser.add_argument("--image-prompt", required=True)
    parser.add_argument("--video-prompt", required=True)
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(api_version="v1"),
    )

    # 1) Generate image
    print("Generating image with Imagen…")
    img_resp = client.models.generate_images(
        model=IMAGEN_MODEL,
        prompt=args.image_prompt,
        config=types.GenerateImagesConfig(number_of_images=1),
    )
    img = img_resp.generated_images[0].image
    image_path = OUTPUT_DIR / "image_1.jpg"
    img.save(image_path)
    print(f"Image saved: {image_path}")

    # 2) Generate videos
    print("Generating videos with Veo…")
    op = client.models.generate_videos(
        model=VEO_MODEL,
        prompt=args.video_prompt,
        image=img,
        config=types.GenerateVideosConfig(
            number_of_videos=args.count,
            duration_seconds=DURATION_SECONDS,
            resolution=RESOLUTION,
        ),
    )
    op = wait_for_op(client, op)

    # 3) Save videos
    vids = op.response.generated_videos
    for i, v in enumerate(vids, start=1):
        out = OUTPUT_DIR / f"video_{i}.mp4"
        v.video.save(out)
        print(f"Saved video {i}: {out}")

if __name__ == "__main__":
    main()
