from prompts.prompt_template import PromptTemplate, ActionPrompt


class CoffeeShopPrompt(PromptTemplate):

    def get_base_scene_prompt(self) -> str:
        return """
        A high-tech yet rustic forest cabin interior, perched on a mountainside, with a floor-to-ceiling panoramic glass wall revealing a misty, rain-soaked valley of pine trees. Warm amber lighting from floor lamps and a modern glass-fronted fireplace contrasts with the cool blue-grey daylight outside. A sleek wooden desk with multiple glowing monitors faces the window. A vertical plant wall adds lush greenery, and a large fluffy dog lies still on a rug beside the fire. The style is semi-realistic, cinematic composition, high detail, rich textures, with a balance of modern Nordic architecture and subtle futuristic elements.
        """

    def get_action_prompts(self) -> list[ActionPrompt]:
        return [
            ActionPrompt(
                prompt="On the left-most monitor, a minimal crypto ticker card fades in, numbers tick upward for 2s, then fade out. No sound.",
                start_loop=1
            ),
            ActionPrompt(
                prompt="Dog by the fireplace gives a tiny ear twitch and slow blink; head remains down. Movement under 1s, very subtle.",
                start_loop=5
            ),
            ActionPrompt(
                prompt="Small ember pop inside the fireplace: a brief spark and glow lift, then settle. Keep flame pattern consistent.",
                start_loop=10
            )