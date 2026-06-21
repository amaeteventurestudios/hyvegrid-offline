# Step 7B Decision — Reject Qwen3-1.7B Q4_K_M

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Candidate: `unsloth/Qwen3-1.7B-GGUF / Qwen3-1.7B-Q4_K_M.gguf`  
Decision: reject as locked scoring candidate

---

## Evidence

### Source and access

- Repo: `unsloth/Qwen3-1.7B-GGUF`
- File: `Qwen3-1.7B-Q4_K_M.gguf`
- License: Apache 2.0
- Gated: False
- HEAD status: 200
- Local file size: 1.0 GB
- SHA256 recorded in `artifacts/step7/qwen3-1.7b-q4km.sha256`

### Raw completion failure

Raw completion mode produced repeated unrelated text:

> What is the correct term for the process of removing the queen from the hive?

This was treated as an inference-mode failure, not a model rejection by itself.

### Chat-template result

Using `llama-cli` with `--single-turn` and `--reasoning off`, Qwen answered:

> Check for pests first, and avoid using strong chemicals immediately.

Speed line:

- Prompt: 27.7 t/s
- Generation: 6.0 t/s

### Why this fails

The answer is faster than Granite and Gemma, but too shallow for the official hive-health prompt family.

Missed required items:

- Ants entering versus ants near the stand
- Ant trails
- Hive stand contact points
- Brood pattern
- Eggs and larvae
- Colony strength
- Avoid harvesting immediately
- Avoid moving the hive immediately unless necessary
- Confirm by physical inspection

---

## Scoring implication

Qwen3-1.7B improves speed but does not improve scored apiculture answer quality enough to lock.

Accuracy is weighted more heavily than speed, so this candidate should not be locked.

---

## Next step

Move to Granite 3.3 8B Q3 source/license/access verification only.
