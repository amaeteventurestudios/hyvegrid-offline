# Task 035A Bee and Ant Micro-Sprite Specification

## Task Purpose

Task 035A specifies future bee and ant micro-sprite assets for the HyveGrid
guided field walkthrough. This task is limited to asset planning and naming so a
later task can draw, upload, integrate, and test the sprites in the existing
scripted inspection route.

No new image assets are created in this task.

## Bee Micro-Sprite Specification

Recommended source filename:

`app/static/assets/source/bee-micro-sprite.png`

Recommended runtime filename:

`app/static/assets/walkthrough/bee-micro-sprite.webp`

Asset requirements:

- Transparent background required.
- Recommended frame size: 32 x 32 px.
- Recommended frame count: 4 to 6 frames.

Visual requirements:

- Must read as a bee at small size.
- Use a yellow/black body.
- Include small wings.
- Show slight hover or wing movement.
- Remain readable over the isometric board.

Intended behavior:

- Small looping hover near the hive entrance.
- No autonomous behavior.
- Purely scripted visual support while local guidance is prepared.

## Ant Micro-Sprite Specification

Recommended source filename:

`app/static/assets/source/ant-micro-sprite.png`

Recommended runtime filename:

`app/static/assets/walkthrough/ant-micro-sprite.webp`

Asset requirements:

- Transparent background required.
- Recommended frame size: 32 x 32 px.
- Recommended frame count: 4 to 6 frames.

Visual requirements:

- Must read as an ant at small size.
- Use a dark body.
- Imply head/thorax/abdomen shape.
- Imply legs or marching motion.
- Remain readable near the hive stand.

Intended behavior:

- Small scripted march near the hive stand.
- No autonomous behavior.
- Represents manual observation of ant pressure, not live sensing.

## Asset Folder Plan

Runtime assets should live in:

`app/static/assets/walkthrough/`

Editable/source assets should live in:

`app/static/assets/source/`

## Naming Convention

| Filename | Purpose | Recommended location |
| --- | --- | --- |
| `bee-micro-sprite.png` | Editable bee sprite-sheet source | `app/static/assets/source/` |
| `bee-micro-sprite.webp` | Runtime bee sprite-sheet asset | `app/static/assets/walkthrough/` |
| `ant-micro-sprite.png` | Editable ant sprite-sheet source | `app/static/assets/source/` |
| `ant-micro-sprite.webp` | Runtime ant sprite-sheet asset | `app/static/assets/walkthrough/` |

## Integration Guidance For Later Task

- Later CSS should use sprite-sheet background-position animation or simple
  frame-based animation.
- Later JS/CSS should keep behavior scripted.
- Bees should appear near the hive entrance.
- Ants should appear near the hive stand.
- Preserve existing loading behavior and advisor-specific step text.
- Preserve the Task 034D camera timeline.
- Keep the sprites as visual support while local guidance is prepared.
- Treat the visual state as manual observations or sample edge-signal inputs.

## Safety And Wording Constraints

Approved terms for later copy and evidence:

- guided field walkthrough
- scripted inspection route
- visual support while local guidance is prepared
- manual observations or sample edge-signal inputs

Avoid these terms in user-facing copy:

- autonomous agents
- digital twin
- live sensor simulation
- real-time sensor readings
- certified diagnosis

## Manual Asset Creation Checklist

- [ ] Create transparent PNG sprite sheet.
- [ ] Verify readability at final display scale.
- [ ] Convert to WebP.
- [ ] Place runtime WebP in `app/static/assets/walkthrough/`.
- [ ] Keep PNG source in `app/static/assets/source/`.
- [ ] Preview against the actual board background before integration.
