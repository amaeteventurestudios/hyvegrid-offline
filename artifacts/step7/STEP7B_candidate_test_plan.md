# Step 7B Candidate Test Plan

Date: 2026-06-20
Project: HyveGrid Offline ADTC 2026
Status: model not locked
Scope: model experimentation only

Do not start UI, RAG, Yoruba mode, or app work in this step.

---

## Why this step exists

Granite 3.3 2B Q4_K_M is efficient but too shallow on the official HyveGrid prompt families.

Gemma-2-2B-it Q4_K_M sometimes gives better content than Granite but is slower.

Granite QLoRA V1, V2, and V3 did not solve the quality gap enough to justify GGUF conversion.

The next step is to test stronger or faster public GGUF candidates before locking the scoring model.

---

## Scoring reminder

ADTC automated scoring is model-centric.

Score formula:

S_total = 0.50 × S_acc + 0.30 × S_perf + 0.20 × S_eff − P_thermal

Practical meaning:

| Lever | Weight / effect | What moves it |
|---|---:|---|
| Accuracy | 50% | Better model knowledge, better quantization, or useful fine-tune |
| Tokens/sec | 30% | Smaller/faster GGUF, quantization, llama.cpp behavior |
| Peak RAM | 20% | Smaller model, lower quantization, smaller context |
| Thermal/OOM | Gate/penalty | Avoid heavy models that overheat, throttle, crash, or OOM |

---

## Current baseline

| Model / experiment | Result | Decision |
|---|---|---|
| Gemma-2-2B-it Q4_K_M | 2.03 TPS, 1.949 GB peak RSS | Better content sometimes, but slow |
| Granite-3.3-2B-Instruct Q4_K_M | 2.97 TPS earlier, 1.723 GB peak RSS | Efficient, but shallow |
| Granite llama-bench 4 threads | pp128 26.59 t/s, tg64 2.95 t/s | Verified slow generation |
| Granite llama-bench 8 threads | pp128 26.07 t/s, tg64 3.32 t/s | Verified slow generation |
| Granite QLoRA V2 | eval loss 1.448, token accuracy 0.7162 | Save adapter only, do not convert |
| Granite QLoRA V3 | eval loss 1.454, token accuracy 0.6979 | Save adapter only, do not convert |

---

## Candidate order

### 1. Gemma 3 4B IT

Role: accuracy-ceiling test with manageable size.

Test first because accuracy is 50% of the score. A bigger model can be justified only if answer quality improves enough to offset lower speed and efficiency.

Candidate sources to verify before download:

| Source | Candidate | Notes |
|---|---|---|
| google/gemma-3-4b-it-qat-q4_0-gguf | Official QAT Q4_0 GGUF | Official source, but not Q4_K_M |
| ggml-org/gemma-3-4b-it-GGUF | Q4_K_M GGUF candidate | Strong candidate if public download works |
| bartowski/google_gemma-3-4b-it-GGUF | Q4_K_M GGUF candidate | Community fallback |

Required verification:
- Exact Hugging Face repo
- Exact `.gguf` filename
- License
- Gated or ungated access
- Public download without token
- llama.cpp compatibility
- Keep model files out of git

### 2. Qwen3-1.7B Q4_K_M

Role: speed-lane test.

Test second because it may beat Granite on answer structure while staying closer to the RAM efficiency target.

Required verification:
- Exact Hugging Face repo
- Exact `.gguf` filename
- License
- Gated or ungated access
- Public download without token
- llama.cpp compatibility

### 3. Granite 3.3 8B Q3 only if needed

Role: last accuracy-ceiling fallback.

Use only if Gemma 3 4B does not improve quality enough and Qwen3-1.7B does not close the gap.

Expected risk:
8B Q3 may be too slow, too hot, or too RAM-heavy for scoring even if answer quality improves.

---

## Candidate acceptance criteria

A candidate is worth deeper profiling only if it improves answer quality on the official prompt families.

### Hive-health prompt must cover

- Ants entering versus ants near the stand
- Ant trails
- Stand contact points
- Brood pattern
- Eggs and larvae
- Colony strength
- Avoid harvesting immediately
- Avoid moving the hive immediately unless necessary

### Site-readiness prompt must cover

- Cassava
- Mango
- Pepper
- Vegetables
- Pesticide spray risk
- Seasonal water reliability
- Dry-season backup water
- Shade and wind
- Human and livestock safety
- Staged placement

### Heat-stress variant must cover

- Bearding
- Direct sun
- Shade
- Airflow
- Entrance blockage
- Avoid sealing, spraying, or harvesting during stress

---

## Decision rule

Do not lock a model from one good answer.

Compare:
1. Official prompt answer quality
2. Hidden-prompt style variants
3. llama-bench generation TPS
4. Peak RSS from profiler or constrained run
5. License and public download safety
6. Clean repo state

---

## Do not do in Step 7B

- Do not start UI
- Do not start RAG
- Do not start Yoruba mode
- Do not modify metadata.json
- Do not modify download_model.sh
- Do not commit model files
- Do not convert Granite V2 or V3 adapters yet
- Do not repeat Granite 2B speed tests
