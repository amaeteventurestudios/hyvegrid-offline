# HyveGrid Offline ADTC 2026 Report

This is the challenge report for the public ADTC 2026 edition of HyveGrid Offline.
It records benchmark and submission-path evidence only. It is written after the
runtime, retrieval, prompt-builder, and profiler work in Tasks 010 through 017.
It does not replace physical inspection guidance or expert beekeeping advice, and
HyveGrid is not a certified disease diagnosis tool.

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
- The app, retrieval (SQLite FTS5), public apiculture notes, CLI, and future
  Yoruba support are a demo and field-product layer. They improve demo clarity,
  the African use-case story, and panel review. They do not improve automated
  telemetry, because the evaluator never routes scored accuracy through the app
  or retriever.

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

### 4. Accuracy status

- No local hidden-validation accuracy score is claimed.
- The Task 017 profiler run attempted the accuracy path, but emitted an empty
  accuracy result because `lm_eval` was not installed in the local venv.
- Final hidden-set accuracy must be measured by the official audit environment or
  by an organizer-provided validation setup.

### 5. Compliance status

- GGUF model format: confirmed
- llama.cpp profiler path: confirmed
- `download_model.sh` idempotent: confirmed
- `metadata.json` valid: confirmed
- exactly two official prompts: confirmed
- `submitter.email` finalized: confirmed
- no model files committed: confirmed
- no cloud/API runtime dependency: confirmed
- no private/proprietary material: confirmed
- public challenge edition boundary: confirmed

### 6. Limitations

- Throughput is below the 15 t/s target (observed 6.12 and 4.38 t/s in profiler
  runs; 2.2 to 3.6 t/s in app CLI runs).
- Accuracy is not locally measured.
- The app/RAG layer improves demo clarity and field usability but not automated
  telemetry.
- HyveGrid is a field triage assistant, not a certified disease diagnosis tool.
