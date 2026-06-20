# Step 7 Post-Finetune Model Strategy

## Purpose

This note records the decision after Granite QLoRA V1, V2, and V3. HyveGrid Offline remains model-first for ADTC 2026. App, RAG, Yoruba, and UI work remain deferred until the scoring model is locked or clearly chosen.

## Current scoring frame

ADTC scoring is model-centric:

S_total = 0.50 × S_acc + 0.30 × S_perf + 0.20 × S_eff − P_thermal

The scored path is the bare GGUF model, quantization, profiler telemetry, and metadata prompts.

## Baseline telemetry

Gemma-2-2B-it Q4_K_M:
- TPS: 2.03
- Peak RSS: 1.949 GB
- Review: sometimes better content than Granite, but slower.

Granite-3.3-2B-Instruct Q4_K_M:
- TPS from earlier profiler-style run: 2.97
- Peak RSS: 1.723 GB
- Review: current efficiency baseline, but answer quality is shallow.

## Direct llama-bench validation

A direct llama-bench run was executed on the iMac CPU path.

Machine:
- Architecture: x86_64
- CPU: Intel Core i7-6700K @ 4.00GHz
- Physical cores: 4
- Logical cores: 8

Model:
- model/granite-3.3-2b-instruct-Q4_K_M.gguf
- Size: 1.44 GiB
- llama.cpp build: 9724f664e (9700)
- Backend: BLAS and CPU

Results:

| Threads | Prompt processing | Token generation |
|---:|---:|---:|
| 4 | pp128 = 26.59 t/s | tg64 = 2.95 t/s |
| 8 | pp128 = 26.07 t/s | tg64 = 3.32 t/s |

Conclusion:
- The earlier 2 to 3 TPS number is not only a profiler artifact on this machine.
- Prompt processing is above 15 t/s.
- Answer-token generation is around 3 t/s.
- 8 threads is slightly better than 4 threads for generation.
- Granite does not currently achieve the 15 TPS target on this iMac CPU path.
- Final speed still needs verification on a representative Ubuntu 22.04 x86 laptop or constrained ADTC-like environment before model lock.

## Fine-tune experiments reviewed

Granite QLoRA V1:
- Train examples: 52
- Eval examples: 8
- Result: ran successfully in Colab on Tesla T4.
- Problem: repeated prompt and repeated tokens in quick eval.
- Decision: do not convert, do not lock.

Granite QLoRA V2:
- Train examples: 52
- Eval examples: 8
- Final eval loss: 1.448
- Final eval mean token accuracy: 0.7162
- Result: stable output, but shallow apiculture detail.
- Decision: save adapter locally, do not convert to GGUF, do not lock.

Granite QLoRA V3:
- Train examples: 61
- Eval examples: 11
- Final train runtime: 153.4 seconds
- Train loss: 1.948
- Final eval loss: 1.454
- Final eval mean token accuracy: 0.6979
- Result: stable output, but still shallow.
- Decision: save adapter locally, do not convert to GGUF, do not lock.

## V3 quick eval gaps

Official hive ants prompt missed:
- ants entering versus ants near the stand
- ant trails
- stand contact points
- brood pattern
- eggs and larvae
- harvesting caution
- hive movement caution

Official site readiness prompt missed:
- cassava
- mango
- pepper
- vegetables
- seasonal water reliability
- dry-season backup water
- spray timing
- staged placement

Heat variant missed:
- bearding
- shade
- direct sun
- airflow
- entrance blockage
- avoiding sealing, spraying, or harvesting during stress

## Decision

Stop repeating the same Granite QLoRA strategy.

Granite QLoRA V2 and V3 show that fine-tuning works technically, but the current recipe does not inject enough specific apiculture reasoning into the model.

Do not convert V2 or V3 to GGUF yet.
Do not lock Granite yet.
Do not start UI, RAG, Yoruba, or app work yet.

## Next model experiment path

The next phase should answer two questions:

1. Can a faster 1B to 1.7B model improve throughput without collapsing apiculture answer quality?
2. Can a stronger prompt/evaluation wrapper improve answer specificity before another fine-tune?

Recommended experiments:

### Experiment A: prompt wrapper benchmark

Run base Granite and Gemma with:
- 256 or 384 output tokens instead of 120
- structured answer format
- explicit field-triage instructions
- key-point rubric scoring

### Experiment B: speed-lane model test

Test one or two smaller GGUF models in the 1B to 1.7B range.

Acceptance target:
- Meaningfully faster than Granite
- Stable output
- Does not collapse on the two official metadata prompts
- Peak RAM safely below Granite or close to it

### Experiment C: accuracy-ceiling test

Test one stronger 3B-class GGUF model only after the wrapper benchmark.

Purpose:
- Determine whether a larger or better base model solves answer specificity enough to justify slower speed or higher RAM.

## Lock criteria

A model can be locked only if:
- It has the best measured accuracy on the official prompts and eval set.
- It runs through llama.cpp as GGUF.
- It does not crash or OOM.
- Peak RAM stays safely within the 8 GB ADTC profile.
- TPS is acceptable relative to accuracy gains.
- download_model.sh and metadata.json match the final model path.
- Clean clone profiler run passes.

## Current recommendation

The fastest path is not another Granite QLoRA run.

The next move is:
1. Benchmark a stronger prompt wrapper.
2. Benchmark a 1B to 1.7B speed-lane model.
3. Keep Granite as the current efficiency and content baseline.
4. Test one 3B accuracy-ceiling model only if needed.
5. Move to app, RAG, and Yoruba only after model lock.
