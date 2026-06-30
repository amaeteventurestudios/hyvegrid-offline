# HyveGrid Offline ADTC 2026 Report

This is the challenge report for the public ADTC 2026 edition of HyveGrid Offline.
HyveGrid Offline is a local, offline apiculture intelligence assistant for
African beekeepers and extension workers. It combines a local GGUF model,
`llama.cpp` runtime, local retrieval over public apiculture notes, and a
FastAPI/localhost browser interface served from the laptop.

HyveGrid Offline is not a certified disease diagnosis tool. It is field triage
and guidance support for cautious inspection, record keeping, and local
apiculture reasoning.

## Benchmark and submission-path evidence

### 1. Scored submission path

The official ADTC scoring path is the bare GGUF model only. The evaluator obtains
the model through `download_model.sh` and runs it through `llama.cpp`
(`llama-bench` for telemetry).

- The profiler resolves the model to `model.gguf`.
- `download_model.sh` produces and verifies `model.gguf` (idempotent; SHA256
  check passes). It targets the Granite 3.3 2B Instruct Q4_K_M GGUF file.
- The locked model is Granite 3.3 2B Instruct, quantization Q4_K_M, in GGUF
  format, served by `llama.cpp`.
- The app, SQLite FTS5 retrieval, public apiculture notes, CLI, local browser
  UI, and language layer are demo and field-product layers. They improve demo
  clarity, the African use-case story, and panel review. They do not improve
  automated telemetry, because the evaluator never routes scored accuracy
  through the app or retriever.

### 2. Official profiler results

Both runs used the ADTC profiler in participant mode (Gate 1) on the participant
VM: Intel i7-6700K, 6.7 GB RAM, no GPU, Ubuntu 22.04.5 LTS.

| Run | Command | Accuracy mode | Generation t/s | First-token latency | Peak RSS | Throttled | Result |
|---|---|---|---|---|---|---|---|
| Task 016 | participant mode with `--skip-accuracy` | skipped | 6.12 | ~16.4 s | ~2.67 GB | false | PASS |
| Task 017 | participant mode without `--skip-accuracy` | attempted, empty because `lm_eval` was not installed | 4.38 | ~18.1 s | ~2.67 GB | false | PASS WITH ISSUES |

Both runs exited 0, with no OOM or crash, `params_match: true`, and the profiler
reporting the model as Granite (2B). Peak RSS of about 2.67 GB is well within the
8 GB budget-laptop target. Throughput varies run to run (6.12 vs 4.38 t/s) on the
6.7 GB VM because the Q4 model pages against swap under memory pressure.

### 3. App CLI smoke results

The app CLI runs the full demo path: public knowledge retrieval, prompt builder,
`llama.cpp`, then Granite. Task 014 ran the first real local smoke. Task 015
cleaned up the output, ranking, and truncation issues.

| Prompt | Task | Wall time | Max RSS | Generation t/s | Top source | Clean output | Truncated | Exit |
|---|---|---|---|---|---|---|---|---|
| 1 (hive health) | 014 | 5:55.73 | ~5.88 GB | 2.2 | README.md (generic) | no | no | 0 |
| 1 (hive health) | 015 | 7:53.44 | ~5.79 GB | 2.8 | hive_health.md | yes | no | 0 |
| 2 (site readiness) | 014 | 7:18.30 | ~5.84 GB | 1.8 | site_readiness.md | no | yes (slight) | 0 |
| 2 (site readiness) | 015 | 4:00.66 | ~5.78 GB | 3.6 | site_readiness.md | yes | no | 0 |

Task 014 showed real Granite inference worked, but had problems: llama.cpp chrome
and prompt echo in the output, Prompt 2 slightly truncated at 384 tokens, and
README.md ranking above the relevant field note. Task 015 fixed all of these:
answer-only CLI output, README.md and glossary.md demoted for normal field
questions, reduced context, and max tokens raised from 384 to 512. Tests: 45/45.

App CLI RSS (about 5.8 GB) is higher than profiler RSS (about 2.67 GB) because the
CLI demo path has a larger process footprint and runs the app/RAG wrapper, while
the profiler measures the bare model through `llama-bench` with a controlled
context. This is why the app CLI generation rate (2.2 to 3.6 t/s) is lower than
the profiler rate (6.12 t/s): the app path pages against swap on the 6.7 GB VM.

### 4. Current local browser advisor QA

Task 040A verified the full local advisor flow across all five advisor pages.
Each page rendered, accepted the required prompt, completed a local GGUF answer,
displayed retrieved source cards, and showed `Completed locally.` Evidence:
`artifacts/eval/final-advisor-flow-qa-task-040A.md`.

| Advisor | Page rendered | Local GGUF answer completed | Retrieved sources appeared | Completion status appeared |
|---|---|---|---|---|
| Hive Health Advisor | yes | yes | yes | yes |
| Site Readiness Advisor | yes | yes | yes | yes |
| Harvest Quality Coach | yes | yes | yes | yes |
| Forage and Pollination Guide | yes | yes | yes | yes |
| Hive Signal Check | yes | yes | yes | yes |

