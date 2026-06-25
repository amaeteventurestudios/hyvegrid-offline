# Task 030: HyveGrid visual asset plan

Date/time of run: 2026-06-25 16:53:22 PDT

Starting branch: `phase-1-eval-harness`

Starting commit: `5b296d216b68e749fa74e16d9f6ed0603cd67d5d`

## Reference PNG Availability

Documented host reference path:

```text
/Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026/public/images/hyvegrid-site reference.png
```

Expected VM/repo path checked:

```text
public/images/hyvegrid-site reference.png
/home/amaete/hyvegrid-offline/public/images/hyvegrid-site reference.png
```

Result: the reference PNG was not found inside the VM repo. Task 030 used the provided reference description as the source of truth. No image was copied, moved, converted, or edited.

## Visual Direction Summary

Task 030 documents a honey-brown / dark amber / golden-brown visual direction with gold/yellow accents, cream/off-white text, near-black depth colors, honeycomb texture, bee imagery, and a honeycomb/cone-style logo mark.

The plan explicitly rejects the earlier green dashboard direction and any generic blue dashboard direction.

Tone: serious, field-intelligence, offline, honey/apiculture system.

## Mobile-First and Center-Aligned Layout

The visual plan requires mobile-first layout behavior and center-aligned composition:

- 9:16 phone-shaped viewports are first-class targets.
- Major sections should be centered and visually balanced.
- Hero logo, title, and key status cards should center where practical.
- Advisor cards should stack on narrow screens.
- Card content should center on mobile unless readability requires otherwise.
- Horizontal scrolling, cramped text, and left-heavy desktop-only layout are not acceptable.

## Responsive Viewport Requirements

Task 031 should inspect at least:

- Mobile 390 x 844 or similar
- Mobile 430 x 932 or similar
- Tablet/small width 768 x 1024
- Laptop 1366 x 768 or similar

Planned behavior:

- Hero stacks vertically on mobile.
- Status strip becomes stacked cards on mobile.
- Advisor cards become one column on mobile.
- Guide cards become one or two columns depending on readability.
- At a Glance stats stack cleanly on mobile.
- Language dropdown remains visible and easy to tap.

## Required Hero WebP Placeholders

- `hero-honeycomb-bg.webp`
- `logo-honeycomb-mark.webp`
- `hero-bee.webp`

## Required Advisor Card WebP Placeholders

- `card-hive-health.webp`
- `card-site-readiness.webp`
- `card-harvest-quality.webp`
- `card-forage-pollination.webp`
- `card-hive-signal.webp`
- `card-offline-status.webp`

## Required Guidance Card WebP Placeholders

- `guide-yoruba-template.webp`
- `guide-ask-advisor.webp`
- `guide-daily-checklist.webp`
- `guide-storage-handling.webp`
- `guide-pesticide-awareness.webp`
- `guide-forage-calendar.webp`

## Implementation Warning

Do not build the future UI as one flat screenshot. Task 031 should use real HTML/CSS with local assets. Text must remain editable, accessible, responsive, and compatible with Yoruba mode.

Assets should be backgrounds, icons, panels, marks, and illustrations, not text-heavy screenshots.

## Yoruba Compatibility Note

The future visual refresh must preserve:

- English default behavior
- Yoruba mode
- Language dropdown
- Controlled Yoruba templates
- Yoruba glossary
- Human Yoruba review note

The layout must be checked in Yoruba mode because longer localized labels can change wrapping.

## Offline and Local Asset Note

All planned assets are local-only. No CDN, external image links, external fonts, cloud assets, or external runtime dependency should be introduced.

All planned placeholder site images are documented as WebP. The reference PNG remains allowed only as a visual reference.

## Visual Inspection Requirements for Task 031

Task 031 should use browser tooling if available:

- Firefox headless screenshot if working
- Chromium/Playwright if installed
- Otherwise route/HTML checks with explicit reporting that screenshot tooling was unavailable

Task 031 must confirm:

- No horizontal overflow
- Centered major sections
- Readable card text
- Tappable dropdown and buttons
- Yoruba mode does not break layout
- Advisor cards align cleanly
- Guidance cards align cleanly
- At a Glance section stacks cleanly

## Simulation Boundary

The future visual layer should be called Hive State Walkthrough or Guided Hive Walkthrough in the public ADTC version.

For ADTC, it should use manual observations and sample edge-signal inputs. It must not claim live proprietary sensor integration. Real wireless sensor-informed visualization belongs to a future private/product lane, not the public repo implementation.

## IP and Compliance Note

The visual asset system must not include:

- Proprietary hardware plans
- Sensor IP
- Wireless architecture
- Firmware strategy
- Private datasets
- Real partner/customer/pilot data
- Commercial roadmap
- Investor materials
- Patent-sensitive diagrams
- Certified diagnosis claims

No cloud dependency, app runtime dependency, metadata/model/download/runtime change, retrieval change, prompt-builder change, Hausa implementation, Swahili implementation, visual redesign implementation, animation, or simulation implementation was added in Task 030.

## Files Created

- `specs/001-hyvegrid-offline/visual-asset-system.md`
- `artifacts/eval/hyvegrid-visual-asset-plan-task-030.md`

## No-Code Confirmation

Task 030 is planning/documentation only. No app source code, templates, CSS, images, binary assets, model files, runtime integration, retrieval logic, prompt builder, `metadata.json`, or `download_model.sh` were changed.

## Next Recommended Tasks

- Task 031A: Create WebP placeholder asset slots
- Task 031B: Mission Control visual refresh
- Task 031C: Advisor page visual refresh
