# pip install google-genai
import argparse
import time
import pathlib
from google import genai
from google.genai import types

# ---- STATIC CONFIG ----
PROJECT_ID = "personal-358900"
LOCATION = "us-central1"
MODEL_NAME = "veo-3.0-generate-001"  # or "veo-3.0-fast-generate-001"
DURATION_SECONDS = 8
OUTPUT_DIR = pathlib.Path("demos/veo/videos")
STORAGE_URI = None  # e.g., "gs://your-bucket/veo-output/"
RESOLUTION = "1080p"  # or "720p"
# -----------------------

def main():
    parser = argparse.ArgumentParser(description="Generate videos with Veo 3 on Vertex AI")
    parser.add_argument("--prompt", required=True, help="Text prompt for video generation")
    parser.add_argument("--count", type=int, default=1, help="Number of videos to generate")
    args = parser.parse_args()

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
        http_options=types.HttpOptions(api_version="v1"),  # GA endpoint
    )

    config = types.GenerateVideosConfig(
        number_of_videos=args.count,
        duration_seconds=DURATION_SECONDS,
        resolution=RESOLUTION,
        **({"storage_uri": STORAGE_URI} if STORAGE_URI else {}),
    )

    op = client.models.generate_videos(
        model=MODEL_NAME,
        prompt=args.prompt,
        config=config,
    )

    print(f"Started operation: {op.name}")
    while not op.done:
        print("Waiting for video generation...")
        time.sleep(10)
        op = client.operations.get(op)

    if STORAGE_URI:
        for idx, v in enumerate(op.response.generated_videos, start=1):
            print(f"Video {idx} saved to:", v.gcs_uri)
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    for idx, v in enumerate(op.result.generated_videos, start=1):
        (OUTPUT_DIR).mkdir(exist_ok=True)
        (OUTPUT_DIR / f"video_{idx}.mp4").parent.mkdir(exist_ok=True)
        v.video.save(OUTPUT_DIR / f"video_{idx}.mp4")  

if __name__ == "__main__":
    main()
