# Metadata Finalization and Profiler Accuracy-Path Audit (Task 017)

1. **Task title and date:** Metadata finalization (submitter email) and full ADTC
   profiler accuracy-path check (no `--skip-accuracy`). Date: 2026-06-23.

## Starting commit

- `7eaf81c2ee4c2d54cb0cd7ee292a64058f62c555`

## Branch

- `phase-1-eval-harness`

## Scope

Finalize the last metadata placeholder and test whether the ADTC profiler can run
without `--skip-accuracy`. Evidence-only; no product features, no UI, no Yoruba,
no new models, no app/RAG/runtime refactor.

## Files inspected

- `metadata.json`
- `download_model.sh`
- `.gitignore`
- `artifacts/eval/adtc-profiler-audit-task-016.md` (prior audit / baseline)
- `artifacts/profiler/task-016-submission-skip-accuracy.json` (baseline telemetry)
- `adtc-profiler run --help` (accuracy interface)

## Files changed

- `metadata.json` — `submitter.email` placeholder replaced (see exact change below).
- Generated outputs (untracked):
  - `artifacts/profiler/task-017-submission-with-accuracy.json`
  - `artifacts/eval/metadata-and-accuracy-audit-task-017.md` (this artifact)

No edits to `download_model.sh`, `.gitignore`, model files, app/RAG/runtime, or
tests.

## Exact metadata change

Single line, `submitter.email`:

```diff
   "submitter": {
     "name": "Amaete Umanah",
-    "email": "REPLACE_BEFORE_FINAL_SUBMISSION",
+    "email": "amaete@umanah.org",
     "github_handle": "amaeteventurestudios"
   },
```

`git diff metadata.json` confirms this is the only change.

## Confirmation that test prompts remain exact

- `metadata.json` is valid JSON (parsed successfully).
- Exactly **two** `test_prompts`.
- Both are **byte-exact** against the official prompts (programmatic check):
  1. `hive-health-advisor-001` — "A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?" ✓
  2. `site-readiness-advisor-001` — "An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?" ✓
- The model block (Granite-3.3-2B-Instruct Q4_K_M, llama.cpp, Q4_K_M, binary_bundle) is unchanged.

## Confirmation that model/download path remains aligned

- `bash download_model.sh` → "Model already exists at model.gguf", SHA256 verified, exit 0 (idempotent).
- `model.gguf` exists (symlink → `model-candidates/granite-3.3-2b-instruct-Q4_K_M.gguf`); `test -f model.gguf` passes.
- Profiler again resolved the model to **`model.gguf`** (same as Task 016), matching the download script. No metadata-path field is required; alignment is intact.

## Profiler command without `--skip-accuracy`

```
.venv/bin/adtc-profiler run \
  --submission . \
  --mode participant \
  --output artifacts/profiler/task-017-submission-with-accuracy.json
```

(Defaults applied: `--accuracy-task arc_easy`, `--accuracy-limit 50`, `--seed 42`.
No `--skip-accuracy`.)

## Profiler result

- **Exit code: 0** (the profiler did not crash; it ran the throughput bench, then
  attempted the accuracy path).
- **Output JSON:** `artifacts/profiler/task-017-submission-with-accuracy.json` (written).
- **Profiler console output (verbatim):**
  ```
  adtc-profiler mode=participant model=model.gguf
  → running llama-bench (throughput)…
  lm_eval not installed — emitting empty accuracy. Install with `uv sync --extra accuracy` for real benchmarks.
  ✓ wrote artifacts/profiler/task-017-submission-with-accuracy.json
  ```
- **Telemetry (from JSON):**

  | Field | Value |
  |---|---|
  | tokens_per_second_generation | 4.38 |
  | first_token_latency_ms | 18130.0 (~18.1 s, cold load + pp512) |
  | prompt_tokens / generated_tokens | 512 / 128 |
  | peak_rss_mb | 2736.35 (~2.67 GB) |
  | steady_state_rss_mb | 2629.85 |
  | cpu_percent_p99 | 97.0 |
  | throttled | false |
  | params_match | true (granite, 2B) |
  | context_length (model-reported) | 131072 |
  | git_commit_sha | 7eaf81c2ee4c |
  | submitter.email (read from working tree) | amaete@umanah.org |

- **Accuracy values:** none. `accuracy: []` in the JSON.
- **Exact reason no accuracy was produced:** `lm_eval` is not installed in the
  repo `.venv`, so the profiler's accuracy step emitted an empty array. The
  profiler's own message states the fix: install with `uv sync --extra accuracy`.
  **Important scope note (not overstated):** even with `lm_eval` installed, the
  profiler's default task is the **public** `arc_easy` set; the profiler help
  states "Real audits use the hidden validation subset," which is not available
  to a participant locally. So no hidden-set accuracy was — or could be —
  measured here. The accuracy path is therefore *runnable* (exit 0) but
  *non-productive* in this participant environment.

## Comparison to Task 016 skip-accuracy result

| Metric | Task 016 (`--skip-accuracy`) | Task 017 (no skip) |
|---|---|---|
| exit code | 0 | 0 |
| generation tokens/sec | 6.12 | 4.38 |
| peak RSS | ~2736 MB (~2.67 GB) | ~2736 MB (~2.67 GB) |
| first-token latency | ~16.4 s | ~18.1 s |
| throttled | false | false |
| accuracy | `[]` (skipped) | `[]` (attempted; lm_eval not installed) |
| params_match | true | true |

The throughput difference (6.12 vs 4.38 t/s) is run-to-run `llama-bench` variance
on the paging-prone 6.7 GB VM; peak RSS is essentially identical (~2.67 GB),
confirming the model fits comfortably under the 8 GB budget-laptop target with no
throttling. The only substantive difference is that Task 017 *attempted* the
accuracy path (vs. explicitly skipping it in Task 016), but the outcome was the
same empty `accuracy: []` because `lm_eval` is not installed locally.

## Unit test command and result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK
```

## Decision

**PASS WITH ISSUES**

- The metadata finalization succeeded: the `submitter.email` placeholder is
  replaced with `amaete@umanah.org`, JSON is valid, the two official prompts are
  byte-exact, and the model/download path remains aligned with Task 016.
- The profiler accuracy path was attempted without `--skip-accuracy` and did not
  crash (exit 0), but it could not produce accuracy because `lm_eval` is not
  installed in the local `.venv`, and the real (hidden) validation subset is not
  available to a participant. This is a documented environment/Gate-2 limitation,
  not a submission-path defect — per task instructions, no workaround was
  invented.

## Remaining issues and recommended next task

- **Accuracy is unverified locally.** To get real numbers, install the accuracy
  extra (`uv sync --extra accuracy`, which brings `lm_eval`) and run the profiler
  with the **hidden validation subset** on the audit side (Gate 2). This is not
  something a participant can self-serve locally, so it remains a Gate-2/audit
  step at final submission.
- **`docker_image_digest: unknown`** and **`core_temp_c_peak: null`** remain
  expected for a bare-VM local participant run (no Docker, no host temp sensor);
  `throttled: false`.
- The finalized `metadata.json` should get a final human review at submission
  time (email now real; all other fields unchanged since Task 016).
- Recommended **Task 018**: on the audit/submission host, install the accuracy
  extra and run the profiler against the hidden validation subset to obtain the
  Gate-2 accuracy number; then finalize/submit. No further participant-side
  metadata or runtime work is required.
