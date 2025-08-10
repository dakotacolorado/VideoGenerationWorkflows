from __future__ import annotations

import logging
import pathlib
import shutil
from typing import Any, List, Union

from moviepy import VideoFileClip, concatenate_videoclips

logger = logging.getLogger(__name__)


class VideoSegmentManager:
    """
    Manages a collection of MoviePy `VideoFileClip` segments and writes
    a single combined video to disk.

    Configure with a `video_name` and a `save_dir` path. Use `add_segment`
    to append segments, and call `save` to concatenate and write the final file.

    On each `add_segment` call, a copy of the segment file is stored in
    `save_dir` as `segment_XX.mp4` (1-based index) for resilience if the
    process stops mid-run.
    """

    def __init__(
        self,
        video_name: str,
        output_dir: Union[str, pathlib.Path] | None = None,
        *,
        save_dir: Union[str, pathlib.Path] | None = None,
    ) -> None:
        """
        Create a segment manager.

        Parameters
        ----------
        video_name : str
            Name used for the final combined video filename.
        output_dir : Path-like, optional
            Directory where intermediate segments and the final video are stored.
        save_dir : Path-like, optional
            Deprecated alias for `output_dir` (kept for backward compatibility).
        """
        self.video_name: str = video_name
        resolved_dir = output_dir if output_dir is not None else save_dir
        if resolved_dir is None:
            raise ValueError("output_dir must be provided")
        self.output_dir: pathlib.Path = pathlib.Path(resolved_dir)
        self._segments: List[VideoFileClip] = []
        self._segment_paths: List[pathlib.Path] = []
        self._next_index: int = 1
        logger.info(
            f"Initialized VideoSegmentManager for '{video_name}' in directory: {self.output_dir}"
        )

    def add_segment(self, clip_or_api_video: Union[VideoFileClip, Any]) -> None:
        """Append a segment to the internal list and persist a copy to disk.

        Parameters
        ----------
        clip_or_api_video : VideoFileClip | google.genai.types.Video
            Either a MoviePy clip or a Google GenAI API video object (with `.save`).
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        index = self._next_index
        self._next_index += 1
        dest_path = self.output_dir / f"segment_{index:02d}.mp4"

        # Case 1: Google API video-like object with `.save`
        if hasattr(clip_or_api_video, "save") and not isinstance(clip_or_api_video, VideoFileClip):
            clip_or_api_video.save(dest_path)
            logger.info(f"Saved API segment {index:02d} to '{dest_path}'")
            clip = VideoFileClip(str(dest_path))
            self._segments.append(clip)
            self._segment_paths.append(dest_path)
            logger.info(
                f"Added segment {index:02d} (duration: {getattr(clip, 'duration', 0.0):.2f}s) to '{self.video_name}'"
            )
            return

        # Case 2: MoviePy clip – copy from source if possible, else encode
        clip = clip_or_api_video  # expected VideoFileClip
        src_path = getattr(clip, "filename", None)
        try:
            if src_path:
                src_path = pathlib.Path(src_path)
        except TypeError:
            src_path = None

        if src_path and src_path.exists():
            # Avoid copying a file onto itself
            try:
                if src_path.resolve() != dest_path.resolve():
                    shutil.copyfile(src_path, dest_path)
                    logger.info(f"Copied segment {index:02d} from '{src_path}' to '{dest_path}'")
                else:
                    logger.info(
                        f"Segment {index:02d} already at destination '{dest_path}', skipping copy"
                    )
            except Exception as e:
                logger.warning(
                    f"Failed to copy segment from '{src_path}' to '{dest_path}', will encode instead: {e}"
                )
                self._save(clip, dest_path)
        else:
            # Fallback to encoding if source path is unknown
            self._save(clip, dest_path)
            logger.info(f"Wrote segment {index:02d} to '{dest_path}' via encoding")

        self._segments.append(clip)
        self._segment_paths.append(dest_path)
        logger.info(
            f"Added segment {index:02d} (duration: {getattr(clip, 'duration', 0.0):.2f}s) to '{self.video_name}'"
        )

    def save(self) -> str:
        """Concatenate all segments and write the final video file.

        Returns
        -------
        str
            Path to the written video file.
        """
        if not self._segments:
            raise RuntimeError("No segments have been added.")

        logger.info(f"Saving video '{self.video_name}' with {len(self._segments)} segment(s)")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{self.video_name}.mp4"

        logger.info(f"Output path: {output_path}")

        try:
            logger.info("Writing final video file")
            self._save(self._segments, output_path)
        finally:
            # Close all segment clips
            logger.info("Closing all segment clips")
            for i, clip in enumerate(self._segments, 1):
                try:
                    clip.close()
                    logger.info(f"Closed segment {i}")
                except Exception as e:
                    logger.warning(f"Failed to close segment {i}: {e}")

        logger.info(f"Successfully saved video: {output_path}")
        return str(output_path)

    def _save(self, target: Union[VideoFileClip, List[VideoFileClip]], dest_path: pathlib.Path) -> None:
        """Internal helper to persist either a single clip or a list of clips.

        - If `target` is a single clip: write it directly to `dest_path`.
        - If `target` is a list of clips: concatenate and write to `dest_path`.
        """
        if isinstance(target, list):
            logger.info(f"Concatenating {len(target)} segments")
            final = concatenate_videoclips(target, method="compose")
            try:
                logger.info("Writing concatenated video to output file")
                final.write_videofile(str(dest_path), codec="libx264", audio=False)
            finally:
                try:
                    final.close()
                    logger.info("Closed concatenated video clip")
                except Exception as e:
                    logger.warning(f"Failed to close concatenated clip: {e}")
        else:
            logger.info("Writing single clip to output file")
            target.write_videofile(str(dest_path), codec="libx264", audio=False)

