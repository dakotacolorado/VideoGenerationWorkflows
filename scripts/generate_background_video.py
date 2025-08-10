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
    length=4,
    base_scene_prompt=(
        "An otherworldly alien landscape under a star-filled sky: colossal jagged mountains rise from glowing misty valleys,"
        " with bioluminescent flora scattered across the terrain and distant nebulae visible beyond. Cinematic, high detail, ethereal atmosphere."
    ),
    animate_scene_prompt=(
        "Create a seamless short loop from the provided image. The camera and composition must be absolutely locked — no panning, tilting, zooming, reframing, stabilization, or parallax. Treat the image as a frozen plate: do not translate, scale, rotate, crop, or re-project any pixels. Keep background, lighting, perspective, and framing identical across all frames. Only allow very subtle, localized, cyclical in-place motion that returns exactly to the starting state. If any global drift would occur, reduce motion to zero. Ensure the last frame is pixel-identical to the first."
    ),
    action_prompts=[
        ActionPrompt(
            prompt="A faint meteor slowly streaks across the sky and fades.", start_index=1
        ),
        # ActionPrompt(
        #     prompt="A small boat drifts on the lake, a single rowboat.", start_index=2
        # ),
        # ActionPrompt(
        #     prompt="A small boat drifts on the lake, a single rowboat.", start_index=4
        # ),
    ],
)

generator = BackgroundVideoGenerator(
    project_id=PROJECT_ID,
    location=LOCATION,
    output_dir=OUTPUT_DIR,
)
output_path = generator.generate(config)
print(f"Generated video: {output_path}")
