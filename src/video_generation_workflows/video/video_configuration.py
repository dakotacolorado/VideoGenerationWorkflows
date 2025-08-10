from dataclasses import dataclass, field
from typing import List


@dataclass
class ActionPrompt:
    """
    Represents an action that occurs at a specific segment in a video sequence.

    Attributes
    ----------
    prompt : str
        Description of the action to perform in the scene.
    start_index : int
        Index (0-based) of the video segment where the action starts.
        Must be within the range [0, length - 1].
    """
    prompt: str
    start_index: int


@dataclass
class VideoConfiguration:
    """
    Configuration for generating a multi-segment video.

    Attributes
    ----------
    video_name : str
        Human-friendly name for the video. Not used by generators yet.
    length : int
        Total number of segments in the video (e.g., number of 8-second clips).
    base_scene_prompt : str
        Prompt describing the initial static scene.
    animate_scene_prompt : str, optional
        Prompt describing how to animate the base scene. Defaults to
        "Generate a live frame based on provided photo."
    action_prompts : List[ActionPrompt], optional
        List of time-indexed action prompts for specific segments.

    Raises
    ------
    ValueError
        If an action prompt's start index is out of bounds or duplicated.
    """
    video_name: str
    length: int
    base_scene_prompt: str
    animate_scene_prompt: str = "Generate a live frame based on provided photo."
    action_prompts: List[ActionPrompt] = field(default_factory=list)

    def __post_init__(self):
        for ap in self.action_prompts:
            if ap.start_index < 0 or ap.start_index >= self.length:
                raise ValueError(
                    f"Start index {ap.start_index} is out of bounds for video length {self.length}"
                )

        seen_indexes = {}
        for ap in self.action_prompts:
            if ap.start_index in seen_indexes:
                raise ValueError(
                    f"Action prompts {seen_indexes[ap.start_index]} and {ap} "
                    f"share the same start index {ap.start_index}"
                )
            seen_indexes[ap.start_index] = ap

