

@dataclass 
class ActionPrompt:
    """
    A prompt for an action in the scene.
    """
    prompt: str
    start_loop: int



class PromptTemplate(ABC):

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
