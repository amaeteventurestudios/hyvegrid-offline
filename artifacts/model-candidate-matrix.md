# HyveGrid Offline Model Candidate Matrix

Purpose: compare small GGUF model candidates for ADTC 2026 using the same scoring-aware process.

This file exists because HyveGrid Offline has two layers:

1. **Scored model path:** the `.gguf` model, quantization, RAM, throughput, accuracy, crash behavior, and metadata prompts.
2. **Demo/product path:** CLI, SQLite retrieval, public apiculture notes, Yoruba mode, and local web UI.

The scored model path is the priority until the model is locked.

---

## Decision rule

Choose the smallest model that gives the best total tradeoff across:

- Agriculture and apiculture accuracy
- Tokens per second
- Peak RAM
- License safety
- Profiler stability
- No OOM or crash risk
- No thermal flag

Do not choose the smallest model just because it is small. Accuracy is weighted more heavily than efficiency, so a larger model can win if the accuracy gain is large enough and it still runs safely on the 8 GB profile.

---

## Temporary candidate shortlist

These are starting candidates only. Do not lock any candidate until current GGUF availability, license, accuracy, RAM, and throughput have been verified.

| # | Candidate model | Model family | Params | Why consider | Main risk | Initial decision |
|---|---|---|---:|---|---|---|
| 1 | Qwen2.5-1.5B-Instruct | Qwen | 1.5B | Strong reasoning per parameter, widely available GGUF variants | Verify license and current GGUF source | Test |
| 2 | Llama-3.2-1B-Instruct | Llama | 1B | Very low RAM and likely fast | May be weaker on agriculture/apiculture knowledge | Test |
| 3 | Llama-3.2-3B-Instruct | Llama | 3B | Better reasoning and knowledge potential | May exceed the 2.5 GB target, must profile | Test only if smaller models are weak |
| 4 | Gemma-2-2B-it | Gemma | 2B | Good quality for size | Borderline RAM target, license must be reviewed | Test |
| 5 | SmolLM2-1.7B-Instruct | SmolLM | 1.7B | Small and capable | Agriculture performance unknown | Test |

---

## Full comparison matrix

| # | Candidate model | Model family | Params | Instruct tuned? | GGUF source URL | License | License cleared? | Quantization tested | File size | Context used | Peak RAM GB | TPS | First-token latency | OOM/crash? | Thermal flag? | ADTC profiler passed? | Agriculture validation score | Prompt 1 score | Prompt 2 score | Caution language quality | Apiculture reasoning quality | Site-readiness reasoning quality | Fine-tune needed? | Notes | Decision |
|---|---|---|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Qwen2.5-1.5B-Instruct | Qwen | 1.5B | Yes | Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M | Apache 2.0 | Tentative yes | Q4_K_M | TBD | 2048 | TBD | 4.9 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 2.5 | TBD | Medium | Basic but incomplete | TBD | Maybe | Prompt 1 missed key field checks. See run log. | Retest with Prompt 2 |
| 2 | Llama-3.2-1B-Instruct | Llama | 1B | Yes | TBD | TBD | No | Q4_K_M | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Keep / Reject / Retest |
| 3 | Llama-3.2-3B-Instruct | Llama | 3B | Yes | TBD | TBD | No | Q4_K_M | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Keep / Reject / Retest |
| 4 | Gemma-2-2B-it | Gemma | 2B | Yes | TBD | TBD | No | Q4_K_M | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Keep / Reject / Retest |
| 5 | SmolLM2-1.7B-Instruct | SmolLM | 1.7B | Yes | TBD | TBD | No | Q4_K_M | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | Keep / Reject / Retest |

---

## Fields to record

| Field | Why it matters |
|---|---|
| Candidate model | Exact model name being tested |
| Model family | Qwen, Llama, Gemma, SmolLM, or another family |
| Params | Main RAM and speed driver |
| Instruct tuned? | HyveGrid needs instruction-following behavior |
| GGUF source URL | Needed later for `download_model.sh` |
| License | Must allow challenge-safe use |
| License cleared? | No unclear license gets locked |
| Quantization tested | Start with Q4_K_M, then test Q5_K_M if promising |
| File size | Rough proxy for RAM pressure |
| Context used | Smaller context helps RAM and speed |
| Peak RAM GB | Drives efficiency score |
| TPS | Drives performance score |
| First-token latency | Helps responsiveness and audit notes |
| OOM/crash? | Hard rejection if yes |
| Thermal flag? | Avoid thermal penalty |
| ADTC profiler passed? | Must pass before model lock |
| Agriculture validation score | Main accuracy proxy |
| Prompt 1 score | Hive-health prompt quality |
| Prompt 2 score | Site-readiness prompt quality |
| Caution language quality | Checks whether the model avoids unsafe overclaiming |
| Apiculture reasoning quality | Checks beekeeping competence |
| Site-readiness reasoning quality | Checks farm placement and pesticide-risk reasoning |
| Fine-tune needed? | Decides whether we move into public QA dataset and training |
| Notes | Weird outputs, license concerns, profiling issues |
| Decision | Keep, reject, or retest |

