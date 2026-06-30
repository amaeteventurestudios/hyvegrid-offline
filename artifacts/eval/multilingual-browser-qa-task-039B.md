# Task 039B Multilingual Browser QA Audit

## Current Commit Reviewed

```text
541b6fe3e82863f33ac4ee0c8f243e2ac08e92f9
Add multilingual scaffold Task 039A
```

## Browser Method Used

Started the local FastAPI app with the existing preview virtual environment:

```bash
/tmp/hyvegrid-task-034b-test-venv/bin/python -m uvicorn app.web_app:app --host 127.0.0.1 --port 8020
```

The in-app browser was opened against the local app. Browser automation setup
succeeded, but repeated Playwright navigation/evaluation calls timed out in the
browser-control session, so route assertions were completed against the running
local web app using Python standard-library HTTP reads. The server logs confirm
the pages were rendered by the app process, and one real default-English advisor
POST completed locally through the runtime path.

No screenshot artifact was created because the browser-control session timed out
before a stable screenshot capture. No screenshot dependency was added.

## Routes And Pages Inspected

- `/`
- `/advisor/hive-health`
- `/?lang=yo`
- `/advisor/hive-health?lang=yo`
- `/?lang=ha`
- `/advisor/hive-health?lang=ha`
- `/?lang=sw`
- `/advisor/hive-health?lang=sw`

## Language Options Observed

The shared language selector exposed:

- `English`
- `Yorùbá`
- `Hausa Preview`
- `Swahili Preview`

## English QA Result

- English remains the default route.
- Mission Control rendered successfully.
- Hive Health Advisor rendered successfully.
- Field labels and the local guidance waiting state were readable.
- No preview limitation note appeared for English.
- A real default-English Hive Health Advisor form POST completed locally.
- The result included `Completed locally`.
- Retrieved sources were displayed, including `hive_health.md`.
- No local runtime error appeared.

## Yorùbá QA Result

- Yorùbá option appears in the shared selector.
- Yorùbá remains the primary African language layer.
- Yorùbá labels, templates, review note, and glossary support still render where
  implemented.
- Yorùbá did not regress into a preview-only state.
- `/advisor/hive-health?lang=yo` rendered without crashing and showed the local
  guidance waiting state.

## Hausa Preview QA Result

- Hausa appears as `Hausa Preview`.
- Preview limitation note is visible:

```text
Hausa preview. Key field guidance is structured, but full Hausa language review is still needed.
```

- The page does not claim full Hausa support.
- The page does not claim human-reviewed Hausa.
- The page does not ask the local model to freestyle full Hausa translation.
- `/advisor/hive-health?lang=ha` rendered without crashing and showed the local
  guidance waiting state.

## Swahili Preview QA Result

- Swahili appears as `Swahili Preview`.
- Preview limitation note is visible:

```text
Swahili preview. Key field guidance is structured, but full Swahili language review is still needed.
```

- The page does not claim full Swahili support.
- The page does not claim human-reviewed Swahili.
- The page does not ask the local model to freestyle full Swahili translation.
- `/advisor/hive-health?lang=sw` rendered without crashing and showed the local
  guidance waiting state.

## Field-Safety Wording

Rendered language surfaces preserved cautious field wording, including:

- possible concern
- check first
- avoid doing immediately
- confirm by physical inspection
- consult an experienced beekeeper or extension officer when needed

No inspected rendered page introduced these avoided terms:

- guaranteed diagnosis
- digital twin
- autonomous agents
- live sensor simulation
- real-time sensor readings

## Advisor Submission Result

A real POST to `/advisor/hive-health` was submitted through the running local app
with the default English flow. Result:

```text
Completed locally: True
Retrieved sources: True
Runtime error: False
Answer marker: True
```

## Tests Run

Prompt builder tests:

```text
python3 -m unittest tests.test_prompt_builder
Ran 17 tests in 0.032s
OK
```

Bare system Python web command:

```text
python3 -m unittest tests.test_web_app
```

Result: failed before tests ran because the system Python environment does not
have `fastapi` installed.

Focused web suite in the project preview venv:

```text
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app
Ran 43 tests in 0.635s
OK
```

## Visual Or Text Issues Found

- No blocking visual or text issue was found in the inspected routes.
- The only tooling issue was browser-control timeout during automated DOM reads;
  the app itself rendered the inspected routes and completed the default advisor
  submission.

## Files Changed

- `artifacts/eval/multilingual-browser-qa-task-039B.md`

## Confirmations

- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- No runtime path files were changed.
- No cloud API, CDN, Phaser, WebGL, canvas, Remotion, remote asset, external
  runtime dependency, generated art, or animation was added.
- Hausa remains preview only.
- Swahili remains preview only.

## Final Status

MULTILINGUAL_BROWSER_QA_READY
