# Task 036C Walkthrough Sprite Visual Polish

## Task 036B Notes Reviewed

Task 036B had a `PASS_WITH_NOTES` recommendation. The actionable visual note
was that ant micro-sprites were readable but subtle near the hive stand/ground
area. It also suggested optional follow-up screenshot evidence after polish.

No blocking dirty halo, background artifact, clipping, or frame misalignment was
reported. Keeper and bee sprites were already readable at intended scale.

## Files Changed

- `app/static/style.css`
- `tests/test_web_app.py`
- `artifacts/eval/walkthrough-sprite-visual-polish-task-036C.md`
- `artifacts/eval/walkthrough-sprite-visual-polish-task-036C.png`

## Exact Visual Fixes Made

- Increased ant sprite display size from `clamp(10px, 2vw, 15px)` to
  `clamp(12px, 2.3vw, 18px)`.
- Added a slightly stronger local shadow and warm edge glow to improve ant
  readability over the board without changing the source asset.
- Shortened the ant trail movement from `-18px` to `34px` into `-10px` to
  `24px` so ants stay closer to the hive stand/ground area.
- Raised the ant trail minimum opacity from `0.18` to `0.38` so the ants remain
  visible for more of the loop.
- Added a focused web test assertion for the polished ant size token.

## Intentionally Left Unchanged

- Keeper walk and keeper inspect sprite sizing and timing.
- Bee sprite sizing and hover timing.
- Existing board image and camera timeline.
- Existing guided field walkthrough wording and advisor-specific step text.
- Existing submit/loading behavior.
- Existing source PNG and runtime WebP files.
- Existing manifest entries.

## Visual Proof

- Screenshot artifact:
  `artifacts/eval/walkthrough-sprite-visual-polish-task-036C.png`
- Browser style evidence showed ants rendering at `18px` with the updated
  contrast filter and `steps(6)` animation.
- Local server logs showed HTTP 200 loads for the board, keeper walk, keeper
  inspect, bee, and ant local assets.

## Validation

```text
manifest JSON OK
source/runtime assets OK
changed app files static check OK
```

Focused web suite passed:

```text
Ran 41 tests in 0.703s

OK
```

## Confirmations

- The guided field walkthrough still uses only local assets.
- No canvas, WebGL, Phaser, CDN, remote image, cloud API, external runtime
  service, or external runtime dependency was added.
- No app behavior was changed.
- No inference behavior was changed.
- No model/runtime/scoring files were changed.
- No `metadata.json`, `download_model.sh`, or `REPORT.md` files were changed.
- The untracked raw source folder `artifacts/source/` was not committed.

## Final Recommendation

PASS_FOR_DEMO
