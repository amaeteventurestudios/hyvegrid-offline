# Site Readiness Web Advisor (Task 022)

1. **Task title and date:** Wire the Site Readiness Advisor screen to the existing
   offline answer path. Date: 2026-06-24.

## Starting commit

- `e713da3640bfa19519725629d6cbac31ce6fc724`

## Branch

- `phase-1-eval-harness`

## Scope

Make the Site Readiness Advisor usable from the local browser UI. A user types an
English site-readiness / apiary-siting question, submits it, and sees an answer
through the existing local HyveGrid offline path (`app.llama_runtime.answer_question`).
Only Site Readiness is wired; Hive Health remains wired; the other advisors stay
placeholders. Mocked tests only; no real model inference in this task.

## Files inspected

- `app/web_app.py`
- `app/templates/hive_health.html`, `advisor.html`, `index.html`, `base.html`
- `app/static/style.css`
- `tests/test_web_app.py`
- `artifacts/eval/hive-health-web-advisor-task-020.md`,
  `artifacts/eval/hive-health-browser-real-inference-task-021.md`

## Files changed

- `app/web_app.py` (modified)
  - Replaced the Hive-Health-only constants/handlers with data-driven advisor
    configs (`HIVE_HEALTH`, `SITE_READINESS`), a shared `_advisor_context()`, and a
    shared `_submit_advisor_question()` POST helper.
  - Added `GET /advisor/site-readiness` and `POST /advisor/site-readiness`.
  - Migrated Hive Health to the same shared template/helper (output unchanged).
- `app/templates/advisor_form.html` (new) - shared, parameterized advisor form
  template used by both wired advisors.
- `app/templates/hive_health.html` (deleted) - replaced by the shared template.
- `tests/test_web_app.py` (modified) - five new Site Readiness tests and an updated
  placeholder test (now checks the three still-unwired advisors).
- `artifacts/eval/site-readiness-web-advisor-task-022.md` (this artifact)

No new dependency was added (the form body is parsed with the standard library
`urllib.parse`).

## Routes added or updated

- `GET /advisor/site-readiness` (new) - renders the Site Readiness Advisor form.
- `POST /advisor/site-readiness` (new) - validates input and runs the offline
  answer path.
- `GET /advisor/hive-health` and `POST /advisor/hive-health` updated to use the
  shared template/helper; behavior and output are unchanged.
- Existing routes (`/`, `/status`, `/advisor/{slug}` placeholders, `/health`)
  unchanged. The generic `/advisor/{slug}` still serves placeholder pages for
  harvest-quality, forage-pollination, and hive-signals.

## How the Site Readiness Advisor form works

`GET /advisor/site-readiness` renders a page with:

- Title "Site Readiness Advisor".
- Helper text: the answer runs locally through the Granite model and the public
  apiculture knowledge base; no cloud access.
- A page note: "Local and offline. HyveGrid is a field tool, not a certified site
  approval tool."
- A `<form method="post">` with a `<textarea name="question">` and an "Ask
  locally" submit button.
- An "Example prompt" block (the official site-readiness prompt) shown as text in
  a `<details>` element. Displayed only; not auto-run.

`POST /advisor/site-readiness` parses the urlencoded body, trims the question,
and either re-renders with a validation message (empty input) or runs the answer
path and re-renders with the answer, retrieved sources, and a "Completed
locally." label.

## How answer_question() is used

The shared `_submit_advisor_question()` calls the existing `answer_question(
question)` from `app.llama_runtime` without duplicating retrieval, prompt
building, llama.cpp execution, or output cleanup. Because that call blocks for
model load and generation, it is run off the event loop with
`asyncio.to_thread(answer_question, question)` so the server stays responsive.
No cloud service is called. Success requires `runtime.returncode == 0`, not
timed out, and a non-empty answer; otherwise the safe error is shown.

## How errors are handled

- Empty question: "Please enter a site-readiness question before submitting."
  `answer_question` is not called.
- `answer_question()` raises, returns a non-zero/timed-out runtime, or an empty
  answer: "HyveGrid could not complete this local site-readiness answer. Confirm
  the model is downloaded and llama.cpp is available, then try again." No stack
  traces or internal details are exposed.

## How sources are displayed

When an answer is shown, retrieved sources are listed in order, each as
`source_file . heading`, for example `site_readiness.md . Check first` and
`forage_pollination.md . Key checks`. Only the source file and heading are shown.

## Confirmation of boundaries

- No model files, `model.gguf`, or anything under `model/` touched.
- No `metadata.json` change.
- No `download_model.sh` change.
- No profiler artifact changes.
- No cloud/API runtime dependency added (FastAPI serves localhost; the answer path
  is the existing local llama.cpp run).
- No Guided Hive Walkthrough added.
- No Yoruba added.
- No new dependency (`requirements.txt` unchanged).
- Only Hive Health and Site Readiness are wired; harvest-quality,
  forage-pollination, and hive-signals remain placeholders.
- `app/retrieval.py`, `app/prompt_builder.py`, `app/llama_runtime.py` unchanged.

## Test command and result

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK

python3 -m unittest tests/test_web_app.py
Ran 20 tests ... OK
```

Total: 65/65 pass. Web tests monkeypatch `app.web_app.answer_question` (no GGUF
load, no llama.cpp call) and cover for Site Readiness: GET form 200; POST valid
calls the mock and shows the answer; sources displayed; empty input shows
validation and does not call the mock; a mock exception shows the site-readiness
safe error with no stack trace. Hive Health tests still pass after the shared
template migration, and the three unwired advisors are confirmed as placeholders.

## Smoke check command and result

```
python3 -m app.web_app   # started on 127.0.0.1:8000, then stopped
curl http://127.0.0.1:8000/advisor/site-readiness
```

- `GET /advisor/site-readiness` -> HTTP 200; body contains "Site Readiness
  Advisor", a `<form`, `name="question"`, the example prompt, the
  "not a certified site approval tool" note, and the "Ask locally" button. No
  "Completed locally." block on GET.
- `GET /advisor/hive-health` -> HTTP 200 (still works).
- `GET /advisor/forage-pollination` -> placeholder text intact.
- `GET /` -> HTTP 200.
- No real model inference was run for this smoke check, per the task (route/form
  only). The server was stopped; port 8000 is free.

## Decision

**PASS**

`GET /advisor/site-readiness` shows a usable English form; `POST` calls the
existing `answer_question()` for valid questions and renders the answer and
sources; empty input is validated without calling the model; runtime errors show
a safe message with no stack trace; Hive Health still works after the shared
template refactor; the other advisors remain placeholders; 65/65 tests pass; the
route/form smoke check passed. No metadata/download/model/profiler/requirements/
cloud/Yoruba/Guided-Hive-Walkthrough changes.

## Remaining issues and recommended next task

- A real end-to-end Site Readiness browser answer was not run here (mocked tests
  + route check only, per the task). The path is the same one proven with real
  Granite in Task 021 for Hive Health.
- harvest-quality, forage-pollination, and hive-signals are still placeholders.
- Recommended **Task 023**: either (a) capture one real Site Readiness browser
  answer as demo evidence (mirroring Task 021), or (b) wire the next advisor
  using the now-shared form/helper/template, which makes adding an advisor a
  small config + test addition.
