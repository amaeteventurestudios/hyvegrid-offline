# Task 031E Advisor Waiting Walkthrough Animation Evidence

Date/time: 2026-06-25T22:31:32-0700

Starting commit: `8786b8975a89b3d5b4e2b3ed8f612aa477e65026`

## Task Name

Task 031E: Advisor Waiting Walkthrough Animation.

## Files Changed

- `app/web_app.py`
- `app/templates/advisor_form.html`
- `app/static/style.css`
- `tests/test_web_app.py`
- `artifacts/eval/advisor-waiting-walkthrough-animation-task-031E.md`

## Advisor Pages Affected

- Hive Health Advisor
- Site Readiness Advisor
- Harvest Quality Coach
- Forage and Pollination Guide
- Hive Signal Check

## Walkthrough Behavior Summary

After the user clicks `Ask locally`, the submit button changes to `Working locally...`, the existing local runtime loading message appears, and the hidden `Hive State Walkthrough` panel appears. The panel shows a CSS apiary scene with a beekeeper marker moving toward a hive, bee dots moving near the hive entrance, ant dots moving near the stand, and advisor-specific inspection steps rotating while the local response is pending.

The normal answer and retrieved sources rendering path remains unchanged after the local model response returns.

## CSS/JS Approach

- One shared HTML walkthrough block is rendered by `app/templates/advisor_form.html`.
- Advisor-specific step labels are provided as static UI context from `app/web_app.py`.
- CSS keyframes in `app/static/style.css` animate the beekeeper, bees, ants, and responsive walkthrough panel.
- Lightweight vanilla JavaScript in the existing advisor form submit handler reveals the walkthrough and rotates the visible step text.
- No build step, package install, CDN, external image, or external runtime dependency was added.

## Boundary Confirmations

- Phaser was not added.
- WebGL was not added.
- No external assets, CDNs, or packages were added.
- No model inference was run.
- No profiler was run.
- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- llama runtime logic was not changed.
- Retrieval logic was not changed.
- Prompt builder logic was not changed.
- Token streaming was not added.
- Real sensor integration was not added.
- Hausa was not added.
- Swahili was not added.

## Tests Run

Requested command:

```bash
python3 -m unittest tests/test_web_app.py
```

Result:

- Failed before importing the app because the system Python at `/usr/bin/python3` did not have `fastapi` installed.
- Failure was dependency-environment only; it was not an app test failure.

Temporary venv command:

```bash
/tmp/hyvegrid-031e-test-venv/bin/python -m unittest tests/test_web_app.py
```

Result:

- `Ran 34 tests in 0.699s OK`
- Verification rerun for commit: `Ran 34 tests in 0.527s OK`

## Preview

Mac preview URL: Not started.

## Known Limitation

This is a waiting walkthrough animation for local-generation UX. It is not a full simulation, not token streaming, not WebGL, not Phaser, and not real sensor integration.

## Next Recommended Task

- Task 031F: optional token streaming or local demo-speed path
- OR Task 032: deeper Hive State Walkthrough planning
