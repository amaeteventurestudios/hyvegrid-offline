# HyveGrid Offline Local Demo Runbook, Task 042A

## Purpose

This runbook provides repeatable local steps for presenting or recording HyveGrid Offline without improvising. It is documentation-only and does not change app behavior, runtime behavior, model behavior, retrieval behavior, language behavior, or submission metadata.

## Demo environment

- Repo: `/Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026`
- Branch: `phase-1-eval-harness`
- Local app URL: `http://127.0.0.1:8000`
- Runtime: local GGUF model through llama.cpp
- App surface: local FastAPI/localhost browser app
- Retrieval: local apiculture notes
- Internet during judged runtime: not required after local setup/model availability

## Pre-demo checklist

- [ ] Laptop has the repo available locally.
- [ ] Local model files are present.
- [ ] llama.cpp `llama-cli` is available and executable.
- [ ] Runtime diagnostics pass.
- [ ] Browser is ready to open `http://127.0.0.1:8000`.
- [ ] Main Hive Health prompt is ready to paste.
- [ ] Site Readiness prompt is ready to paste or narrate.
- [ ] Screen recorder is set to capture the browser and terminal if needed.
- [ ] Presenter is ready to say the safety language.

## Start from a clean terminal

Open a new terminal window. Avoid running unrelated servers on port 8000.

## Enter the repo

Use this exact command:

```bash
cd /Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026
```

## Activate the virtual environment

Use this exact command:

```bash
source .venv/bin/activate
```

If `.venv` is unavailable on the demo machine, use the known project test venv only for checks, not as a new dependency.

## Check local runtime diagnostics

Use this exact command:

```bash
python3 scripts/check_local_runtime.py
```

Successful diagnostics should show:

- a resolved local `llama-cli`
- executable llama.cpp binary
- model files present
- local GGUF path available
- Intel macOS CPU fallback if applicable on the demo machine

Do not add model weights to git. Do not edit runtime files during the demo.

## Start the local app

Use this exact command:

```bash
python -m app.web_app
```

Keep this terminal open while presenting.

## Open the local URL

Open:

```text
http://127.0.0.1:8000
```

The browser should show Mission Control.

## Main demo path: Hive Health Advisor

1. From Mission Control, open Hive Health Advisor.
2. Paste this exact prompt:

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

3. Submit the question.
4. Show the local guidance waiting state.
5. Wait for the answer to return.
6. Show the returned answer.
7. Show retrieved local sources.
8. Show `Completed locally.`
9. Point out cautious language:
   - possible concern
   - check first
   - avoid doing immediately
   - confirm by physical inspection
   - consult an experienced beekeeper or extension officer when needed

Safety line to say:

```text
HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
```

## Second demo path: Site Readiness Advisor

Use this as a short second live run if time allows. Otherwise, narrate it as the second official ADTC prompt path verified in Task 040A.

Prompt:

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

If running live:

1. Open Site Readiness Advisor.
2. Paste the prompt.
3. Submit.
4. Show local waiting state.
5. Show answer, retrieved sources, and `Completed locally.`

If narrating:

```text
This Site Readiness path is the second official prompt path. Final advisor QA verified it completed locally with retrieved sources and Completed locally status.
```

## Language selector check

On Mission Control or an advisor page, show the language selector.

Confirm the selector shows:

- English
- Yorùbá
- Hausa
- Swahili

Confirm it does not show:

- Hausa Preview
- Swahili Preview

Select Hausa on an advisor page and show the human-review-needed note. Select Swahili and show the same kind of note.

Say:

```text
Hausa and Swahili use structured field-template support with human language review recommended before field deployment. They are not claimed as human-reviewed or native-quality.
```

## Offline System Status check

Open or point to Offline System Status.

Confirm the page or panel communicates:

- local app
- local model
- local retrieval
- offline operation
- no cloud access required during the demo

## Successful output should include

A successful live demo should show:

- app running at `http://127.0.0.1:8000`
- Mission Control visible
- five advisor areas visible
- Hive Health Advisor accepts the main ADTC prompt
- local waiting state appears
- answer returns
- retrieved local sources appear
- `Completed locally.` appears
- English remains available as default
- Yorùbá remains available
- Hausa and Swahili show structured field-template support with human-review-needed notes
- Offline System Status shows local runtime positioning
- no cloud service is required during the demo

## Known failure messages and what they mean

### FastAPI import error

Likely message:

```text
ModuleNotFoundError: No module named 'fastapi'
```

Meaning: wrong Python environment.

Action: activate `.venv` or the known test venv.

Known system Python issue:

```text
Bare system Python may fail web tests if FastAPI is not installed. Use the project virtual environment or the known test venv.
```

### Model path or GGUF missing

Likely meaning: model is not present locally or there is a path mismatch.

Action:

- confirm the local model exists in `model/`
- run `python3 scripts/check_local_runtime.py`
- confirm diagnostics pass
- do not add model weights to git

### llama.cpp binary missing or not executable

Likely meaning: local runtime dependency is not available or permission is wrong.

Action:

- run `python3 scripts/check_local_runtime.py`
- check the resolved `llama-cli` path
- check existing setup notes
- do not edit runtime logic during the demo

### Browser cannot connect to localhost

Likely meaning: app is not running or port is unavailable.

Action:

- return to the terminal
- restart `python -m app.web_app`
- reopen `http://127.0.0.1:8000`
- if another server owns port 8000, stop the old server before recording

### Slow first answer

Likely meaning: local GGUF inference can have first-token latency on CPU.

Action:

- keep recording focused
- narrate the waiting state as local guidance being prepared
- wait for answer, retrieved sources, and `Completed locally.`

## Known system Python issue

```text
Bare system Python may fail web tests if FastAPI is not installed. Use the project virtual environment or the known test venv.
```

This is an environment issue, not a demo app behavior issue.

## Before recording

- [ ] Close unrelated browser tabs.
- [ ] Make browser zoom readable.
- [ ] Open terminal in the repo.
- [ ] Activate `.venv`.
- [ ] Run runtime diagnostics.
- [ ] Start app.
- [ ] Open `http://127.0.0.1:8000`.
- [ ] Keep prompts ready.
- [ ] Keep backup narration ready for slow inference.

## Evidence files and artifacts

Useful evidence to mention if asked:

- `REPORT.md`
- `artifacts/eval/local-runtime-success-answer-guard-task-038D.md`
- `artifacts/eval/african-language-browser-qa-task-039D.md`
- `artifacts/eval/final-advisor-flow-qa-task-040A.md`
- `artifacts/eval/report-final-update-task-041A.md`

## Stop the app

In the terminal running the app, press:

```text
Control-C
```

Then confirm the terminal returns to the shell prompt.

## Acceptance checklist

- [ ] `cd /Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026` documented.
- [ ] `source .venv/bin/activate` documented.
- [ ] `python3 scripts/check_local_runtime.py` documented.
- [ ] `python -m app.web_app` documented.
- [ ] `http://127.0.0.1:8000` documented.
- [ ] Main Hive Health prompt included exactly.
- [ ] Site Readiness prompt included exactly.
- [ ] Five advisor areas covered.
- [ ] Language selector covered.
- [ ] Hausa and Swahili human-review-needed notes covered.
- [ ] Offline System Status covered.
- [ ] Retrieved local sources covered.
- [ ] `Completed locally.` covered.
- [ ] Field guidance and not certified diagnosis language included.
- [ ] No cloud, external API, live sensor, real-time sensor, autonomous agent, or digital twin claim included.
