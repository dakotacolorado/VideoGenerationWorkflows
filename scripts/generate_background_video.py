import os
from datetime import datetime
from pathlib import Path

from video_generation_workflows import (
    VideoConfiguration,
    ActionPrompt,
    BackgroundVideoGenerator,
)


# Allow configuration via environment variables; fall back to sensible defaults
PROJECT_ID = os.getenv("PROJECT_ID", "personal-358900")
LOCATION = os.getenv("LOCATION", "us-central1")
VIDEO_NAME = "background_video"
OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    str(Path("scripts/videos") / VIDEO_NAME / f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"),
)


config = VideoConfiguration(
    video_name=VIDEO_NAME,
    length=5,
    base_scene_prompt=(
        "A serene forest lake with a clear blue sky and gentle ripples on the water."
    ),
    animate_scene_prompt="Generate a slowly changing scene based on provided photo.  Keep the camera position and framing constant.",
    action_prompts=[
        ActionPrompt(
            prompt="A small boat drifts on the lake, a single rowboat.", start_index=1
        ),
        ActionPrompt(
            prompt="A small boat drifts on the lake, a single rowboat.", start_index=2
        ),
        ActionPrompt(
            prompt="A small boat drifts on the lake, a single rowboat.", start_index=4
        ),
    ],
)

generator = BackgroundVideoGenerator(
    project_id=PROJECT_ID,
    location=LOCATION,
    output_dir=OUTPUT_DIR,
)
output_path = generator.generate(config)
print(f"Generated video: {output_path}")
