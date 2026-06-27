# Task 033 Keeper Overlay Marker and Advisor Route Evidence

Date/time: 2026-06-26T20:12:56-0700

Starting commit: `8fa50299bb19b279093e1ab374e95dc09a5c4fd6`

## Task Name

Task 033: Keeper Overlay Marker and Advisor Route Refinement.

## Files Changed

- `app/templates/advisor_form.html`
- `app/static/style.css`
- `app/web_app.py`
- `tests/test_web_app.py`
- `app/static/assets/README.md`
- `app/static/assets/source/walkthrough-keeper-marker.png`
- `app/static/assets/walkthrough-keeper-marker.webp`
- `artifacts/eval/keeper-overlay-route-task-033.md`

## Asset Files Added

- Source keeper PNG: `app/static/assets/source/walkthrough-keeper-marker.png`
- Keeper WebP output: `app/static/assets/walkthrough-keeper-marker.webp`

## Conversion Approach

The keeper PNG was converted locally with Pillow in a temporary `/tmp` virtual environment. Pillow was not added to project requirements.

Conversion settings:

- Open source PNG.
- Convert to RGBA to preserve transparency.
- Crop to the nontransparent marker content so the keeper renders visibly as an overlay.
- Save WebP with `quality=90` and `method=6`.

Source keeper details:

- Path: `app/static/assets/source/walkthrough-keeper-marker.png`
- Size: 2,147,799 bytes
- Format: PNG, 1536 x 1024, RGBA

Keeper WebP details:

- Path: `app/static/assets/walkthrough-keeper-marker.webp`
- Size: 62,384 bytes
- Dimensions: 451 x 493

## Advisor Pages Affected

- Hive Health Advisor
- Site Readiness Advisor
- Harvest Quality Coach
- Forage and Pollination Guide
- Hive Signal Check

## Behavior Summary

The existing waiting walkthrough keeps the static `walkthrough-apiary-board.webp` background and now uses `walkthrough-keeper-marker.webp` as the visible keeper overlay. When the user clicks `Ask locally`, the existing submit handler still changes the button to `Working locally...`, shows the existing loading message, reveals the hidden walkthrough panel, and rotates advisor-specific steps while local guidance is prepared.

The normal answer and retrieved source rendering path remains unchanged after the response returns.

## Route Behavior Summary

The keeper follows a CSS-scripted route with gentle pauses and bobbing while the walkthrough is visible. The route starts from a visible path area, moves toward the apiary, pauses around hive/entrance and stand areas, advances toward a later inspection point, and loops gently while the local answer is pending.

Advisor-specific route labels are static UI context:

- Hive Health Advisor: hive, entrance, ant trail, brood/food, guidance.
- Site Readiness Advisor: proposed area, water, crop zones, shade/wind, pesticide risk, guidance.
- Harvest Quality Coach: hive area, timing, capped honey, storage/hut, filtering/storage, guidance.
- Forage and Pollination Guide: apiary to crop edge, crop plots, forage, water/shade, guidance.
- Hive Signal Check: hive area, activity marker, temperature-style marker, humidity-style marker, clustering/activity note, guidance.

## Boundary Confirmations

- Task 031E submit/loading/walkthrough behavior was preserved.
- Task 032 board background behavior was preserved.
- Moving Keeper, bees, ants, and checklist remain overlay elements.
- The Keeper is scripted, not autonomous.
- The UI does not call this a simulation.
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
/tmp/hyvegrid-task-033-test-venv/bin/python -m unittest tests/test_web_app.py
```

Result:

- `Ran 35 tests in 0.497s OK`
- Final rerun after marker crop documentation: `Ran 35 tests in 0.519s OK`

## Preview

Mac preview URL: Not started.

## Known Limitation

This is a scripted overlay route, not a full walking sprite sheet and not an autonomous agent system.

## Next Recommended Task

- Task 034: Visual preview audit and route tuning from screenshot evidence
- OR Task 031F: optional token streaming/local demo-speed path
