from video_generation_workflows import VideoConfiguration, ActionPrompt, BackgroundVideoGenerator

config = VideoConfiguration(
    length=3,
    base_scene_prompt="A serene forest lake with a clear blue sky and gentle ripples on the water.",
    animate_scene_prompt="Generate a live frame based on provided photo.",
    action_prompts=[
        ActionPrompt(prompt="A small boat drifts on the lake, a single rowboat.", start_index=0),
        ActionPrompt(prompt="A small boat drifts on the lake, a single rowboat.", start_index=1),
        ActionPrompt(prompt="A small boat drifts on the lake, a single rowboat.", start_index=2),
    ],
)

generator = BackgroundVideoGenerator()
output_path = generator.generate(config)
print(f"Generated video: {output_path}")
