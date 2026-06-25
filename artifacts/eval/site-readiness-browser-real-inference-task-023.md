# Site Readiness Browser Real Inference (Task 023)

1. **Task title and date:** Capture one real Site Readiness browser inference
   smoke test as demo evidence. Date: 2026-06-24.

## Starting commit

- `778be0859fae1279c262318d6d84be41b54d2b29`

## Branch

- `phase-1-eval-harness`

## Scope

Prove the full local browser path works end to end for the Site Readiness Advisor
with the real Granite model: browser form / HTTP POST to FastAPI to
`answer_question()` to SQLite FTS5 retrieval to prompt builder to llama.cpp to
Granite GGUF to cleaned answer to retrieved sources rendered on the page.
Evidence capture only; no other advisor is wired and no code is changed.

## Files inspected

- `app/web_app.py` (shared advisor config + `_submit_advisor_question`)
- `app/templates/advisor_form.html`
- `app/llama_runtime.py` (`answer_question`, model path, cleanup)
- `app/retrieval.py`, `app/prompt_builder.py`
- `artifacts/eval/site-readiness-web-advisor-task-022.md`,
  `artifacts/eval/hive-health-browser-real-inference-task-021.md`

## Files changed, if any

None. Evidence capture only. No source, config, model, metadata, download,
profiler, or test files were modified. The only output is this artifact (itself
untracked until a later commit).

## Preflight checks

- Model file present: `model/granite-3.3-2b-instruct-q4_k_m.gguf` (symlink to
  `model-candidates/granite-3.3-2b-instruct-Q4_K_M.gguf`). OK.
- llama.cpp binary present: `/home/amaete/llama.cpp/build/bin/llama-cli`. OK.
- Knowledge DB present: `data/knowledge/knowledge.db` (92 KB). OK.
- Memory: ~6.7 GB total, ~5.8 GB available at start (the app path pages against
  swap; expect minutes, not seconds).
- Existing tests: `python3 -m unittest tests/test_retrieval.py
  tests/test_prompt_builder.py tests/test_llama_runtime.py` ran 45 tests, OK.
- Web tests: `python3 -m unittest tests/test_web_app.py` ran 20 tests, OK.

## Server command used

```
python3 -m app.web_app > /tmp/hyvegrid-task023-web.log 2>&1 &
```

Bound to `http://127.0.0.1:8000`.

## GET route check result

```
curl -s -o /tmp/task023-get.html -w "%{http_code}" http://127.0.0.1:8000/advisor/site-readiness
```

- HTTP 200.
- The body contained "Site Readiness Advisor" and a `<form`. The form page
  rendered correctly (no model load on GET).

## POST command used

```
curl -sS -X POST \
  --data-urlencode 'question=An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?' \
  http://127.0.0.1:8000/advisor/site-readiness \
  -o /tmp/task023-site-readiness-result.html
```

Timed with `/usr/bin/time`. Wall time was captured separately.

## Real inference result table

| Metric | Value |
|---|---|
| Wall time (POST) | 263.71 s (~4.4 min) |
| curl exit code | 0 |
| HTTP status (server log) | 200 OK |
| Answer rendered | yes |
| Sources rendered | yes |
| Top source | site_readiness.md / Avoid doing immediately |
| Output clean (no chrome, no prompt echo) | yes |
| Truncated | no (all five sections present, including "When to escalate") |
| Server errors | no (no 500, no exception, no traceback in log) |
| Completed locally (model + RAG) | yes |

The result HTML was ~4.7 KB and contained "Site Readiness Advisor",
"Completed locally.", "Possible concern", "Check first", "Avoid doing
immediately", "Suggested next step", "When to escalate", "Retrieved sources", and
"site_readiness.md". It did NOT contain "Loading model", "available commands",
"build :", "modalities :", "Exiting...", "llama_model_loader", "system_info", the
"[ Prompt: ... ]" timing line, any echoed prompt block, any raw stdout, or any
traceback.

## Short sanitized answer excerpt

The rendered answer followed the required five-section format and stayed cautious
and grounded in the site/forage notes. Paraphrased excerpt (verbatim phrases
trimmed):

- "1. Possible concern: The proposed site may pose a risk due to the
  concentration of crops (cassava, mango, pepper, and vegetables) which could
  lead to crop dependence risk ..."
- "2. Check first: Conduct a thorough inspection of the local flowering calendar
  to understand the blooming periods ... and identify any potential seasonal
  forage [gaps] ..."
- "3. Avoid doing immediately: Avoid placing 20 hives near these concentrated
  crop areas to prevent over-reliance on a single food source and reduce
  competition among coloni[es] ..."
- (Sections 4 "Suggested next step" and 5 "When to escalate" were also present.)

Full answer length was about 1600 characters. The page also showed the
"Completed locally." label.

## Retrieved sources excerpt

Rendered in order under "Retrieved sources":

- site_readiness.md / Avoid doing immediately
- forage_pollination.md / Key checks
- forage_pollination.md / Check first
- site_readiness.md / Possible concern
- site_readiness.md / Key checks

`site_readiness.md` is present (top source), as required.

## Test command and result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK

python3 -m unittest tests/test_web_app.py
Ran 20 tests ... OK
```

Total: 65/65 pass (preflight). No tests were added or changed for this task.

## Confirmation of no changes

- No `metadata.json` change.
- No `download_model.sh` change.
- No model files, `model.gguf`, or anything under `model/` touched.
- No profiler artifact changes (read only).
- No Yoruba added.
- No Guided Hive Walkthrough added.
- No cloud/API runtime dependency added (FastAPI serves localhost; the answer path
  is the existing local llama.cpp run).
- No code changes at all (evidence capture only).

## Decision

**PASS**

The full local browser path worked end to end for the Site Readiness Advisor with
the real Granite model: a POST to `/advisor/site-readiness` returned HTTP 200 in
~263.7 s, rendered the real cautious five-section answer and the retrieved
sources (top: site_readiness.md, with forage_pollination.md also present), with
no llama.cpp chrome, no prompt echo, no raw stdout, and no stack trace. The
server log showed a clean 200 with no errors. Preflight tests pass (65/65). No
code or config was changed.

## Remaining issues and recommended next task

- Wall time (~4.4 min for one answer) is dominated by model load and swap paging
  on the 6.7 GB VM; consistent with Tasks 021 (Hive Health, ~3.9 min) and
  014/015. Fine for a demo, not interactive.
- Hive Health and Site Readiness are wired and proven with real model inference;
  harvest-quality, forage-pollination, and hive-signals remain placeholders.
- Recommended **Task 024**: wire the next advisor (for example, Harvest Quality
  Coach) using the shared advisor template/helper introduced in Task 022 (now a
  small config + test addition), and/or assemble a short demo script/video note
  referencing the Task 021 and Task 023 real-inference evidence.
