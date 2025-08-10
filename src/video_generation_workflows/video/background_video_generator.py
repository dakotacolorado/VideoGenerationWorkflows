from __future__ import annotations

import pathlib
import time
from typing import Final, Union

from google import genai
from google.genai import types

from .video_configuration import VideoConfiguration
from .video_generator import VideoGenerator
from .video_segment_manager import VideoSegmentManager
from moviepy import VideoFileClip


class BackgroundVideoGenerator(VideoGenerator):
    """
    Background video generator that produces a set of loopable segments and
    appends them to a `VideoSegmentManager`.

    Flow:
    - Generate a base image from the base scene prompt (Imagen)
    - For each segment index in the configured length:
      - Build a prompt that keeps the base loop and optionally applies any
        action(s) whose `start_index` matches the segment index
      - Generate a video constrained to a seamless, static loop (Veo)
      - Append the resulting segment to the manager
    - Concatenate and save the final video, return the written path
    """

    IMAGEN_MODEL: Final[str] = "imagen-3.0-generate-002"
    VEO_MODEL: Final[str] = "veo-3.0-generate-preview"
    ASPECT_RATIO: Final[str] = "16:9"

    # Strong, reusable constraints to create static, loopable clips without an explicit end frame
    STATIC_LOOP_PREAMBLE: Final[str] = (
        "Create an 8-second seamless looping video from the provided reference image.\n"
        "- Lock the camera and composition: absolutely no panning, tilting, dolly, zoom, rotation, or reframing.\n"
        "- Keep the background, horizon, perspective, and parallax completely fixed.\n"
        "- Do not change lighting, weather, white balance, exposure, focus, lens, or depth of field.\n"
        "- Do not add, remove, or reposition background objects.\n"
        "- Treat the input image as a frozen plate: do not translate, scale, rotate, crop, stabilize, or reframe any pixels across frames.\n"
        "- All static regions must remain pixel-aligned and identical in every frame (no drift or breathing).\n"
        "- Only permit extremely subtle, localized, cyclical in-place micro-motions that return to their initial state by the end.\n"
        "- If any global drift would occur, reduce motion to zero to preserve a perfect loop.\n"
        "- Ensure the LAST frame is pixel-identical to the FIRST frame for a perfect start-to-end loop."
    )

    def __init__(
        self,
        project_id: str,
        location: str,
        output_dir: Union[str, pathlib.Path],
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.output_dir = pathlib.Path(output_dir)

    def _wait_for_operation(self, client: genai.Client, operation):
        while not operation.done:
            print("Waiting for generation...")
            time.sleep(10)
            operation = client.operations.get(operation)
        return operation

    def generate(self, config: VideoConfiguration) -> str:
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        client = genai.Client(
            vertexai=True,
            project=self.project_id,
            location=self.location,
            http_options=types.HttpOptions(api_version="v1"),
        )

        # 1) Generate base image from the base scene prompt
        image_response = client.models.generate_images(
            model=self.IMAGEN_MODEL,
            prompt=config.base_scene_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1, output_mime_type="image/jpeg"
            ),
        )
        if not image_response.generated_images:
            raise RuntimeError("Imagen returned no images.")

        base_image = image_response.generated_images[0].image
        image_path = self.output_dir / "image_1.jpg"
        base_image.save(image_path)

        # 2) Generate N segments, allowing actions to add unique features per segment
        manager = VideoSegmentManager(video_name=config.video_name, output_dir=self.output_dir)

        # Pre-index actions by their start index for quick lookup
        index_to_actions = {}
        for ap in config.action_prompts:
            index_to_actions.setdefault(ap.start_index, []).append(ap.prompt)

        # If any segments have no actions, pre-generate a single base segment to reuse
        animate_instructions_global = (config.animate_scene_prompt or "").strip()
        base_segment_path = self.output_dir / "segment_base.mp4"
        if any(i not in index_to_actions for i in range(config.length)):
            base_segment_prompt = (
                f"{self.STATIC_LOOP_PREAMBLE}\n\n"
                f"Scene description: {config.base_scene_prompt.strip()}\n"
                f"Animation guidance: {animate_instructions_global}\n"
                f"Segment 1 of {config.length}."
            )

            base_operation = client.models.generate_videos(
                model=self.VEO_MODEL,
                prompt=base_segment_prompt,
                image=base_image,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    duration_seconds=8,
                    aspect_ratio=self.ASPECT_RATIO,
                ),
            )
            base_operation = self._wait_for_operation(client, base_operation)
            base_videos = getattr(base_operation, "response", getattr(base_operation, "result")).generated_videos
            if not base_videos:
                raise RuntimeError("Veo returned no videos for base segment.")
            base_videos[0].video.save(base_segment_path)

        for segment_index in range(config.length):
            # Build the per-segment prompt: preamble -> scene -> animation guidance -> segment index -> actions
            animate_instructions = (config.animate_scene_prompt or "").strip()

            actions_for_segment = index_to_actions.get(segment_index, [])

            # Reuse the pre-generated base segment if there are no actions for this segment
            if not actions_for_segment and base_segment_path.exists():
                manager.add_segment(VideoFileClip(str(base_segment_path)))
                continue
            actions_text = "".join(
                [
                    f"\n- Apply this subtle, localized action without moving the camera or background: {action_text}."
                    for action_text in actions_for_segment
                ]
            )

            segment_prompt = (
                f"{self.STATIC_LOOP_PREAMBLE}\n\n"
                f"Scene description: {config.base_scene_prompt.strip()}\n"
                f"Animation guidance: {animate_instructions}\n"
                f"Segment {segment_index + 1} of {config.length}."
                f"{actions_text}"
            )

            operation = client.models.generate_videos(
                model=self.VEO_MODEL,
                prompt=segment_prompt,
                image=base_image,
                config=types.GenerateVideosConfig(
                    number_of_videos=1,
                    # Respect API limit; not user-configurable here
                    duration_seconds=8,  # VEO model supports this duration
                    aspect_ratio=self.ASPECT_RATIO,
                    # last_frame=base_image,
                ),
            )

            operation = self._wait_for_operation(client, operation)

            videos = getattr(operation, "response", getattr(operation, "result")).generated_videos
            if not videos:
                raise RuntimeError("Veo returned no videos.")

            # Append this segment to the manager
            manager.add_segment(videos[0].video)

        # 3) Save the combined segments and return final path
        final_path = manager.save()
        return final_path

