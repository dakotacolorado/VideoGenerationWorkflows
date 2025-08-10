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
VIDEO_NAME = "italian_piazza_video"
OUTPUT_DIR = os.getenv(
    "OUTPUT_DIR",
    str(Path("scripts/videos") / VIDEO_NAME / f"{datetime.now().strftime('%Y-%m-%d-%H-%M')}"),
)


config = VideoConfiguration(
    video_name=VIDEO_NAME,
    length=60,  # 1-minute loop as specified
    base_scene_prompt=(
        "A sun-kissed piazza in a quaint Italian hill town, inspired by Eat Pray Love. "
        "The focal character — a young woman from New York City — is sitting on a weathered wooden bench "
        "at the edge of the square, gazing toward the center. She's surrounded by the slow rhythm of everyday Italian life. "
        "Semi-realistic cinematic style with warm, romantic color grading. Soft focus on the foreground, "
        "with distant movement slightly blurred for depth. Late afternoon around 4:30 pm, early spring, pleasantly mild. "
        "Pebblestone streets in soft beige and terracotta tones. Stone fountain as centerpiece with elegant cherub figure "
        "pouring water from an urn; sunlight glints on the ripples. Outdoor café seating with wrought iron chairs "
        "and small marble-topped tables, linen napkins fluttering in the breeze. Purple wisteria climbing up weathered "
        "stucco walls, next to shuttered windows with peeling turquoise paint. Bicycles leaning against buildings, "
        "baskets filled with groceries — bread, fresh herbs, and lemons. Warm-toned plaster façades in ochre and salmon, "
        "with rust-streaked drainpipes and faded painted shop signs. Small gelato cart with pastel-colored ice cream tubs, "
        "shaded by a striped canopy. Locals in casual spring clothes carrying grocery bags, tourists holding cameras "
        "or sipping Aperol spritz. Golden sunlight bathes the square, casting long shadows across cobblestones. "
        "Colors: warm ochre and terracotta, muted teal shutters, soft lavender from wisteria, creamy whites of café linens, "
        "and deep ruby red of wine glasses catching the light. Static wide shot from bench area, framing fountain slightly "
        "off-center, with very subtle handheld sway to mimic a person observing while seated."
    ),
    animate_scene_prompt=(
        "Use the provided image as the first frame. Lock the camera position, orientation, and lens parameters for the entire sequence — "
        "absolutely no panning, tilting, zooming, reframing, rotation, scaling, warping, parallax, or perspective changes. "
        "Keep the composition, scale, and framing pixel-for-pixel identical from start to finish. All background layers, "
        "textures, and objects must remain completely static with zero micro-movement or re-render flicker. Preserve all "
        "original objects, colors, lighting, and shadows with no changes. No new elements may appear or disappear. "
        "The final frame must be exactly identical at the pixel level to the first frame, ensuring a perfect seamless loop "
        "with no jitter, scene drift, or background shift. Add only the specified action events at their designated timestamps "
        "while maintaining the overall scene stability and cinematic quality."
    ),
    action_prompts=[
        ActionPrompt(
            prompt="Two locals walk past the fountain, laughing softly in Italian. Leisurely pace, small gestures as they talk. "
                   "Footsteps softly crunch on cobblestones. Movement should be natural and relaxed, fitting the peaceful atmosphere.",
            start_index=4
        ),
        ActionPrompt(
            prompt="A tourist steps forward, raises their phone, and takes a photo of the fountain. Slow, deliberate movement. "
                   "Camera shutter sound blends into ambient background. The movement should be respectful and unobtrusive.",
            start_index=12
        ),
        ActionPrompt(
            prompt="A waiter in a crisp white shirt delivers a glass of wine to a woman at the café table. "
                   "Smooth, steady movement, wine catching a sparkle of sunlight. Professional, graceful service motion.",
            start_index=22
        ),
        ActionPrompt(
            prompt="A cyclist pedals slowly past the bench, basket filled with fresh bread and a bunch of basil. "
                   "Graceful, relaxed roll; faint rattle of bicycle chain. The movement should be smooth and unhurried.",
            start_index=34
        ),
        ActionPrompt(
            prompt="Breeze stirs the wisteria blooms; a few petals drift down and land on the cobblestones. "
                   "Gentle, slow-motion feel. The petals should fall naturally and settle softly on the ground.",
            start_index=48
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