---

## Official HyveGrid Offline test prompts

### Prompt 1: Hive Health Advisor

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

### Prompt 2: Site Readiness Advisor

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

---

## Manual scoring rubric: Prompt 1

Use a 0 to 5 score.

| Score | Meaning |
|---:|---|
| 5 | Mentions ants entering the hive, colony strength, brood pattern, food or water stress, avoids immediate harvest or chemical overreaction, and recommends physical inspection |
| 4 | Covers most important checks, with only minor missing detail |
| 3 | Generally useful but incomplete |
| 2 | Generic beekeeping advice with weak prioritization |
| 1 | Mostly wrong, unsafe, or misleading |
| 0 | Fails, hallucinates, or gives dangerous advice |

### Required key points for a strong Prompt 1 answer

- Check whether ants are only near the stand or entering the hive.
- Check hive stand protection, nearby ant trails, and ground contact points.
- Check colony strength and whether the colony is too weak to defend itself.
- Check brood pattern, capped brood, larvae condition, and queen-right signs.
- Check food stores, water stress, heat stress, and recent disturbance.
- Avoid harvesting immediately.
- Avoid spraying chemicals into or near the hive.
- Avoid moving the hive immediately unless there is a clear safety reason.
- Confirm by physical inspection.
- Use cautious language: possible concern, check first, not certified diagnosis.

---

## Manual scoring rubric: Prompt 2

Use a 0 to 5 score.

| Score | Meaning |
|---:|---|
| 5 | Covers pesticide risk, water reliability, forage seasonality, shade and wind, human and livestock safety, hive density, access, and farm spraying coordination |
| 4 | Covers most important factors, with only minor missing detail |
| 3 | Useful but shallow |
| 2 | Generic siting advice with weak local reasoning |
| 1 | Mostly wrong, unsafe, or misleading |
| 0 | Fails, hallucinates, or gives dangerous advice |

### Required key points for a strong Prompt 2 answer

- Evaluate pesticide and herbicide risk from pepper and vegetable farms.
- Coordinate with farmers on spray timing and chemical use.
- Check whether the seasonal water source is reliable through dry periods.
- Provide or plan clean water if the natural source dries up.
- Evaluate forage diversity and flowering seasonality across mango, vegetables, cassava, and surrounding plants.
- Avoid assuming cassava is enough forage by itself.
- Check shade, wind protection, drainage, flooding risk, and heat exposure.
- Check human, livestock, and footpath safety.
- Confirm access for hive inspection and harvest.
- Consider hive spacing, stand height, and colony density for 20 hives.
- Use cautious site-readiness language rather than promising success.

---

## Candidate run log

Use this section after each candidate test.

### Candidate run: Qwen2.5-1.5B-Instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-18 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | Qwen/Qwen2.5-1.5B-Instruct-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 32.3 t/s. Generation: 4.9 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 2.5 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 |

Notes:

- The model gave a structured answer and noticed ants, smell, and partially capped brood.
- It missed colony strength, food stores, water stress, harvest caution, chemical caution, and careful physical inspection.
- It incorrectly suggested avoiding opening the hive, using a smoker, or using a hive tool.
- Better guidance would be to inspect carefully and avoid disturbing the colony aggressively.
- Current result is usable but not strong enough to lock.

---

## Lock criteria

Do not lock the scoring model until all of these are true:

- License is cleared.
- `download_model.sh` can download the exact GGUF without credentials.
- The path matches `metadata.json`.
- ADTC profiler passes on a constrained 8 GB-style profile.
- No OOM or crash.
- No thermal flag.
- Peak RAM target is under 2.5 GB, unless a larger model is justified by measured accuracy gain.
- TPS is at or near 15.
- Prompt 1 and Prompt 2 scores are strong enough to defend publicly.
- Agriculture validation score is competitive among tested candidates.

---

## One rule

```text
If a task does not change the .gguf, its quantization, or the 2 metadata test prompts,
it does not change the automated score. Build it only after the model is locked.
```
