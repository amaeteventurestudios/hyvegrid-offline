# Task 035B Keeper Walking Sprite Sheet Specification

## Task Purpose

Task 035B specifies future beekeeper walking sprite assets for the HyveGrid
guided field walkthrough. This task is limited to asset planning and naming so a
later task can draw, upload, integrate, and test the walking keeper in the
existing scripted inspection route.

No new image assets are created in this task.

The current keeper uses a single static image. CSS can move that image along the
board, but it cannot show changing foot positions, body shift, or direction
changes. As a result, the current keeper slides instead of walking.

## Visual Goal

- The beekeeper should look like a person walking on the isometric board.
- The keeper should be readable at small scale.
- The keeper should visually match the existing African apiary board.
- The keeper should not look like a floating marker, robot, ghost, or flying
  object.
- The movement should support a scripted inspection route, not autonomous
  behavior.

## Beekeeper Character Requirements

- Beekeeper suit or light protective clothing.
- Veil or hat shape readable at small size.
- Boots or clear foot contact.
- Gloves optional.
- Smoker/tool optional, but it should not clutter the sprite.
- Simple readable silhouette.
- No proprietary hardware, sensor, or device details.

## Required Walking Directions

Minimum directional sprite set:

- `keeper-walk-se`
- `keeper-walk-sw`
- `keeper-walk-ne`
- `keeper-walk-nw`

These four directions are enough for a lightweight isometric guided field
walkthrough because the route can be split into southeast, southwest,
northeast, and northwest board-aligned segments.

## Optional Keeper States

- `keeper-idle`
- `keeper-inspect`

`idle` is used when the keeper pauses at a checkpoint.

`inspect` is used when the keeper visually checks the hive entrance, hive stand,
or surrounding area.

## Sprite Sheet Technical Specification

- Transparent background required.
- Recommended source format: PNG.
- Recommended runtime format: WebP.
- Recommended frame size: 96 x 128 px or 128 x 160 px.
- Recommended frame count per walking direction: 6 frames.
- Recommended idle frame count: 1 to 3 frames.
- Recommended inspect frame count: 2 to 4 frames.
- Bottom-center foot/contact point is the movement anchor.
- Asset should be drawn larger than final display size and scaled down in CSS.
- Keep file sizes lightweight for offline runtime.

## Asset Folder Plan

Runtime assets should live in:

`app/static/assets/walkthrough/`

Source/editable assets should live in:

`app/static/assets/source/`

## Naming Convention

| Asset role | Source PNG | Runtime WebP |
| --- | --- | --- |
| Walk southeast | `keeper-walk-se.png` | `keeper-walk-se.webp` |
| Walk southwest | `keeper-walk-sw.png` | `keeper-walk-sw.webp` |
| Walk northeast | `keeper-walk-ne.png` | `keeper-walk-ne.webp` |
| Walk northwest | `keeper-walk-nw.png` | `keeper-walk-nw.webp` |
| Idle | `keeper-idle.png` | `keeper-idle.webp` |
| Inspect | `keeper-inspect.png` | `keeper-inspect.webp` |

## Direction And Route Behavior Guidance For Later Integration

Later implementation should:

- Switch sprite direction by route segment.
- Use `walk-se`, `walk-sw`, `walk-ne`, and `walk-nw` classes or equivalent.
- Pause at inspection points.
- Switch to `idle` or `inspect` during pauses.
- Preserve the Task 034D camera timeline.
- Preserve advisor-specific walkthrough step text.
- Preserve existing loading behavior.
- Keep fallback to the current static keeper marker if sprite assets are
  missing.
- Keep the walking keeper as visual support while local guidance is prepared.
- Treat route cues as manual observations or sample edge-signal inputs.

## Manual Asset Creation Checklist

- [ ] Create transparent PNG sprite sheets.
- [ ] Verify frame alignment.
- [ ] Verify bottom-center foot anchor is consistent across frames.
- [ ] Verify the keeper reads clearly at final display size.
- [ ] Verify no frame appears to float.
- [ ] Verify walking loop does not jitter.
- [ ] Export runtime WebP files.
- [ ] Place runtime WebP files in `app/static/assets/walkthrough/`.
- [ ] Keep source PNG files in `app/static/assets/source/`.
- [ ] Preview against the actual apiary board before integration.

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

## Later Task Boundaries

- Task 035C should integrate keeper walking assets after they exist.
- Task 035D should handle direction-aware route switching.
- This task must not perform either of those steps.