Mac local runtime QA confirmed the app can complete all five advisor flows
through the local GGUF runtime. Final constrained Ubuntu/VM profiler confirmation
remains a separate packaging step.

### 5. Offline compliance status

- Runtime is local and offline.
- No cloud runtime dependency is required.
- No external API dependency is required.
- No remote database dependency is required.
- No internet is needed during judged runtime after the model is present.
- The model format is GGUF.
- The model runtime is `llama.cpp`.
- Retrieval uses local public apiculture notes through SQLite/FTS5.
- The browser UI is a local web-style interface served from the laptop. It is not
  a cloud web app.
- The localhost app is a demo and field-support layer; the automated scoring path
  remains the bare GGUF model.

### 6. Answer safety and assumption guard

Task 038D added an unsupported-assumption guard in the prompt builder. The guard
instructs the local answer path to distinguish reported observations from
possible concerns and to phrase uncertain findings as checks.

Task 040A confirmed the Hive Health prompt did not introduce unsupported claims
such as no eggs, no young brood, queen absent, disease confirmed, or mites
confirmed. The verified answer used safer wording such as checking whether eggs
and young larvae are present, confirming brood pattern by inspection, and checking
whether ants are near the stand or entering the hive.

The app uses cautious field framing:

- possible concern
- check first
- avoid doing immediately
- confirm by physical inspection
- consult an experienced beekeeper or extension officer when needed

HyveGrid Offline is not a certified disease diagnosis tool.

### 7. Language support

English remains the default. Yorùbá is preserved as a supported African language
layer with controlled labels, templates, glossary entries, and review-needed
copy. HyveGrid Offline supports English and Yorùbá, with structured Hausa and
Swahili field-template modes prepared for human language review.

Hausa and Swahili do not appear as `Preview` in the current selector. They use
structured field-template modes with visible human-review-needed notes. They are
not claimed as human-reviewed, native-quality, or fully validated language modes.
The local model is not asked to freestyle full Hausa or Swahili translations.

Evidence:

- `artifacts/eval/african-language-browser-qa-task-039D.md`
- `artifacts/eval/african-language-review-export-task-039D.md`

### 8. Runtime evidence

- Local runtime diagnostics pass.
- The Mac local runtime path resolver can find a local `llama-cli` without using
  the Ubuntu VM path.
- On the tested Intel macOS development machine, CPU-only fallback applies with
  `--device none -ngl 0`.
- `llama.cpp` remains the runtime.
- GGUF remains the model format.
- The Mac local browser app completed all five advisor flows through local GGUF
  inference in Task 040A.

Mac local evidence is useful development evidence. It is not presented as the
final ADTC constrained Ubuntu/VM profiler result.

### 9. Accuracy status

- No local hidden-validation accuracy score is claimed.
- The Task 017 profiler run attempted the accuracy path, but emitted an empty
  accuracy result because `lm_eval` was not installed in the local venv.
- Final hidden-set accuracy must be measured by the official audit environment or
  by an organizer-provided validation setup.

### 10. Evidence artifact index

| Task | Evidence | Path |
|---|---|---|
| Task 016 | ADTC profiler and submission-path audit | `artifacts/eval/adtc-profiler-audit-task-016.md` |
| Task 017 | Metadata finalization and profiler accuracy-path audit | `artifacts/eval/metadata-and-accuracy-audit-task-017.md` |
| Task 038D | Local runtime success and unsupported-assumption guard | `artifacts/eval/local-runtime-success-answer-guard-task-038D.md` |
| Task 039A | Multilingual scaffold | `artifacts/eval/multilingual-scaffold-task-039A.md` |
| Task 039B | Multilingual browser QA | `artifacts/eval/multilingual-browser-qa-task-039B.md` |
| Task 039C | African language structured templates | `artifacts/eval/african-language-template-parity-task-039C.md` |
| Task 039D | African language QA and reviewer export | `artifacts/eval/african-language-browser-qa-task-039D.md`; `artifacts/eval/african-language-review-export-task-039D.md` |
| Task 040A | Final advisor flow QA | `artifacts/eval/final-advisor-flow-qa-task-040A.md` |

### 11. Compliance status

- GGUF model format: confirmed
- `llama.cpp` profiler path: confirmed
- `download_model.sh` idempotent: confirmed
- `metadata.json` valid: confirmed
- exactly two official prompts in `metadata.json`: confirmed
- `submitter.email` finalized: confirmed
- no model files committed: confirmed
- no cloud/API runtime dependency: confirmed
- no private/proprietary material: confirmed
- public challenge edition boundary: confirmed

### 12. Limitations and remaining work

- Throughput is below the 15 t/s target (observed 6.12 and 4.38 t/s in profiler
  runs; 2.2 to 3.6 t/s in app CLI runs).
- Accuracy is not locally measured.
- Final Ubuntu/VM constrained profiler audit remains pending if a fresh final
  packaging run is required.
- Demo video script/runbook remains pending.
- Clean clone audit remains pending.
- Human review is recommended for Yorùbá, Hausa, and Swahili before field
  deployment, especially Hausa and Swahili.
- The app/RAG layer improves demo clarity and field usability but not automated
  telemetry.
- HyveGrid Offline is field triage and guidance support, not certified diagnosis.
