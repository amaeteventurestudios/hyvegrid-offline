# English Advisors Completion (Task 024)

- **Task name and date:** Wire the remaining English advisor screens (Harvest
  Quality Coach, Forage and Pollination Guide, Hive Signal Check) using the
  existing shared advisor template/helper. Date: 2026-06-25.
- **Starting branch:** `phase-1-eval-harness`
- **Starting HEAD:** `9f957f24c2ca89a8b5c87b5fc05b5e57cb1d4548`
- **Working tree started clean:** yes (confirmed before editing; `git status
  --short` was empty, branch and HEAD matched the expected values).

## Scope

Wire the three remaining advisors to the existing offline answer path
(`app.llama_runtime.answer_question`) by reusing the shared `advisor_form.html`
template and the shared `_submit_advisor_question()` helper introduced in Task
022. No new architecture. Mocked tests only; no real model inference.

## Routes added

All six new routes reuse the shared GET/POST pattern and are registered before the
generic `/advisor/{slug}` route so they take precedence:

- `GET /advisor/harvest-quality`, `POST /advisor/harvest-quality`
- `GET /advisor/forage-pollination`, `POST /advisor/forage-pollination`
- `GET /advisor/hive-signal`, `POST /advisor/hive-signal`

Note on the Hive Signal slug: the Mission Control card previously used the slug
`hive-signals` (plural), but the required route is `/advisor/hive-signal`
(singular). The ADVISORS slug was changed from `hive-signals` to `hive-signal` so
the card links to the wired route. (Hive Health and Site Readiness already used
slugs matching their routes.)

Each wired advisor now: renders a form with helper text and an example prompt (not
auto-run); validates empty input (no model call); runs `answer_question()` off the
event loop via `asyncio.to_thread`; renders the answer and retrieved sources; and
shows a safe, advisor-specific error if `answer_question()` fails or returns a
non-zero/timed-out/empty result. Raw stdout, prompt echo, command details,
exception text, and stack traces are never rendered.

## Tests added or updated

`tests/test_web_app.py`:
- Removed `test_other_advisors_remain_placeholders` (no advisors are placeholders
  anymore).
- Added `test_all_advisors_are_wired` (all five advisors return 200 with a form).
- Added a shared `_assert_wired_advisor(slug, question, source_file, marker)`
  helper that checks, per advisor: GET renders the form (no answer); POST valid
  calls mocked `answer_question` once with the question and renders the answer
  marker, "Completed locally.", and the expected source file; empty input shows
  validation and does not call the mock; a raised exception shows a safe error
  with no leaked exception text or traceback.
- Added three tests using that helper:
  `test_harvest_quality_advisor_wired` (source `harvest_quality.md`),
  `test_forage_pollination_advisor_wired` (source `forage_pollination.md`),
  `test_hive_signal_advisor_wired` (source `hive_signals.md`).

Existing Hive Health, Site Readiness, Mission Control, Offline System Status,
`/health`, and unknown-slug-404 tests remain unchanged and still pass.

## Test command run

pytest is not installed in this environment, so the established unittest command
was used (matching prior tasks):

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
python3 -m unittest tests/test_web_app.py
```

`python3 -m py_compile app/web_app.py tests/test_web_app.py` was also run (OK).

A brief live GET smoke (no inference) confirmed the server boots and the three new
routes return HTTP 200 with a form and example prompt; the Mission Control Hive
Signal card now links to `/advisor/hive-signal`.

## Test result

- Retrieval + prompt builder + llama runtime: 45 tests, OK.
- Web app: 23 tests, OK.
- Total: 68/68 pass.

## Confirmation that no real model inference was run

Confirmed. All web tests monkeypatch `app.web_app.answer_question`, so no GGUF
model is loaded and llama.cpp is never called. The live smoke used only GET routes
(forms), which do not run inference.

## Confirmation that no Yoruba or Guided Hive Walkthrough work was added

Confirmed. English only. No Yoruba and no Guided Hive Walkthrough were added.

## Confirmation of no other changes

No changes to `metadata.json`, `download_model.sh`, model files / `model/`,
profiler artifacts, `app/retrieval.py`, `app/prompt_builder.py`, or
`app/llama_runtime.py`. No cloud/API/external-service/network dependency was
added. No new dependency was added (the form is still parsed with the standard
library `urllib.parse`; `requirements.txt` unchanged). The only code changes are
in the web app (`app/web_app.py`) and its tests.

## Files changed

- `app/web_app.py` (modified): added three example-prompt constants, three advisor
  config dicts (`HARVEST_QUALITY`, `FORAGE_POLLINATION`, `HIVE_SIGNAL`), six
  GET/POST route handlers, and changed the Hive Signal slug to `hive-signal`.
- `tests/test_web_app.py` (modified): replaced the placeholder test with
  all-advisors-wired coverage and three new advisor tests via a shared helper.
- `artifacts/eval/english-advisors-completion-task-024.md` (new; this artifact).

## Notes / risks

- All five advisors now share one template and one POST helper; adding a future
  advisor is a small config + test addition.
- A real end-to-end browser answer for the three new advisors was intentionally
  not run (mocked tests + GET smoke only). The underlying path is the same one
  proven with real Granite for Hive Health (Task 021) and Site Readiness
  (Task 023).
- The generic `/advisor/{slug}` route and `advisor.html` template remain for
  handling unknown slugs (404); no known advisor renders the placeholder anymore.
