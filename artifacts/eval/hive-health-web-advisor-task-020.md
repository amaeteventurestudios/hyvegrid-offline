# Hive Health Web Advisor (Task 020)

1. **Task title and date:** Wire the Hive Health Advisor screen to the existing
   offline answer path. Date: 2026-06-24.

## Starting commit

- `8e151360942ef67b57290b95692759f895008a15`

## Branch

- `phase-1-eval-harness`

## Scope

Make the Hive Health Advisor usable from the local browser UI. A user types an
English hive-health question, submits it, and sees a real answer produced through
the existing local HyveGrid offline path (`app.llama_runtime.answer_question`).
Only Hive Health is wired; the other advisors remain placeholders.

## Files inspected

- `app/web_app.py`
- `app/templates/advisor.html`, `index.html`, `status.html`, `base.html`
- `app/static/style.css`
- `app/llama_runtime.py` (the `answer_question` signature and return shape)
- `tests/test_web_app.py`
- `artifacts/eval/local-web-ui-skeleton-task-019.md`

## Files changed

- `app/web_app.py` (modified)
  - Imported `answer_question` from `app.llama_runtime`.
  - Added Hive Health constants (example prompt, helper text, validation and
    safe-error messages) and a shared context helper.
  - Added `GET /advisor/hive-health` (renders the form, no model load) and
    `POST /advisor/hive-health` (runs the answer path). Both are registered
    before the generic `/advisor/{slug}` route so they take precedence.
- `app/templates/hive_health.html` (new) - the form + result/error template.
- `app/static/style.css` (modified) - styles for the form, answer (pre-wrap),
  sources, validation, and error states.
- `tests/test_web_app.py` (modified) - six new Hive Health tests (mocked).
- `artifacts/eval/hive-health-web-advisor-task-020.md` (this artifact)

No new dependencies were added. The form body is parsed with the standard
library `urllib.parse`, so `python-multipart` is not required.

## Routes added or updated

- `GET /advisor/hive-health` (new) - renders the Hive Health Advisor form.
- `POST /advisor/hive-health` (new) - validates input and runs the offline
  answer path.
- Existing routes (`/`, `/status`, `/advisor/{slug}`, `/health`) are unchanged.
  The generic `/advisor/{slug}` still serves placeholder pages for the other
  four advisors (site-readiness, harvest-quality, forage-pollination,
  hive-signals).

## How the Hive Health Advisor form works

`GET /advisor/hive-health` renders a page with:

- Title "Hive Health Advisor".
- Helper text: the answer runs locally through the Granite model and the public
  apiculture knowledge base; no cloud access.
- A reminder that HyveGrid is a field triage assistant, not a certified disease
  diagnosis tool.
- A `<form method="post">` with a `<textarea name="question">` and an "Ask
  locally" submit button.
- An "Example prompt" block (the official hive-health prompt) shown as text in a
  `<details>` element. It is displayed only; it does not run automatically.

`POST /advisor/hive-health` parses the urlencoded body, trims the question, and
either re-renders the page with a validation message (empty input) or runs the
answer path and re-renders with the answer, retrieved sources, and a "Completed
locally." label.

## How answer_question() is used

The handler calls the existing `answer_question(question)` from
`app.llama_runtime` without duplicating retrieval, prompt building, llama.cpp
execution, or output cleanup. Because that call blocks for the model load and
generation (minutes on this VM), it is run off the event loop with
`asyncio.to_thread(answer_question, question)` so the server stays responsive.
No cloud service is called.

The returned bundle is treated as success only when `runtime.returncode == 0`,
not timed out, and the answer is non-empty; otherwise the safe error message is
shown. Raw stdout, prompt text, and internal command details are never rendered.

## How errors are handled

- Empty question: a friendly validation message ("Please enter a hive-health
  question before submitting.") is shown and `answer_question` is not called.
- `answer_question()` raises, returns a non-zero/timed-out runtime, or returns
  an empty answer: the page shows "HyveGrid could not complete this local
  answer. Confirm the model is downloaded and llama.cpp is available, then try
  again." No stack traces or internal details are exposed to the user.

## How sources are displayed

When an answer is shown, the retrieved sources are listed in order, each as
`source_file . heading`, for example `hive_health.md . Avoid doing immediately`
and `site_readiness.md . Check first`. Only the source file and heading are
shown; full knowledge chunks are not dumped.

## Confirmation of boundaries

- No model files, `model.gguf`, or anything under `model/` touched.
- No `metadata.json` change.
- No `download_model.sh` change.
- No profiler artifact changes (read only).
- No cloud/API runtime dependency added (FastAPI serves localhost; the answer
  path is the existing local llama.cpp run).
- No `requirements.txt` change (no new dependency).
- No Yoruba added.
- Only Hive Health wired; other advisors remain placeholders.
- `app/retrieval.py`, `app/prompt_builder.py`, `app/llama_runtime.py` unchanged.

## Test command and result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK

python3 -m unittest tests/test_web_app.py
Ran 15 tests ... OK
```

Total: 60/60 pass. The web tests monkeypatch `app.web_app.answer_question` (no
GGUF load, no llama.cpp call) and cover: GET form 200; POST valid calls the mock
and shows the answer; sources are displayed; empty input shows validation and
does not call the mock; an exception from the mock shows the safe error and does
not leak the internal detail or any traceback; and other advisors remain
placeholders. Existing Task 019 route tests still pass.

## Smoke check command and result

```
python3 -m app.web_app   # started on 127.0.0.1:8000, then stopped
curl http://127.0.0.1:8000/advisor/hive-health
```

- `GET /advisor/hive-health` -> HTTP 200, and the body contains "Hive Health
  Advisor", a `<form`, `name="question"`, the example prompt, the not-a-diagnosis
  reminder, and the "Ask locally" button. No "Completed locally." block on GET.
- `GET /advisor/site-readiness` -> placeholder text intact (other advisors not
  wired).
- `GET /` -> HTTP 200 (Mission Control unchanged).
- No real model inference was run for this smoke check, per the task (route/form
  only). The server was stopped after the check; port 8000 is free.

## Decision

**PASS**

`GET /advisor/hive-health` shows a usable English form; `POST` calls the existing
`answer_question()` for valid questions and renders the answer and retrieved
sources; empty input is validated without calling the model; runtime errors show
a safe message with no stack trace; 60/60 tests pass; the route/form smoke check
passed; no model/metadata/download/profiler/requirements/cloud/Yoruba changes;
no other advisor wired.

## Remaining issues and recommended next task

- A real end-to-end browser answer (user submits, waits minutes, sees a Granite
  answer) was intentionally not run here; it would take several minutes per
  question on this VM. The path is the same one validated in Tasks 014/015.
- The other four advisors are still placeholders.
- Recommended **Task 021**: either (a) run one real Hive Health answer through
  the browser to capture demo evidence, or (b) wire the next advisor (for
  example, Site Readiness Advisor) using the same pattern, factoring the shared
  form/POST logic if a second advisor makes that worthwhile.
