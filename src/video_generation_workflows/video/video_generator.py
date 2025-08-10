from __future__ import annotations

from abc import ABC, abstractmethod

from .video_configuration import VideoConfiguration


class VideoGenerator(ABC):
    """
    Interface for all video generators.

    Subclasses implement `generate` to produce a video based on
    a `VideoConfiguration` and return the output file path.
    """

    @abstractmethod
    def generate(self, config: VideoConfiguration) -> str:
        """
        Generate a video using the provided configuration.

        Parameters
        ----------
        config : VideoConfiguration
            The video generation configuration describing the scene
            and any actions to be applied.

        Returns
        -------
        str
            Absolute or relative file system path to the generated video.
        """
        raise NotImplementedError

