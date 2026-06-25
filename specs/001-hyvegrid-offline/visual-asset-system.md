# HyveGrid Offline Visual Asset System

Task: 030

Date: 2026-06-25

Status: planning/specification only

## 1. Purpose

This document defines the visual asset system for the HyveGrid Offline public ADTC edition. It supports demo clarity, panel impression, African use-case presentation, and product coherence for the local offline app.

The visual asset system does not change the automated GGUF scoring path. The scored path remains the locked GGUF model evaluated through `llama.cpp`; visual assets, UI polish, and demo presentation do not affect profiler telemetry.

## 2. Visual Reference

Reference file path from the host machine:

```text
/Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026/public/images/hyvegrid-site reference.png
```

Expected VM/repo path:

```text
public/images/hyvegrid-site reference.png
```

The reference image is a PNG and is for visual reference only. Actual site placeholder assets should be planned as WebP files, not PNG files.

## 3. Visual Direction

Use the 9:16 honey-brown mockup as the visual reference.

Primary direction:

- Honey-brown
- Dark amber
- Golden brown
- Gold/yellow accents
- Cream/off-white text
- Near-black depth colors
- Honeycomb texture
- Bee imagery
- Honeycomb/cone-style logo mark

Do not use the earlier green dashboard direction. Do not use a generic blue dashboard direction.

Tone: serious, field-intelligence, offline, honey/apiculture system. The UI should feel like a practical field intelligence product for beekeepers and extension workers, not a generic developer dashboard.

## 4. Mobile-First and Center-Aligned Layout Requirements

Treat mobile as a first-class target. The design should work naturally in a 9:16 viewport.

Layout requirements:

- Center-align major visual sections.
- Center the hero logo, title, and key status cards where practical.
- Center card content on mobile unless readability requires otherwise.
- Use stacked cards on narrow screens.
- Avoid horizontal scrolling.
- Avoid cramped text.
- Avoid left-heavy desktop-only layouts.
- Use balanced spacing, large tap targets, readable typography, and clear visual hierarchy.
- Maintain a polished look on both phone-shaped 9:16 viewports and laptop browser windows.

On mobile, the interface should feel intentionally composed rather than like a desktop page squeezed into a phone.

## 5. Responsive Breakpoint Plan

Small mobile width, around 360 to 430 px:

- Hero stacks vertically.
- Hero logo, title, language dropdown, and status indicators are centered.
- Bee visual is smaller and should not crowd the layout.
- Status strip becomes stacked cards.
- Advisor cards become one column.
- Guide cards become one column unless two columns remain readable.
- At a Glance stats stack cleanly.
- Language dropdown remains visible and easy to tap.

Larger mobile / small tablet width, around 600 to 768 px:

- Hero remains centered but can use slightly wider spacing.
- Advisor cards may use two columns if text remains readable.
- Guide cards may use two columns.
- Status strip can use two-column cards.
- At a Glance can use two or three columns only if it remains balanced.

Laptop browser width, around 1024 to 1440 px:

- Hero can use a balanced two-zone layout with centered content and bee visual support.
- Bee visual may sit to the right on wider screens.
- Advisor cards can use a centered grid.
- Guide cards can use a centered grid.
- At a Glance can use a horizontal or multi-column layout.
- Major titles and visual sections should still feel centered and balanced, not left-heavy.

## 6. Implementation Principle

Do not recreate the mockup as one giant flat screenshot.

Future implementation should build real HTML/CSS UI using local assets. Text must remain real HTML so it is editable, accessible, responsive, and compatible with Yoruba mode.

Assets should be backgrounds, icons, panels, marks, and illustrations, not text-heavy screenshots. Avoid baking important UI text into images.

## 7. Asset Directory Plan

Planned local asset directory:

```text
app/static/assets/
```

Planned WebP placeholder assets:

- `hero-honeycomb-bg.webp`
- `logo-honeycomb-mark.webp`
- `hero-bee.webp`
- `card-hive-health.webp`
- `card-site-readiness.webp`
- `card-harvest-quality.webp`
- `card-forage-pollination.webp`
- `card-hive-signal.webp`
- `card-offline-status.webp`
- `guide-yoruba-template.webp`
- `guide-ask-advisor.webp`
- `guide-daily-checklist.webp`
- `guide-storage-handling.webp`
- `guide-pesticide-awareness.webp`
- `guide-forage-calendar.webp`

Task 030 does not create these files. They are planned placeholders for a later asset task.

## 8. Hero Section Asset Plan

Planned hero assets and layout:

- Honeycomb/dark amber background using `hero-honeycomb-bg.webp`.
- Bee visual using `hero-bee.webp`.
- Bee visual may sit on the right for wider screens.
- Bee visual should not crowd mobile layout.
- Honeycomb/cone-style logo mark using `logo-honeycomb-mark.webp`.
- Real HTML overlay for:
  - HyveGrid Offline
  - Language dropdown
  - Mission Control
  - Offline Mode
  - Model: Granite 3.3 2B
  - System Ready

