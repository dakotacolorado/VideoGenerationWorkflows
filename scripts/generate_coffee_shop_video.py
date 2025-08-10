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
VIDEO_NAME = "coffee_shop_video"
OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    str(Path("scripts/videos") / VIDEO_NAME / f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"),
)


config = VideoConfiguration(
    video_name=VIDEO_NAME,
    length=2,
    base_scene_prompt=(
        "Modern Nordic-style coffee shop on a quiet Sunday afternoon (about 2 pm). "
        "Semi-realistic, cinematic composition. Bright, warm daylight from two glass walls "
        "with matte black frames; pendant lamps add a soft amber glow. Natural wood panels, "
        "light oak tables with rounded corners, Nordic chairs with muted green/grey cushions. "
        "Abundant plants (some trailing from wall shelves, some in woven/ceramic pots on the floor). "
        "A full-wall modern bookshelf holds books, board games, small clay décor, and tiny plants. "
        "White stone counter with pale oak accents, espresso machine, and pastries. "
        "A few abstract steel-texture art pieces on the wall. Ceramic mugs, laptops, notebooks, pens on tables. "
        "A single bicycle is parked outside and visible through the window. "
        "Early autumn, bright overcast skies with occasional soft sun. Only 2–3 patrons seated quietly; "
        "in the far corner away from the camera, a young adult sits alone with head bowed over an open book, "
        "absorbed in reading, elbows resting on the table, a ceramic mug beside them. "
        "No motion implied. Color palette: forest green, warm oak brown, matte cream, soft grey, muted teal, terracotta accents."
    ),
    animate_scene_prompt=(
        "Animate the provided still image into a live photo with the camera completely locked—"
        "no pan, tilt, zoom, reframing, rotation, or perspective change. Preserve the exact composition, scale, "
        "lighting, colors, and shadows. the starting frame and the end frame must be exactly the same with no frame shiting. Add only subtle, repeating environmental motion suitable for a café: "
        "gentle steam rising from a cup, extremely slight plant sway, very soft ambient light change from passing clouds. "
        "Do not move people or objects unless specified by overlay actions. No new objects or UI elements. "
        "The final frame must match the first frame exactly for a perfect loop; avoid any jitter, drift, or exposure creep."
    ),
    action_prompts=[
        # ActionPrompt(
        #     prompt="A seated person flips one page of a book with a slow, quiet motion (3-4s).",
        #     start_index=1
        # ),
        # ActionPrompt(
        #     prompt="A seated customer lifts a mug for a small sip and sets it down gently (2s).",
        #     start_index=2
        # ),
        # ActionPrompt(
        #     prompt="A car drive pass the street slowly, visible through the window (2s).",
        #     start_index=3
        # ),
        # ActionPrompt(
        #     prompt="Leaves of a hanging plant sway slightly as a soft indoor draft passes (2s).",
        #     start_index=4
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
