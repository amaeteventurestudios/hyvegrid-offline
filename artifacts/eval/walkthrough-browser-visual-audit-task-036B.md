# Task 036B Walkthrough Browser Visual Audit

## Scope

Task 036B audited the integrated walkthrough sprites in the actual rendered
advisor page context. No production behavior, advisor logic, inference behavior,
model path handling, metadata, download script, report, retrieval, scoring, or
model files were changed.

## Page Inspected

- Route: `/advisor/hive-health`
- URL: `http://127.0.0.1:8000/advisor/hive-health`
- Screenshot artifact:
  `artifacts/eval/walkthrough-browser-visual-audit-task-036B.png`

## Browser Method

- Local app server: `/tmp/hyvegrid-task-034b-test-venv/bin/python -m app.web_app`
- Browser: local Google Chrome through the existing bundled local Playwright
  package.
- Screenshot method: loaded the live advisor page, filled the sample question,
  and activated the same client-side loading/walkthrough state used by the form
  submit handler without sending a final inference request.
- Server log evidence during browser runs showed HTTP 200 loads for the board,
  keeper walk, keeper inspect, bee, and ant local WebP assets.

## Visual Results

- Board image rendered: yes.
- Keeper walk sprite rendered: yes, visible on the scripted inspection route.
- Keeper inspect sprite rendered or fallback observed: the inspect sprite asset
  was loaded and CSS-attached; it was not visible in the captured movement frame
  because the route was in the walking segment. No fallback condition was
  observed.
- Bee micro-sprites rendered: yes, visible near hive areas.
- Ant micro-sprites rendered: yes, visible but subtle near the hive stand/ground
  area.
- Sprites readable at intended scale: yes for keeper and bees; ants are readable
  but intentionally subtle.
- Dirty halo, background artifact, clipping, or frame misalignment: no blocking
  issue visible in the screenshot. Minor edge softness from the source art is
  acceptable for demo use.
- Reduced-motion CSS exists and remains valid:
  `@media (prefers-reduced-motion: reduce)` freezes camera, route, sprite frame,
  bee, ant, and shadow animations.

## Browser Computed Style Evidence

- Board background: `/static/assets/walkthrough-apiary-board.webp`
- Keeper walk background: `/static/assets/walkthrough/keeper-walk-sprite.webp`
- Keeper walk animation: `keeper-walk-frames, keeper-walk-visibility`
- Keeper walk timing: `steps(8), steps(1)`
- Keeper inspect background:
  `/static/assets/walkthrough/keeper-inspect-sprite.webp`
- Keeper inspect animation: `keeper-inspect-frames, keeper-inspect-visibility`
- Keeper inspect timing: `steps(4), steps(1)`
- Bee background: `/static/assets/walkthrough/bee-micro-sprite.webp`
- Bee animation: `bee-sprite-frames, bee-loop-one`
- Bee timing: `steps(6), ease-in-out`
- Ant background: `/static/assets/walkthrough/ant-micro-sprite.webp`
- Ant animation: `ant-sprite-frames, ant-trail`
- Ant timing: `steps(6), linear`

## Wording Check

Approved wording remains present in the walkthrough:

- guided field walkthrough
- scripted inspection route
- Visual support while local guidance is prepared.
- manual observations or sample edge-signal inputs

No new app wording was introduced in this task. The avoided terms listed in the
Task 036B brief were not added to the app UI or CSS.

## Static Checks

```text
manifest JSON OK
source/runtime assets OK
changed app files static check OK
```

The static check confirmed no `http://`, `https://`, `cdn`, `phaser`, `webgl`,
or `<canvas` references were introduced in the changed app files.

## Tests

Focused web suite passed:

```text
Ran 41 tests in 0.451s

OK
```

## Confirmations

- No canvas, WebGL, Phaser, CDN, remote image, cloud API, external runtime
  service, or external runtime dependency was introduced.
- No app behavior was changed.
- No inference behavior was changed.
- No model path behavior was changed.
- No model/runtime/scoring files were edited.
- No `metadata.json`, `download_model.sh`, or `REPORT.md` files were edited.
- The guided field walkthrough still uses offline local assets only.
- The untracked raw source folder `artifacts/source/` was not committed.

## Recommendation

PASS_WITH_NOTES

The sprites are demo-ready in browser context. Follow-up polish can make the
ant motion slightly easier to read and capture a second screenshot during an
inspect-pause frame if needed.
