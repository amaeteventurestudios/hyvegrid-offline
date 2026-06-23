# ADTC Profiler and Submission-Path Audit (Task 016)

1. **Task title and date:** ADTC profiler and submission-path audit. Date: 2026-06-23.

## Starting commit

- `fa1b22623c82909a5789d48d8c36c1fee9ac984f`

## Branch

- `phase-1-eval-harness`

## Scope

Profiler/compliance evidence only: confirm the official scored submission path
(metadata.json -> download_model.sh -> Granite GGUF -> llama.cpp / llama-bench
telemetry via the ADTC profiler) is aligned, runnable, and documented after the
Granite runtime cleanup. No UI, no Yoruba, no new models, no RAG changes.

## Files inspected

- `metadata.json`
- `download_model.sh`
- `.gitignore`
- `SCORING.md`
- `artifacts/eval/granite-runtime-cleanup-task-015.md` (prior smoke numbers for comparison)
- `model/` and `model.gguf` (symlinks to the Granite Q4_K_M file)
- `adtc-profiler` CLI (`--help`, `run --help`)

## Files changed

**None.** No source/config/model files were modified — the submission path was
already aligned (see audits below). Only generated outputs were produced:
- `artifacts/profiler/task-016-submission-skip-accuracy.json` (profiler output, untracked)
- `artifacts/eval/adtc-profiler-audit-task-016.md` (this artifact)

## metadata.json audit

- Schema-valid; the profiler echoed it back unchanged into the submission JSON.
- Exactly **two** `test_prompts`, both byte-exact matches to the official ADTC prompts:
  1. `hive-health-advisor-001` — "A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?"
  2. `site-readiness-advisor-001` — "An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?"
- `model`: name `Granite-3.3-2B-Instruct Q4_K_M`, runtime `llama.cpp`, quantization `Q4_K_M`, packaging `binary_bundle` — matches the locked candidate.
- `model_info.params_match: true` (profiler-confirmed); `architecture: granite`; `context_length: 131072`.
- `budget_laptop_claim: true` and `environment.measured_on: participant_laptop` (profiler-confirmed).
- Note: metadata.json has **no explicit model-path field**. The profiler resolves the model to `model.gguf` by default, which is exactly what `download_model.sh` produces — so metadata, the download script, and the profiler are consistent without requiring a metadata edit.
- Pre-submission placeholder to replace later (not a Task 016 item): `submitter.email = "REPLACE_BEFORE_FINAL_SUBMISSION"`.

## download_model.sh audit

- Idempotent: re-ran with the model present → "Model already exists at model.gguf", then SHA256 verification, exit 0.
- Targets `MODEL_PATH="model.gguf"` (repo root) and verifies SHA256 `ac71e9e3…d95c4852` against the Granite 3.3 2B Instruct Q4_K_M file from the official ibm-granite HF repo. Verification passed.
- Path alignment: the profiler also resolves the model to `model.gguf`, so the download script and the profiler use the **same path**. (The app/CLI uses a separate symlink `model/granite-3.3-2b-instruct-q4_k_m.gguf` to the same underlying file; that is an internal app path, not part of the profiler submission path.)
- No redesign needed; works offline once the model is present (no download triggered this run).

## .gitignore / model-file audit

- `.gitignore` excludes `model/`, `*.gguf`, `*.bin`, `*.safetensors` — so the model files and GGUF weights are not committable. Confirmed: `git status` shows no model/GGUF files.
- The generated profiler JSON (`artifacts/profiler/*.json`) is **not** gitignored (the `artifacts/*.json` rule only matches the top level), so it is currently untracked/committable. Left as-is per scope (no .gitignore change requested).

## Profiler install / status

- `adtc-profiler` was **not** installed and is **not** on PATH.
- Install requirement: Python **>= 3.11**. System `python3` is 3.10.12, so a global
  install was rejected (`ERROR: requires a different Python: 3.10.12 not in '>=3.11'`).
- Installed into the repo's existing gitignored `.venv` (Python 3.11.15) — not a
  broad environment change:
  - `.venv/bin/python -m pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"`
  - Result: `adtc-profiler 0.1.0` installed (commit `cf3432c`).
- Exact install command recorded for final submission environment:
  `python3 -m pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"` (on a Python >= 3.11 host).

## Exact profiler command used

```
.venv/bin/adtc-profiler run \
  --submission . \
  --mode participant \
  --output artifacts/profiler/task-016-submission-skip-accuracy.json \
  --skip-accuracy
```

This matches the task-specified command form (`run --submission . --mode participant --output … --skip-accuracy`) exactly; the only deviation is the `.venv/bin/` prefix because the tool was installed in the project venv (Python 3.11) rather than globally. No corrected command was needed — the documented interface worked as-is.

## Profiler result table

