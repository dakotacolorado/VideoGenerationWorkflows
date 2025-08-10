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
VIDEO_NAME = "rainy_valley_video"
OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    str(Path("scripts/videos") / VIDEO_NAME / f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"),
)


config = VideoConfiguration(
    video_name=VIDEO_NAME,
    length=2,
    base_scene_prompt=(
        "A high-tech yet rustic forest cabin interior perched on a mountainside, featuring a floor-to-ceiling panoramic glass wall overlooking a misty, rain-soaked valley of pine trees. Warm amber light from floor lamps and a modern glass-fronted fireplace contrasts beautifully with the cool blue-grey daylight filtering through overcast skies. A sleek wooden desk with multiple glowing monitors, showing detailed market charts, suggests the workspace of a tech founder or crypto trader. Along one wall, a lush vertical garden adds greenery, while a large fluffy dog rests motionless on a rug beside the fire. The scene is softly illuminated by the muted afternoon light, diffused by rain outside. Semi-realistic, cinematic composition with high detail, rich textures, modern Nordic architecture blended with subtle futuristic design elements."
    ),
    animate_scene_prompt=(
        "Use the provided image as the first frame. Lock the camera position, orientation, and lens parameters for the entire sequence — absolutely no panning, tilting, zooming, reframing, rotation, scaling, warping, parallax, or perspective changes. Keep the composition, scale, and framing pixel-for-pixel identical from start to finish. All background layers, textures, and objects must remain completely static with zero micro-movement or re-render flicker. Preserve all original objects, colors, lighting, and shadows with no changes, except for the fireplace flames, which should flicker subtly. No new elements may appear or disappear. The final frame must be exactly identical at the pixel level to the first frame, ensuring a perfect seamless loop with no jitter, scene drift, or background shift."
    ),
    action_prompts=[
        # ActionPrompt(
        #     prompt="On the left-most monitor, a minimal market movement update the chart, then fade out. No sound.",
        #     start_index=1
        # ),
        # ActionPrompt(
        #     prompt="Dog by the fireplace gives a tiny ear twitch and slow blink; head remains down. Movement under 1s, very subtle.",
        #     start_index=2
        # ),
        # ActionPrompt(
        #     prompt="Small ember pop inside the fireplace: a brief spark and glow lift, then settle. Keep flame pattern consistent.",
        #     start_index=3
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
