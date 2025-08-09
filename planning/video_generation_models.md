## Long‑Form Text‑to‑Video Model Landscape (2025 Q3)

This document lists widely referenced video generation models with an emphasis on long‑form capability (≥60s), per‑clip limits, stitching/extend workflows, access status, and practical constraints. Details change frequently; verify latest terms and limits with each provider.

### Summary at a glance

| Model | Organization | Per‑clip length (typical) | Long‑form strategy | Access/API | Notable strengths | Common constraints |
|---|---|---:|---|---|---|---|
| Sora | OpenAI | up to ~60s | Multi‑shot prompts; extend/chain clips | Limited access; no broadly available API | High realism, complex scene understanding | Availability; usage policies |
| Veo (latest gen) | Google DeepMind | ~8–12s clips; higher tiers may vary | Clip extend/continuation; stitching | Vertex/partner access; gated | Quality, editing tools integration | Gated access; content policies |
| Gen‑3 (Alpha/Prod tiers) | Runway | ~5–10s per clip | Extend, shot‑by‑shot stitching, keyframe/control tracks | Web app + API (plan dependent) | Control (camera, masks, motion), speed to iterate | Cost; per‑clip limits; style drift |
| Dream Machine | Luma AI | ~5s per clip (extend available) | Extend + stitching | Web app; API limited/rolled out | Motion coherence, ease of use | Short clips; rate limits |
| Pika | Pika | ~3–8s per clip | Frame/clip continuation + stitching | Web app; API limited/beta | Camera/motion controls, quick iteration | Short clips; style consistency |
| Kling (latest) | Kuaishou | Demos show 1+ min; user tiers vary | Direct long clips or chained segments | Region‑gated; no broad API | Realistic motion/physics in demos | Access limits; policy/region constraints |
| Hunyuan Video | Tencent | Short‑to‑medium clips | Stitching/extend | Limited/publicity demos | Human/scene realism | Enterprise/gated access |
| VeoFX/VideoFX/Flow tools | Google | Tooling for sequencing | Tool‑assisted chaining | Platform tools | Workflow integration | Access; credits |
| Stable Video Diffusion | Stability AI | ~2–4s (open source) | Local stitching; control‑nets | Open source checkpoints | Self‑hosted, controllable | Quality vs SOTA; engineering effort |
| Open‑Sora / research stacks | Community | Varies (research) | Experimental chaining | Research code | Inspectable, adaptable | Fragile; compute heavy |

Notes:
- Per‑clip lengths are practical ranges observed across tiers; providers may offer “extend/continue” to build longer sequences. True single‑pass long‑form (minutes) is rare outside gated programs; most workflows chain clips.
- Long‑form success depends as much on workflow (shot planning, seeds, reference frames, temporal constraints) as the base model.

### Practical guidance for this project (v0 → v1)

- **v0 goal (single shot)**: Generate one clip given (prompt, duration, filename). Target 5–10s to ensure reliability; longer if your chosen provider supports extend.
- **v0.5 (pseudo long‑form)**: Add “extend/continue” or “next shot” to chain multiple clips; stitch with `ffmpeg`, add crossfades, maintain seeds/refs for consistency.
- **v1 (shot list)**: Accept a shot list (prompt per shot, duration per shot), enforce camera/style constraints, and stitch. Add reference images to stabilize identity/style.

### Model selection considerations

- **Access and terms**: Many leading models are gated or region‑restricted. Confirm API availability, quotas, pricing, and allowed use cases.
- **Clip length vs. quality**: Longer single clips often reduce fidelity/consistency. Shorter clips with careful stitching can look better.
- **Temporal control**: Prefer providers exposing camera paths, keyframes, masks, or control tracks for scene continuity.
- **Identity/style locking**: Look for reference image/video conditioning and seed control to reduce drift across shots.
- **Throughput/cost**: Long‑form requires many generations/iterations; model speed and unit pricing matter for iteration.

### Short list by use case

- **Highest photorealism (gated)**: OpenAI Sora, Google Veo (latest). Use if you have access; plan for policy reviews and quotas.
- **Builder‑friendly with API**: Runway Gen‑3 (plan dependent), Pika (beta), Luma (API rollout). Good for rapid iteration and programmatic control.
- **Self‑hosted / research**: Stable Video Diffusion, Open‑Sora variants. Expect engineering to reach acceptable quality and to implement your own long‑form stitching.

### Reality check for long‑form (≥60s)

- Today’s practical path is **shot‑based generation + stitching**, not single‑pass minutes‑long output, unless you have access to gated long‑form tiers.
- Plan for: shot planning, consistent style/identity assets, transition design, and post‑processing (denoise, interpolation, upscaling, color).

### What to verify next (before implementation)

- Chosen provider’s current: per‑clip limit, extend availability, API endpoints, rate limits, pricing, and content policy.
- Availability of controls you need: seeds, reference images/video, masks, camera paths, negative prompts.
