# Hive Health Browser Real Inference (Task 021)

1. **Task title and date:** Capture one real Hive Health browser inference smoke
   test as demo evidence. Date: 2026-06-24.

## Starting commit

- `f7a81df74e55e68a04e213222a3c1ab9908efe0a`

## Branch

- `phase-1-eval-harness`

## Scope

Prove the full local browser path works end to end with the real Granite model:
browser form / HTTP POST to FastAPI to `answer_question()` to SQLite FTS5
retrieval to prompt builder to llama.cpp to Granite GGUF to cleaned answer to
retrieved sources rendered on the page. Evidence capture only; no other advisor
is wired and no code is changed.

## Files inspected

- `app/web_app.py` (POST handler, context, template wiring)
- `app/templates/hive_health.html`
- `app/llama_runtime.py` (`answer_question`, model path, cleanup)
- `app/retrieval.py`, `app/prompt_builder.py`
- `artifacts/eval/hive-health-web-advisor-task-020.md`

## Files changed, if any

None. This task is evidence capture only. No source, config, model, metadata,
download, profiler, or test files were modified. The only output is this artifact
(itself untracked until a later commit).

## Preflight checks

- Model file present: `model/granite-3.3-2b-instruct-q4_k_m.gguf` (symlink to
  `model-candidates/granite-3.3-2b-instruct-Q4_K_M.gguf`). OK.
- llama.cpp binary present: `/home/amaete/llama.cpp/build/bin/llama-cli`. OK.
- Knowledge DB present: `data/knowledge/knowledge.db` (92 KB). OK.
- Memory: ~6.7 GB total, ~5.6 GB available at start (the app path pages against
  swap; expect minutes, not seconds).
- Existing tests: `python3 -m unittest tests/test_retrieval.py
  tests/test_prompt_builder.py tests/test_llama_runtime.py` ran 45 tests, OK.
- Web tests: `python3 -m unittest tests/test_web_app.py` ran 15 tests, OK.

## Server command used

```
python3 -m app.web_app > /tmp/hyvegrid-task021-web.log 2>&1 &
```

Bound to `http://127.0.0.1:8000`.

## GET route check result

```
curl -s -o /tmp/task021-get.html -w "%{http_code}" http://127.0.0.1:8000/advisor/hive-health
```

- HTTP 200.
- The body contained "Hive Health Advisor" and a `<form`. The form page rendered
  correctly (no model load on GET).

## POST command used

```
curl -sS -X POST \
  --data-urlencode 'question=A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?' \
  http://127.0.0.1:8000/advisor/hive-health \
  -o /tmp/task021-hive-health-result.html
```

Timed with `/usr/bin/time`. Wall time was captured separately.

## Real inference result table

| Metric | Value |
|---|---|
| Wall time (POST) | 232.88 s (~3.9 min) |
| curl exit code | 0 |
| HTTP status (server log) | 200 OK |
| Answer rendered | yes |
| Sources rendered | yes |
| Top source | hive_health.md / Avoid doing immediately |
| Output clean (no chrome, no prompt echo) | yes |
| Truncated | no (all five sections present, including "When to escalate") |
| Server errors | no (no 500, no exception, no traceback in log) |
| Completed locally (model + RAG) | yes |

The result HTML was ~4.7 KB and contained "Hive Health Advisor",
"Completed locally.", "Possible concern", "Check first", "Avoid doing
immediately", "Suggested next step", "When to escalate", "Retrieved sources", and
"hive_health.md". It did NOT contain "Loading model", "available commands",
"build :", "modalities :", "Exiting...", "llama_model_loader", "system_info", the
"[ Prompt: ... ]" timing line, any echoed prompt block, any raw stdout, or any
traceback.

## Short sanitized answer excerpt

The rendered answer followed the required five-section format and stayed cautious
and grounded in the notes. Paraphrased excerpt (verbatim phrases trimmed):

- "1. Possible concern: The beekeeper should be cautious ... low hive activity,
  ants near the hive stand, partially capped brood ..."
- "2. Check first: ... confirm by physical inspection before drawing conclusions
  ... check whether the entrance is blocked ..."
- "3. Avoid doing immediately: ... avoid harvesting honey from this weak or
  stressed colony ... Splitting, ..."
- (Sections 4 "Suggested next step" and 5 "When to escalate" were also present.)

Full answer length was about 1707 characters. The page also showed the
"Completed locally." label.

## Retrieved sources excerpt

Rendered in order under "Retrieved sources":

- hive_health.md / Avoid doing immediately
- site_readiness.md / Check first
- hive_health.md / Check first
- hive_health.md / Possible concern
- site_readiness.md / Avoid doing immediately

## Test command and result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK

python3 -m unittest tests/test_web_app.py
Ran 15 tests ... OK
```

Total: 60/60 pass (preflight). No tests were added or changed for this task.

## Confirmation of no changes

- No `metadata.json` change.
- No `download_model.sh` change.
- No model files, `model.gguf`, or anything under `model/` touched.
- No profiler artifact changes (read only).
- No Yoruba added.
- No cloud/API runtime dependency added (FastAPI serves localhost; the answer path
  is the existing local llama.cpp run).
- No code changes at all (evidence capture only).

## Decision

**PASS**

The full local browser path worked end to end with the real Granite model: a POST
to `/advisor/hive-health` returned HTTP 200 in ~232.9 s, rendered the real
cautious five-section answer and the retrieved sources (top: hive_health.md), with
no llama.cpp chrome, no prompt echo, no raw stdout, and no stack trace. The server
log showed a clean 200 with no errors. Preflight tests pass (60/60). No code or
config was changed.

## Remaining issues and recommended next task

- Wall time (~3.9 min for one answer) is dominated by model load and swap paging
  on the 6.7 GB VM; this is expected and consistent with Tasks 014/015. It is fine
  for a demo but not interactive.
- Only Hive Health is wired; the other advisors are still placeholders.
- Recommended **Task 022**: either (a) capture a second real browser answer for a
  different concern to strengthen demo evidence, or (b) wire the next advisor
  (for example, Site Readiness Advisor) using the same form/POST pattern now that
  the path is proven end to end.
