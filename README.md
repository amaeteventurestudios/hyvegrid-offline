# HyveGrid Offline

HyveGrid Offline is a local AI field assistant for African beekeeping operations.

It helps beekeepers, extension workers, and field operators reason through hive health, site readiness, honey quality, forage, pollination, and simple hive signal patterns without cloud access.

## Challenge edition

This repository is the public Africa Deep Tech Challenge 2026 edition of HyveGrid Offline.

This edition is intentionally limited to public, challenge-safe material. It does not include proprietary hardware plans, sensor IP, private datasets, Honey Flow Africa internal strategy, commercial roadmap material, partner strategy, investor materials, API keys, or credentials.

## Core competition priority

ADTC's automated scoring is model-centric. The GGUF model's own accuracy, speed, RAM usage, thermal behavior, and crash resistance matter first.

The local app, RAG layer, public apiculture notes, and Yoruba mode support the demo, documentation, African use-case story, and live evaluation.

Read `SCORING.md` before building.

## Runtime target

- Offline local execution
- llama.cpp runtime
- GGUF model format
- Target model path: `model/hyvegrid-offline.gguf`
- SQLite local retrieval for demo layer
- English first for scoring
- Yoruba support for field usability and African use-case strength
- Target hardware: low-cost Ubuntu laptop with 8 GB RAM

## Planned modules

1. Mission Control
2. Hive Health Advisor
3. Site Readiness Advisor
4. Harvest Quality Coach
5. Forage & Pollination Guide
6. Hive Signal Check
7. Offline System Status

## Current build status

- [x] Repo skeleton created
- [x] SCORING.md added
- [x] Build plan placed under `specs/001-hyvegrid-offline/plan.md`
- [x] Model candidate matrix created
- [x] metadata.json starter created
- [x] download_model.sh starter created
- [ ] Model candidates benchmarked
- [ ] Scoring model selected
- [ ] Public apiculture knowledge base added
- [ ] CLI demo layer built
- [ ] SQLite FTS5 retrieval added
- [ ] Yoruba controlled field mode added
- [ ] Local web UI added
- [ ] Profiler results recorded
- [ ] REPORT.md completed

## Repository layout

```text
hyvegrid-offline-adtc-2026/
  metadata.json
  download_model.sh
  REPORT.md
  SCORING.md
  README.md
  .gitignore
  LICENSE
  model/

  app/
  data/
  scripts/
  tests/
  artifacts/

  specs/
    001-hyvegrid-offline/
      spec.md
      plan.md
      tasks.md
      research.md
      data-model.md
      quickstart.md