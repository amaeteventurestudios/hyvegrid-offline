# HyveGrid Offline WebP Placeholder Assets

Task: 031A

These are local WebP placeholder assets for the HyveGrid Offline public ADTC edition. They are lightweight generated graphics for future Mission Control and advisor page visual refresh work.

The final app should render important text as real HTML, not baked into images. These assets are intended for backgrounds, marks, icons, cards, and illustrative panels.

Visual direction: honey-brown, dark amber, golden-brown, gold/yellow, cream/off-white, and near-black. These placeholders intentionally avoid the earlier green dashboard direction and avoid a generic blue dashboard direction.

Public-edition safety: these assets are generic apiculture and offline-system placeholders. They do not represent proprietary sensor design, hardware plans, firmware strategy, wireless architecture, private field data, partner/customer/pilot data, commercial roadmap, investor material, or patent-sensitive diagrams.

Future tasks will wire these assets into Mission Control and advisor pages.

## Placeholder Files

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

## Task 032 Walkthrough Board

Source image:

- `source/walkthrough-apiary-board.png`

Generated WebP:

- `walkthrough-apiary-board.webp`

Conversion method:

- Converted locally with Pillow in a temporary `/tmp` virtual environment.
- Pillow was not added to `requirements.txt`.
- Command shape: open the PNG, convert to RGB, save as WebP with quality 82 and method 6.

Runtime notes:

- The board is a local static asset served by the offline web app.
- No CDN, hotlink, external image, or internet runtime dependency is used.
- The source background is intended to contain no people or animals.
- Moving keeper, bee, ant, and checklist markers are separate HTML/CSS/vanilla JavaScript overlays.
- The keeper marker is a scripted walkthrough marker, not an autonomous agent.
