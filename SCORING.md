# SCORING.md — What affects the ADTC score and what does not

This file exists to stop anyone, human or coding agent, from optimizing the wrong layer. Read it before touching code. If a task does not move something in the "scored" column below, it is product or demo work, not scoring work, and it waits until the model is locked.

---

## The formula

```
S_total = 0.50 × S_acc + 0.30 × S_perf + 0.20 × S_eff − P_thermal
```

Accuracy 50%, throughput 30%, efficiency 20%, thermal penalty up to −10. OOM or crash means S_total = 0 and disqualification.

---

## What is scored (the bare GGUF model only)

The evaluator downloads your `.gguf` via `download_model.sh` and runs it through `llama.cpp` (`llama-bench` for telemetry). Only the model and its `metadata.json` are in this path.

| Lever | Score effect | How to move it |
|---|---|---|
| Model's own English agriculture/apiculture knowledge | S_acc, 50% | Pick a stronger small model, or fine-tune knowledge into the weights |
| Performance on the domain MCQ validation set | S_acc, 50% | Same. Test on the provided set early |
| Tokens per second | S_perf, 30% | Smaller model, good quantization, reach 15 TPS |
| Peak RAM | S_eff, 20% | Smaller model, Q4_K_M, small context window |
| Core temperature and throttling | −10 | Keep the model light enough to avoid sustained heavy load |
| OOM or crash | disqualify | Stay well within the 8 GB profile |

If the work does not change the model file, the quantization, or the two metadata test prompts, it does not change these numbers.

---

## What is NOT scored by automated telemetry (the demo and bonus layer)

These earn points only through the human panel, the African Use Case Bonus (up to 10 points), the demo video, and the live defense. They do not touch S_perf, S_eff, or the automated part of S_acc.

| Layer | Earns | Does NOT earn |
|---|---|---|
| CLI engine | Demo clarity | Telemetry |
| SQLite + FTS5 RAG | Cross-disciplinary credit, live-defense strength | Automated accuracy |
| Public apiculture knowledge base | African use-case story | Telemetry |
| Yoruba mode | African Use Case Bonus, field credibility | Telemetry, and English is the evaluation language |
| Web UI and screens | Demo and panel impression | Telemetry |

Retrieval cannot ground an answer the evaluator never routes through your retriever. For the scored accuracy, knowledge must live in the model weights.

---

## Open verification (resolve before trusting this file fully)

- Confirm from the profiler source whether the accuracy evaluation applies any system prompt or chat template to the model. If it does not, all knowledge must live in the weights.
- Confirm whether the `packaging` field (`docker_image`, `docker_build_from_repo`, `binary_bundle`) allows any inference-time wrapper in the scored path. Do not assume it does.

Until these are confirmed, treat the model as the sole scored artifact.

---

## The one rule for any builder or agent

```
If your task does not change the .gguf, its quantization, or the 2 metadata test prompts,
it does not change the automated score. Build it only after the model is locked.
```
