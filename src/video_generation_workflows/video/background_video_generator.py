from __future__ import annotations

import pathlib
import time
from typing import Final

from google import genai
from google.genai import types

from .video_configuration import VideoConfiguration
from .video_generator import VideoGenerator


class BackgroundVideoGenerator(VideoGenerator):
    """
    Simple background video generator that mirrors the demo script logic:
    - Generate a base image from the scene prompt (Imagen)
    - Generate a single video using that image as both first and last frame (Veo)
    - Save outputs to disk and return the video file path
    """

    # Copied from demo for rev one; will be made configurable later
    PROJECT_ID: Final[str] = "personal-358900"
    LOCATION: Final[str] = "us-central1"
    IMAGEN_MODEL: Final[str] = "imagen-3.0-generate-002"
    VEO_MODEL: Final[str] = "veo-2.0-generate-001"
    OUTPUT_DIR: Final[pathlib.Path] = pathlib.Path(
        "demos/generate_video_from_start_end_images/videos"
    )

    DURATION_SECONDS: Final[int] = 8
    ASPECT_RATIO: Final[str] = "16:9"

    def _wait_for_operation(self, client: genai.Client, operation):
        while not operation.done:
            # Minimal logging for now; can be replaced with structured logging later
            print("Waiting for generation...")
            time.sleep(10)
            operation = client.operations.get(operation)
        return operation

    def generate(self, config: VideoConfiguration) -> str:
        # Ensure output directory exists
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        client = genai.Client(
            vertexai=True,
            project=self.PROJECT_ID,
            location=self.LOCATION,
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
        image_path = self.OUTPUT_DIR / "image_1.jpg"
        base_image.save(image_path)

        # 2) Generate a single video using the base image as first & last frame
        operation = client.models.generate_videos(
            model=self.VEO_MODEL,
            prompt=config.animate_scene_prompt,
            image=base_image,
            config=types.GenerateVideosConfig(
                number_of_videos=1,
                duration_seconds=self.DURATION_SECONDS,
                aspect_ratio=self.ASPECT_RATIO,
                last_frame=base_image,
            ),
        )

        operation = self._wait_for_operation(client, operation)

        # 3) Save the single generated video and return its path
        videos = getattr(operation, "response", getattr(operation, "result")).generated_videos
        if not videos:
            raise RuntimeError("Veo returned no videos.")

        output_path = self.OUTPUT_DIR / "video_1.mp4"
        videos[0].video.save(output_path)
        return str(output_path)

