# Task 032 Isometric Apiary Background Board Evidence

Date/time: 2026-06-26T19:36:50-0700

Starting commit: `5e0bce8dd51cccd4e4ef13c677b687612444869c`

## Task Name

Task 032: HyveGrid Isometric Apiary Background Board.

## Files Changed

- `app/templates/advisor_form.html`
- `app/static/style.css`
- `tests/test_web_app.py`
- `app/static/assets/README.md`
- `app/static/assets/source/walkthrough-apiary-board.png`
- `app/static/assets/walkthrough-apiary-board.webp`
- `artifacts/eval/isometric-apiary-background-task-032.md`

## Asset Files Added

- Source PNG: `app/static/assets/source/walkthrough-apiary-board.png`
- WebP output: `app/static/assets/walkthrough-apiary-board.webp`

## Conversion Approach

The source PNG was converted locally with Pillow in a temporary `/tmp` virtual environment. Pillow was not added to project requirements.

Conversion settings:

- Open source PNG.
- Convert to RGB.
- Save WebP with `quality=82` and `method=6`.

Source image details:

- Path: `app/static/assets/source/walkthrough-apiary-board.png`
- Size: 3,806,571 bytes
- Dimensions: 1536 x 1024
- Visual check: no visible people or animals are baked into the background image.

WebP output details:

- Path: `app/static/assets/walkthrough-apiary-board.webp`
- Size: 563,168 bytes
- Dimensions: 1536 x 1024

## Advisor Pages Affected

- Hive Health Advisor
- Site Readiness Advisor
- Harvest Quality Coach
- Forage and Pollination Guide
- Hive Signal Check

## Behavior Summary

The Task 031E waiting walkthrough panel now uses `walkthrough-apiary-board.webp` as a local static isometric apiary board background. The existing submit flow is preserved: the advisor submit button changes to `Working locally...`, the existing local runtime loading message appears, the walkthrough panel appears, and advisor-specific checklist steps continue rotating while local guidance is prepared.

Moving elements remain separate overlay elements:

- Keeper marker
- Bee dots
- Ant trail dots
- Advisor-specific checklist and active step marker

The Keeper is a scripted visual walkthrough marker only. It is not an autonomous AI agent.

## Boundary Confirmations

- Existing Task 031E submit/loading/walkthrough behavior was preserved.
- Moving Keeper, bees, ants, and checklist remain overlay elements.
- The Keeper is scripted, not autonomous.
- Phaser was not added.
- WebGL was not added.
- Canvas was not added.
- No external packages were added to project requirements.
- No CDN or external runtime assets were added.
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

System Python command:

```bash
python3 -m unittest tests/test_web_app.py
```

Result:

- Failed before importing the app because `/usr/bin/python3` did not have `fastapi` installed.
- This was a local dependency-environment issue, not an app test failure.

Temporary venv command:

```bash
/tmp/hyvegrid-task-032-test-venv/bin/python -m unittest tests/test_web_app.py
```

Result:

- `Ran 34 tests in 1.082s OK`

## Preview

Mac preview URL: Not started.

## Known Limitation

This is a static background board with scripted overlays. It is not a full simulation, autonomous agent system, token streaming system, WebGL scene, Phaser scene, canvas scene, or real sensor integration.

## Next Recommended Task

- Task 033: Keeper overlay route refinement and advisor-specific map markers
- OR Task 031F: optional token streaming or local demo-speed path
