# REPORT.md Benchmark Section (Task 018)

1. **Task title and date:** REPORT.md benchmark and compliance evidence section.
   Date: 2026-06-23.

## Starting commit

- `d50a9f22e0d637f5f15776b45437d4641df75e5a`

## Files inspected

- `REPORT.md` (was empty, 0 bytes)
- `SCORING.md`
- `metadata.json`
- `artifacts/eval/granite-runtime-smoke.md` (Task 014)
- `artifacts/eval/granite-runtime-cleanup-task-015.md` (Task 015)
- `artifacts/eval/adtc-profiler-audit-task-016.md` (Task 016)
- `artifacts/eval/metadata-and-accuracy-audit-task-017.md` (Task 017)
- `artifacts/profiler/task-016-submission-skip-accuracy.json`
- `artifacts/profiler/task-017-submission-with-accuracy.json`

## Files changed

- `REPORT.md` (created; previously empty)
- `artifacts/eval/report-benchmark-section-task-018.md` (this artifact)

No changes to `metadata.json`, `download_model.sh`, `.gitignore`, model files,
app/RAG/runtime code, or tests.

## REPORT.md section added or updated

Added a new top-level report and the required section
`## Benchmark and submission-path evidence` with six subsections:

1. Scored submission path (profiler resolves `model.gguf`; `download_model.sh`
   produces/verifies it; locked model is Granite 3.3 2B Instruct Q4_K_M GGUF;
   app/RAG is a demo and field-product layer, not the telemetry path).
2. Official profiler results (table for Task 016 and Task 017).
3. App CLI smoke results (comparison table for Task 014 and Task 015; note that
   app CLI RSS is higher than profiler RSS because the demo path runs the
   app/RAG wrapper).
4. Accuracy status (no local hidden-validation score claimed; Task 017 accuracy
   empty because `lm_eval` was not installed; final accuracy is audit-side).
5. Compliance status (10-item checklist).
6. Limitations (below the 15 t/s target; accuracy not locally measured; app/RAG
   helps demo/field usability not telemetry; field triage tool, not certified
   diagnosis).

Style followed: direct, factual, concise; no hype; no em dashes; no banned words
("fluff", "vibe"); tables and checklists used.

## Evidence sources used

- Profiler telemetry was read directly from the two JSON files (authoritative):
  - Task 016: 6.12 t/s, 16382.31 ms first-token, 2736.31 MB peak RSS, throttled
    false, accuracy `[]`.
  - Task 017: 4.38 t/s, 18130.0 ms first-token, 2736.35 MB peak RSS, throttled
    false, accuracy `[]`.
- App CLI smoke numbers came from the Task 014 and Task 015 artifacts.
- The 15 t/s target and the scored/non-scored layer split came from `SCORING.md`.
- No accuracy score was invented. No hidden-set performance is claimed.

## Test result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK
```

## Decision

**PASS**

`REPORT.md` now contains the benchmark and submission-path evidence section,
grounded only in the completed Task 014/015/016/017 artifacts and the profiler
JSONs. No accuracy numbers were invented; the app/RAG path is not misrepresented
as improving automated telemetry; telemetry and smoke numbers are reported
accurately; 45/45 tests pass; no metadata/download/model/UI/Yoruba changes.

## Remaining issues and recommended next task

- Throughput (6.12 and 4.38 t/s in profiler runs) remains below the 15 t/s
  target. The model and quantization are locked, so this is bounded by the
  hardware profile unless a future model decision changes.
- Accuracy is still not locally measured (needs `lm_eval` plus the hidden
  validation subset, which is audit-side).
- Recommended **Task 019**: on the official audit environment, install the
  profiler accuracy extra and run the hidden validation subset to capture the
  real Gate-2 accuracy, then finalize submission. No further participant-side
  report or runtime work is required for this documentation task.
