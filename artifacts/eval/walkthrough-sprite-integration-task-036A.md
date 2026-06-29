# Task 036A Walkthrough Sprite Integration Audit

## Task Summary

Task 036A integrates the processed walkthrough sprite sheets into the existing
guided field walkthrough using plain HTML and CSS. The existing board image,
loading behavior, advisor-specific step text, scripted inspection route timing,
and offline local asset flow remain in place.

## Files Changed

- `app/templates/advisor_form.html`
- `app/static/style.css`
- `tests/test_web_app.py`
- `artifacts/eval/walkthrough-sprite-integration-task-036A.md`

## Sprites Integrated

- `app/static/assets/walkthrough/keeper-walk-sprite.webp`
- `app/static/assets/walkthrough/keeper-inspect-sprite.webp`
- `app/static/assets/walkthrough/bee-micro-sprite.webp`
- `app/static/assets/walkthrough/ant-micro-sprite.webp`

## Placement

- Keeper walk sprite appears on the existing bottom-center anchored keeper
  route marker during movement portions of the scripted inspection route.
- Keeper inspect sprite appears on the same anchored keeper position during
  scripted route pauses.
- Bee micro-sprites appear as small hover details near the hive area.
- Ant micro-sprites appear as subtle movement near the hive stand or ground
  area.
- The existing `app/static/assets/walkthrough-apiary-board.webp` board remains
  the walkthrough background.
- The existing `app/static/assets/walkthrough-keeper-marker.webp` marker remains
  referenced in the markup as the conservative fallback asset.

## Animation Method

- Sprite frames use CSS `steps()` animation through `background-position`.
- Keeper walk uses an 8-frame `steps(8)` loop.
- Keeper inspect uses a 4-frame `steps(4)` loop during route pauses.
- Bee and ant micro-sprites use 6-frame `steps(6)` loops.
- No canvas, sprite rendering library, Phaser, WebGL, or external runtime
  dependency was added.

## Reduced Motion

Reduced-motion support exists through `@media (prefers-reduced-motion: reduce)`.
In reduced-motion mode, camera movement, route movement, sprite frame stepping,
bee movement, ant movement, and keeper shadow pulsing are frozen.

## Confirmations

- No model/runtime/scoring files were edited.
- No model code, llama.cpp integration, retrieval code, `metadata.json`,
  `download_model.sh`, `REPORT.md`, or model files were changed.
- The guided field walkthrough uses offline local assets only.
- No CDN, remote image, remote script, cloud API, or external runtime service
  was added.
- No production animation framework was added.

## Visual Concerns And Follow-Up

- The ant micro-sprite is intentionally subtle and should remain over lighter
  board/stand areas during later tuning.
- The keeper walk sheet is a single side-view walking loop; later route work can
  improve direction-aware switching if additional directional sheets are drawn.
- A later polish task may tune exact keeper scale against the Task 034D camera
  timeline after manual preview on target hardware.

## Validation

Manifest and static asset checks passed:

```text
manifest JSON OK
runtime WebP assets OK
no remote/CDN/Phaser/WebGL/canvas refs in changed app files
```

Focused web suite passed:

```text
Ran 41 tests in 0.542s

OK
```

Full discovered suite with the preview venv ran 88 tests and failed only on the
existing unrelated runtime diagnostics expectation that this workspace path
should end with `hyvegrid-offline`; the actual workspace ends with
`hyvegrid-offline-adtc-2026`.

```text
FAILED (failures=1)
test_runtime_diagnostics_reports_configured_paths
```
