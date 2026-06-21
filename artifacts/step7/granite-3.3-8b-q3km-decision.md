# Step 7B Decision — Reject Granite 3.3 8B Q3_K_M

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Candidate: `ibm-granite/granite-3.3-8b-instruct-GGUF / granite-3.3-8b-instruct-Q3_K_M.gguf`  
Decision: reject as scoring candidate

---

## Evidence

### Source and access

- Repo: `ibm-granite/granite-3.3-8b-instruct-GGUF`
- File: `granite-3.3-8b-instruct-Q3_K_M.gguf`
- License: Apache 2.0
- Gated: False
- HEAD status: 200
- Local file size: 3.7 GB
- SHA256 recorded in `artifacts/step7/granite-3.3-8b-q3km.sha256`

### Prompt result

Official hive-health prompt family:

> A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?

Model answer:

> The beekeeper should first check for signs of pests or diseases, such as Varroa mites or American Foulbrood (AFB). They should avoid disturbing the hive excessively, as this could spread potential infection or stress the bees further.

### Runtime signal

- Prompt: 5.2 t/s
- Generation: 0.8 t/s

---

## Why this fails

The answer is not strong enough to justify the model size or speed cost.

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

The model jumped to Varroa/AFB instead of following the evidence in the prompt.

---

## Scoring implication

Granite 8B Q3_K_M is much slower than Granite 2B and does not improve the apiculture answer quality enough to justify its size.

This candidate should not be benchmarked further.
