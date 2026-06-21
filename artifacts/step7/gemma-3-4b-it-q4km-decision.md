# Step 7B Decision — Reject Gemma 3 4B IT Q4_K_M

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Candidate: `ggml-org/gemma-3-4b-it-GGUF / gemma-3-4b-it-Q4_K_M.gguf`  
Decision: reject as scoring candidate

---

## Evidence

### Load and runtime

- Model loaded successfully through local llama.cpp.
- File size: 2.3 GB.
- SHA256 recorded in `artifacts/step7/gemma-3-4b-it-q4km.sha256`.
- Projected host memory during short test: 3548 MiB.
- Prompt eval: 12.69 tokens/sec.
- Generation eval: 2.62 tokens/sec.

### Prompt quality failure

Official prompt family:

> A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. Give a concise field answer. What should they check first, and what should they avoid doing immediately?

Model answer:

> Check for Varroa mites. Avoid treating immediately without confirmation of mite infestation, as treatments can negatively impact brood development.

### Why this fails

The answer does not follow the visible evidence in the prompt.

Missed required items:

- Ants entering versus ants near the stand
- Ant trails
- Hive stand contact points
- Whether ants are entering the hive
- Brood pattern
- Eggs and larvae
- Colony strength
- Avoid harvesting immediately
- Avoid moving the hive immediately unless necessary
- Confirm by physical inspection

The Varroa answer is not the right first move for this prompt. It ignores the ants and stand-access evidence.

---

## Scoring implication

Gemma 3 4B Q4_K_M is slower than Granite 2B and did not produce a better apiculture answer on the official prompt family.

This candidate does not justify deeper benchmark work.

---

## Next step

Move to Qwen3-1.7B Q4_K_M as the speed-lane candidate.
