# HyveGrid Offline Granite Model Lock Decision

## Decision

Granite 3.3 2B Instruct Q4_K_M is selected as the accuracy-first runtime model candidate for the next build phase.

This is a model-lock decision for the current build phase, subject to final ADTC profiler/submission checks. It records the current accuracy-first selection based on the completed Phase 1 evaluation and challenger comparison; it is not a guarantee that Granite passes every final submission gate.

## Why Granite

Human review found Granite safer and more relevant for apiculture field guidance than Qwen. Granite was more inspection-first, colony-welfare-first, and field-practical across the reviewed prompts. It avoided several risky answer patterns seen in Qwen and Phi, including harvesting uncapped nectar or brood frames, recommending insecticides or baits as an immediate action, and over-crediting irrelevant hazard lists.

Granite remains within VM memory and already passed prior benchmark/profiler smoke testing without an OOM, crash, or thermal flag. Granite is not perfect, but it is the strongest current balance of field safety, answer quality, and offline feasibility.

## Rejected or non-selected challengers

| Model                            | Status       | Reason                                                                                                                              |
| -------------------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Qwen2.5 1.5B Instruct Q4_K_M     | Not selected | Fast and efficient, but human review found unsafe or weak field guidance, including false keyword positives                         |
| Phi-4-mini-instruct Q4_K_M       | Not selected | Technically viable, but full bare review found likely weaker quality than Granite, with pest, harvest, and heat-management concerns |
| NVIDIA Nemotron 3 Nano 4B Q4_K_M | Not selected | Smoke test failed; low generation speed, visible reasoning output, and weaker two-prompt answer quality                             |
| Gemma 2 2B / Gemma 3 4B          | Not selected | Earlier benchmarks were slower, heavier, or did not justify replacing Granite                                                       |

## Evidence summary

* Granite keyword score: 84.8%
* Qwen keyword score: 81.8%
* Human-adjusted Granite estimate: 28.5 / 33 = 86.4%
* Human-adjusted Qwen estimate: 19 / 33 = 57.6%
* Phi keyword score: 81.8%, but likely weaker than Granite by first-read review
* Phi smoke: 5.77 ± 1.30 generation tokens/second, peak RSS about 3.65 GiB
* Nemotron smoke: 3.06 ± 0.58 generation tokens/second, peak RSS about 3.36 GiB
* Nemotron did not justify full evaluation because of low speed, visible reasoning output, and weak two-prompt quality

Sources for these numbers:

* Granite and Qwen keyword and human-adjusted scores: `artifacts/eval/bare-human-review-decision.md`
* Phi full bare keyword score and first-read notes: `artifacts/eval/phi-full-bare-evaluation.md`
* Phi smoke telemetry: `artifacts/eval/phi-smoke-benchmark.md`
* Nemotron smoke telemetry and two-prompt notes: `artifacts/eval/nemotron-smoke-benchmark.md`

## ADTC fit

Runtime remains llama.cpp. Model format remains GGUF. Offline runtime remains local. No cloud model, API, external database, or internet dependency is being added. GLM/Codex/Claude are coding assistants only, not runtime models. Public challenge edition remains IP-safe.

## Next build phase

With Granite selected for the current build phase, the next implementation phase should move to:

1. Public apiculture knowledge notes
2. SQLite FTS retrieval
3. Prompt builder
4. llama.cpp runtime integration
5. Test prompts
6. Yoruba mode
7. Local web UI

## Decision note

Do not reopen model search unless Granite fails final profiler/submission checks or a later public model clearly improves both field quality and ADTC scoring feasibility.
