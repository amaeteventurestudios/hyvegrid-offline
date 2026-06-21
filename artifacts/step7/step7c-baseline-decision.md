# Step 7C Baseline Decision

Date: 2026-06-21
Project: HyveGrid Offline ADTC 2026

Decision: keep Granite 3.3 2B Instruct Q4_K_M as the practical baseline lock candidate.

This is not a high-accuracy claim. It is the best practical scoring-path candidate currently tested after rejecting Gemma 3 4B, Qwen3-1.7B, and Granite 8B.

## Side-by-side result

| Model | Prompt 1 quality | Prompt 2 quality | Speed signal | Decision |
|---|---|---|---:|---|
| Granite 3.3 2B Q4_K_M | Weak, but mentioned abnormal brood and avoid disturbance | Better crop/site answer than Gemma; mentioned pesticides, crops, water, forage, habitat disruption | 4.0 / 3.5 t/s generation | Keep as practical baseline |
| Gemma 2 2B IT Q4_K_M | More direct on ants, but too short | Generic; missed crop-specific pesticide and placement detail | 3.5 / 3.5 t/s generation | Do not switch |

## Why Granite remains the baseline

- Smaller local footprint than larger rejected candidates.
- Known profiler smoke result was better than Gemma baseline.
- Site-readiness answer was more useful than Gemma on the official prompt.
- Gemma did not show enough answer-quality improvement to justify switching.

## Guardrail

Do not overclaim model accuracy. The app/RAG layer should make demo answers useful, but the automated scorer sees the bare GGUF path.

## Next step

Update download_model.sh to download Granite 3.3 2B Q4_K_M to model/hyvegrid-offline.gguf, then run the profiler path.