| Field | Value |
|---|---|
| Exit code | **0** |
| profiler_version | adtc-profiler 0.1.0 |
| schema_version | 1.0.0 |
| mode | participant (Gate 1 submission.json) |
| model resolved | `model.gguf` |
| accuracy | `[]` (skipped via `--skip-accuracy`) |
| **tokens_per_second_generation** | **6.12** |
| first_token_latency_ms | 16382.31 (~16.4 s, cold model load + pp512) |
| prompt_tokens / generated_tokens | 512 / 128 |
| **peak_rss_mb** | **2736.31 (~2.67 GB)** |
| steady_state_rss_mb | 2647.94 |
| peak_vms_mb | 3026.77 |
| cpu_percent_p99 | 97.5 |
| core_temp_c_peak | null (no host temp sensor) |
| **throttled** | **false** |
| context_length (model-reported) | 131072 |
| architecture | granite |
| claimed_params_estimate / params_match | 2B / true |
| git_commit_sha | fa1b22623c82 (matches HEAD) |
| docker_image_digest | unknown |
| random_seed | 42 |
| OOM / crash | none |

## Link / path to profiler JSON output

- `artifacts/profiler/task-016-submission-skip-accuracy.json` (untracked; schema-valid Gate 1 submission.json)

## Comparison to previous smoke numbers (Task 014 / Task 015)

| Metric | Task 014 (CLI smoke) | Task 015 (CLI smoke) | Task 016 (profiler llama-bench) |
|---|---|---|---|
| generation tokens/sec | 2.2 (P1) / 1.8 (P2) | 2.8 (P1) / 3.6 (P2) | **6.12** |
| peak RSS | ~5.88 GB (P1) / ~5.84 GB (P2) | ~5.79 GB (P1) / ~5.78 GB (P2) | **~2.67 GB** |
| first-token latency | not measured | not measured | ~16.4 s (cold load) |
| throttled | n/a | n/a | false |
| exit code | 0 | 0 | 0 |
| path used | `model/granite-…gguf` (app) | same | `model.gguf` (profiler) |

**Interpretation — the profiler telemetry confirms the Task 014/015 findings.**
The profiler's controlled `llama-bench` run (pp512/tg128, ~2.67 GB RSS) shows the
model generating at **6.12 t/s with no throttling**, far faster than the app CLI
smoke runs (2.2-3.6 t/s). The difference is memory footprint: `llama-bench` fits
in ~2.7 GB (well under the 8 GB budget-laptop target), whereas the app's
`llama-cli` path with a larger context/KV cache and conversation overhead sat at
~5.8 GB RSS and paged against swap on the 6.7 GB VM. This directly corroborates
the Task 015 conclusion that the app's slower smoke numbers were caused by
swap-paging memory pressure, **not** by the model itself. The ~16.4 s
first-token latency reflects the one-time cold model load, consistent with the
~60-90 s load phase observed across smoke runs.

## Any failures or corrected commands

- **Profiler Python-version failure (captured, not a silent guess):**
  - Attempted: `python3 -m pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"`
  - Error: `ERROR: Package 'adtc-profiler' requires a different Python: 3.10.12 not in '>=3.11'`
  - Resolution: installed into the repo's existing `.venv` (Python 3.11.15). No broad environment change, no profiler command correction needed.
- **No metadata/download path mismatch.** Although `download_model.sh` targets `model.gguf` while the app uses `model/granite-3.3-2b-instruct-q4_k_m.gguf`, the **profiler** resolves the model to `model.gguf` — identical to the download script. No metadata.json or download_model.sh edit was required.
- **No internet needed for the model** (present locally); `--skip-accuracy` avoided the lm_eval network/benchmark step.

## Decision

**PASS**

The official scored submission path is aligned, runnable, and documented:
metadata.json is schema-valid with exactly the two official prompts and the
locked Granite model; download_model.sh is idempotent and produces `model.gguf`,
the path the profiler resolves; `.gitignore` excludes model/GGUF files; the model
is present locally; the ADTC profiler participant mode ran to exit 0 and emitted a
schema-valid Gate 1 submission.json with telemetry (6.12 tok/s, ~2.67 GB peak
RSS, no throttle, params_match true, correct commit SHA); 45/45 unit tests pass.
No source/config/model files changed.

## Remaining issues and recommended next task

- `submitter.email` still holds `REPLACE_BEFORE_FINAL_SUBMISSION` — replace before final submission (out of scope here; metadata ran fine with the placeholder).
- `docker_image_digest: unknown` and `core_temp_c_peak: null` are expected for a bare-VM local audit (no Docker, no host temp sensor); `throttled: false`.
- Accuracy was skipped (`--skip-accuracy`); a real Gate 2 audit run requires the hidden lm_eval validation subset and more time.
- Recommended **Task 017**: run the profiler **without** `--skip-accuracy` against the hidden validation subset for a true Gate 2 accuracy number, and finalize `metadata.json` submitter fields for submission. The runtime/submission plumbing itself needs no further work.