On mobile, hero content should be centered and stacked.

## 9. Main Advisor Card Asset Plan

| Screen | Planned asset | Visual concept |
| --- | --- | --- |
| Hive Health Advisor | `card-hive-health.webp` | Bee + hive + brood/colony health symbol |
| Site Readiness Advisor | `card-site-readiness.webp` | Location pin + apiary placement + trees |
| Harvest Quality Coach | `card-harvest-quality.webp` | Honey jar + capped frame |
| Forage & Pollination Guide | `card-forage-pollination.webp` | Flower + bee + pollen |
| Hive Signal Check | `card-hive-signal.webp` | Signal wave + hive activity |
| Offline System Status | `card-offline-status.webp` | Shield/check + local system readiness |

Card layout requirements:

- Cards should be centered and visually balanced.
- Icons/images should sit above or centered beside text depending on width.
- Mobile cards should stack vertically.
- Card actions should be centered and easy to tap.

## 10. Guidance Card Asset Plan

| Guide card | Planned asset | Visual concept |
| --- | --- | --- |
| Yoruba Template | `guide-yoruba-template.webp` | Honeycomb + language/template symbol |
| Ask the Hive Advisor | `guide-ask-advisor.webp` | Chat bubble + bee/hive mark |
| Daily Hive Checklist | `guide-daily-checklist.webp` | Checklist + field notebook |
| Storage & Handling | `guide-storage-handling.webp` | Honey jar/storage container |
| Pesticide Awareness | `guide-pesticide-awareness.webp` | Shield + caution + bee |
| Forage Calendar | `guide-forage-calendar.webp` | Flower + calendar |

Layout requirements:

- Cards should be compact but readable.
- Mobile should use stacked cards or two-column cards only if readable.
- Avoid tiny text.

## 11. UI Sections for Later Task 031

Future Mission Control layout:

- Hero section
- Status strip
- Six main advisor cards
- Safety reminder strip
- Guidance at Your Fingertips
- At a Glance
- Language dropdown preserved
- Yoruba mode preserved
- Centered layout preserved on mobile and desktop

## 12. Visual Inspection Requirements for Task 031

Task 031 implementation must visually inspect the UI before committing.

Required viewport checks:

- Mobile 390 x 844 or similar
- Mobile 430 x 932 or similar
- Tablet/small width 768 x 1024
- Laptop 1366 x 768 or similar

Codex should use available browser tooling if present:

- Firefox headless screenshot if working
- Chromium/Playwright if installed
- Otherwise HTML route checks plus an explicit report that screenshot tooling was unavailable

Task 031 must confirm:

- No horizontal overflow
- Centered major sections
- Readable card text
- Tappable dropdown and buttons
- Yoruba mode does not break layout
- Advisor cards align cleanly
- Guidance cards align cleanly
- At a Glance section stacks cleanly

## 13. Asset Technical Requirements

- Local only
- No CDN
- No external image links
- No external font dependency
- All planned placeholder images must be WebP
- Do not use PNG for site placeholder assets
- Reference PNG is allowed only as a visual reference
- No large binary files unless justified
- Responsive on laptop browser and narrow screens
- No text baked into images unless it is purely decorative

## 14. Public ADTC IP Boundary

Assets must not include:

- Proprietary sensor design
- Wireless architecture
- Firmware strategy
- Private datasets
- Real partner/customer/pilot data
- Commercial roadmap
- Investor materials
- Patent-sensitive diagrams
- Certified diagnosis claims

## 15. Simulation Boundary

The future visual layer should be called Hive State Walkthrough or Guided Hive Walkthrough in the public ADTC version.

For ADTC it should use manual observations and sample edge-signal inputs. It should not claim live proprietary sensor integration.

Real wireless sensor-informed visualization is a future private/product lane, not public repo implementation.

## 16. Task 030 Acceptance Criteria

- [x] Visual asset system spec exists.
- [x] Task 030 artifact exists.
- [x] Reference PNG path documented.
- [x] WebP placeholder asset filenames documented.
- [x] Honey-brown/gold direction documented.
- [x] Green/blue dashboard direction rejected.
- [x] Mobile-first behavior documented.
- [x] Center-aligned layout preference documented.
- [x] Responsive breakpoints documented.
- [x] Visual inspection requirements for Task 031 documented.
- [x] Required asset list documented.
- [x] Hero/card/guide sections documented.
- [x] Public ADTC boundary documented.
- [x] No app code changed.
- [x] No images added.
- [x] No CSS/template/source files changed.
- [x] No model/runtime/metadata/download files changed.
