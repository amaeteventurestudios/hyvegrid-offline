# Task 037A Guided Field Walkthrough Demo Readiness Lock

## Current Commit Reviewed

- Branch: `phase-1-eval-harness`
- Commit: `fa498f0ef5142d69953fe98af040fc9a7dacc0cb`
- Commit message: `Polish walkthrough sprites from browser audit Task 036C`

## Walkthrough Asset Pipeline Summary

- Raw source images were processed in Task 035C.
- Cleaned source PNG sprite sheets were created and committed.
- Runtime WebP sprite sheets were created and committed.
- Sprite preview audit was completed in Task 035D.
- Browser visual audit was completed in Task 036B.
- Visual polish from browser audit notes was completed in Task 036C.
- Task 036C final recommendation: `PASS_FOR_DEMO`.

## Committed Runtime Sprite Assets

- `app/static/assets/walkthrough/bee-micro-sprite.webp`
- `app/static/assets/walkthrough/ant-micro-sprite.webp`
- `app/static/assets/walkthrough/keeper-inspect-sprite.webp`
- `app/static/assets/walkthrough/keeper-walk-sprite.webp`

## Committed Source PNG Assets

- `app/static/assets/source/bee-micro-sprite.png`
- `app/static/assets/source/ant-micro-sprite.png`
- `app/static/assets/source/keeper-inspect-sprite.png`
- `app/static/assets/source/keeper-walk-sprite.png`

## Confirmed Dimensions And Frame Counts

- Bee: `192 x 32`, 6 frames, `32 x 32` per frame.
- Ant: `192 x 32`, 6 frames, `32 x 32` per frame.
- Keeper inspect: `384 x 96`, 4 frames, `96 x 96` per frame.
- Keeper walk: `768 x 96`, 8 frames, `96 x 96` per frame.

## Wording Lock

The guided field walkthrough uses the approved wording:

- guided field walkthrough
- scripted inspection route
- visual support while local guidance is prepared
- manual observations or sample edge-signal inputs

The avoided terms were not introduced into the guided field walkthrough UI:

- autonomous agents
- digital twin
- live sensor simulation
- real-time sensor readings
- certified diagnosis

## Local-Only Rendering Lock

- No canvas is used.
- No WebGL is used.
- No Phaser is used.
- No CDN is used.
- No remote image is used.
- No external runtime dependency is used.
- Reduced-motion support exists through `@media (prefers-reduced-motion: reduce)`.
- The guided field walkthrough uses local static assets under `app/static/assets/`.

## Model And Scoring Lock

- No model/runtime/scoring files were changed in this walkthrough sprite phase.
- No model code was changed.
- No llama.cpp integration was changed.
- No retrieval code was changed.
- No `metadata.json` changes were made.
- No `download_model.sh` changes were made.
- No `REPORT.md` changes were made.
- This is demo-layer work and does not affect automated GGUF scoring.

## Static Checks

```text
manifest JSON OK
source/runtime assets OK
changed app files static check OK
tracked artifacts/source files: 0
```

`walkthrough-manifest.json` remains valid JSON. The four runtime WebP assets and
four source PNG assets exist. The checked app files do not include `http://`,
`https://`, `cdn`, `phaser`, `webgl`, or `<canvas`.

## Focused Web Tests

```text
Ran 41 tests in 0.777s

OK
```

## Final Status

WALKTHROUGH_DEMO_LOCKED
