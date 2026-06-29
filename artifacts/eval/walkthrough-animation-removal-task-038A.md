# Task 038A Walkthrough Animation Removal Audit

## Why The Sprite Animation Was Removed

The prior sprite animation layer was technically validated, but the product
direction changed toward a cleaner field-tool interface. Task 038A removes the
sprite/walkthrough animation layer from the live advisor UI and replaces it
with a simple local guidance waiting state.

## Files Changed

- `app/templates/advisor_form.html`
- `app/static/style.css`
- `app/static/assets/README.md`
- `tests/test_web_app.py`
- `artifacts/eval/walkthrough-animation-removal-task-038A.md`

## Files Deleted

- `app/static/assets/walkthrough/bee-micro-sprite.webp`
- `app/static/assets/walkthrough/ant-micro-sprite.webp`
- `app/static/assets/walkthrough/keeper-inspect-sprite.webp`
- `app/static/assets/walkthrough/keeper-walk-sprite.webp`
- `app/static/assets/source/bee-micro-sprite.png`
- `app/static/assets/source/ant-micro-sprite.png`
- `app/static/assets/source/keeper-inspect-sprite.png`
- `app/static/assets/source/keeper-walk-sprite.png`
- `app/static/assets/walkthrough/walkthrough-manifest.json`
- `app/static/assets/walkthrough-apiary-board.webp`
- `app/static/assets/walkthrough-keeper-marker.webp`
- `app/static/assets/source/walkthrough-apiary-board.png`
- `app/static/assets/source/walkthrough-keeper-marker.png`
- `scripts/process_walkthrough_assets.py`
- `scripts/preview_walkthrough_sprites.py`

The untracked raw folder `artifacts/source/` was removed locally and was not
committed.

## Old References Removed

The live advisor template and CSS no longer reference:

- bee sprite usage
- ant sprite usage
- keeper walk sprite usage
- keeper inspect sprite usage
- old board/keeper waiting visual assets
- old walkthrough markup/classes
- sprite-specific CSS animation classes
- sprite processing or preview scripts
- sprite manifest entries

## New Waiting State Added

The advisor page now shows a static local guidance waiting/status panel on form
submit. The panel includes:

- `Preparing local guidance...`
- `Working locally on your question. No cloud access.`
- progress rows for reading the field observation, searching local apiculture
  notes, preparing a cautious response, and running the local GGUF model through
  llama.cpp
- the note `This may take a few minutes on a low-cost laptop.`
- a `Need visual support?` support card
- a `Local system status` card
- language output controls for English, Yorùbá, Hausa Preview, and Swahili
  Preview

The form still posts normally. Plain local JavaScript only reveals the waiting
panel, disables the submit button, and keeps the existing local request flow.

## Confirmations

- The app now uses a simple local guidance waiting state instead of sprites.
- No Remotion, Phaser, WebGL, canvas, CDN, remote image, cloud API, external
  runtime service, internet dependency, or remote asset was added.
- No model/runtime/scoring files were changed.
- No model code, llama.cpp integration, retrieval code, `metadata.json`,
  `download_model.sh`, `REPORT.md`, or model files were changed.
- Local inference behavior was not changed.
- The known Mac `LLAMA_BIN` runtime setup issue was not addressed in this task.
- The app remains fully local/offline.

## Checks

```text
manifest removed
changed app files static check OK
no live template/CSS references to deleted sprite files
```

Focused web suite in the existing preview venv passed:

```text
Ran 40 tests in 0.889s

OK
```

The exact system command `python3 -m unittest tests.test_web_app` was also run.
It failed because the system Python environment lacks `fastapi`, matching the
known local environment split; the focused web suite passes in the preview venv.

## Final Status

ANIMATION_REMOVED_WAITING_STATE_READY
