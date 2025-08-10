

@dataclass 
class ActionPrompt:
    """
    A prompt for an action in the scene.
    """
    prompt: str
    start_index: int



class PromptTemplate(ABC):

    def __init__(self):
        for action_prompt in self.get_action_prompts():
            if action_prompt.start_index < 0 or action_prompt.start_index >= self.get_length():
                raise ValueError(f"Start index {action_prompt.start_index} is out of bounds for template of length {self.get_length()}")
                
        for action_prompt in self.get_action_prompts():
            for other_action_prompt in self.get_action_prompts():
                if action_prompt.start_index == other_action_prompt.start_index and action_prompt != other_action_prompt:
                    raise ValueError(f"Action prompts {action_prompt} and {other_action_prompt} share the same start index {action_prompt.start_index}")
                
        


    @property
    @abstractmethod
    def get_length(self) -> int:
        """
        Get the length of the template.  This is the number of 8s videos in the video.
        """
        return 3

    @property
    @abstractmethod
    def get_base_scene_prompt(self) -> str:
        """
        Get the base scene prompt for the template.
        """
        pass
    
    @property
    @abstractmethod
    def animate_scene_prompt(self) -> str:
        """
        Animate the scene prompt for the template.
        """
        return "Generate a live frame based on provided photo."


    @property
    @abstractmethod
    def get_action_prompts(self) -> list[ActionPrompt]:
        """
        Get the action prompts for the template.
        """
        return []
