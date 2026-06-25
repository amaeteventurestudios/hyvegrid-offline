# HyveGrid Offline Multilingual Mode Specification

Task: 027

Date: 2026-06-25

Status: planning/specification only

## 1. Purpose

Multilingual mode is part of the HyveGrid Offline demo and field-product layer. It supports the African use-case bonus, field credibility, demo video, and live defense by showing that the local app can be adapted for beekeepers and extension workers who do not work only in English.

This mode does not change the automated profiler score, GGUF telemetry, bare model evaluation path, `metadata.json`, `download_model.sh`, or model files. The ADTC scoring path remains the locked GGUF model evaluated through `llama.cpp`. Multilingual mode is a local app experience around that model, supported by controlled templates and public, challenge-safe language material.

## 2. Language Strategy

| Option | Decision | Rationale |
| --- | --- | --- |
| Yoruba | Build first | Yoruba-first gives the submission a focused Nigerian field story, keeps review scope manageable, and makes it more likely that labels, glossary terms, and caution language can be checked by a human reviewer before final submission. |
| Hausa | Later | Hausa is important for future Nigerian and West African coverage, but adding it before Yoruba is reviewed would multiply translation and quality-control risk. |
| Swahili | Later | Swahili is important for East African future reach, but it should follow the same language-pack pattern only after the first language is proven. |
| All three at once | Not now | Building Yoruba, Hausa, and Swahili together would increase implementation, review, and demo risk without improving the automated profiler score. |

Yoruba-first is lower risk and higher quality for this submission because it narrows the language surface, allows a real controlled field demo, and leaves time for human Yoruba review. A single good Yoruba flow is more defensible than three shallow or unreviewed language modes.

## 3. Design Principles

- Do not ask Granite to freestyle perfect Yoruba.
- Use controlled templates, glossary terms, structured field flows, and English fallback.
- Keep the model's role focused on field reasoning; keep localized phrasing constrained where possible.
- Preserve cautious field language in every supported language mode:
  - Possible concern
  - Check first
  - Avoid doing immediately
  - Confirm by physical inspection
  - Consult an experienced beekeeper or extension officer when needed
- Treat multilingual mode as field triage support, not certified diagnosis.
- Keep all content public-edition safe and offline.

## 4. Yoruba Mode Requirements

Yoruba mode should include:

- English/Yoruba toggle on supported demo screens.
- Yoruba UI labels for navigation, form labels, buttons, section headings, and safety notices.
- Yoruba glossary for common beekeeping, site, harvest, forage, signal, and caution terms.
- Yoruba structured field flow that prompts users for observations in a predictable order instead of open-ended translation.
- Yoruba response templates that reuse the same safe field structure across advisors.
- Yoruba demo task that can be shown in a video or live defense without requiring internet access.
- Clear fallback to English when a term, phrase, or response segment is not reviewed or cannot be expressed safely.
- Human Yoruba review before final submission, especially for caution language and any beekeeping terms that may vary by region.

Yoruba mode should prefer reviewed phrases and glossary substitutions over unrestricted model-generated Yoruba. If the system cannot produce a reviewed Yoruba answer safely, it should show the English answer with a visible fallback note.

## 5. Advisor Coverage

| Screen | Yoruba support requirement |
| --- | --- |
| Mission Control | Add English/Yoruba toggle when Yoruba implementation begins; localize screen title, advisor names, short descriptions, and status navigation. |
| Hive Health Advisor | Support Yoruba labels, structured observation prompts, glossary terms for brood, pests, activity, smell, colony strength, and cautious response templates. |
| Site Readiness Advisor | Support Yoruba labels and templates for shade, water, wind, people/livestock safety, pesticide exposure, forage, and access concerns. |
| Harvest Quality Coach | Support Yoruba labels and templates for capped frames, moisture risk, smoke contamination, clean containers, storage, and food-grade handling. |
| Forage & Pollination Guide | Support Yoruba labels and templates for crop flowering, forage gaps, pesticide timing, colony competition, and farmer coordination. |
| Hive Signal Check | Support Yoruba labels and templates for temperature, humidity, entrance activity, clustering, ventilation, water, and heat-stress caution. |
| Offline System Status | Localize user-facing status labels while preserving technical markers such as `llama.cpp`, `GGUF`, `SQLite FTS5`, `localhost`, and no-cloud/offline claims in clear form. |

The first Yoruba implementation should cover the demo-critical path before expanding every edge case. It should not remove or weaken the existing English advisor screens.

## 6. Controlled Template Plan

All Yoruba advisor responses should use a shared safe structure:

1. Field observation summary
2. Possible concern
3. Check first
4. Avoid doing immediately
5. Next safe action
6. When to consult an experienced beekeeper or extension officer
7. English fallback note

Template behavior:

- Keep section order stable across advisors.
- Use reviewed Yoruba labels for section headings.
- Use glossary-controlled terms for domain words.
- Allow English fallback inside the answer when a term is not yet reviewed.
- Avoid unsupported certainty. Use cautious phrasing such as "may indicate" and "confirm by physical inspection."
- Keep emergency or severe cases directed toward an experienced beekeeper or extension officer.

## 7. Glossary Plan

The Yoruba glossary should start as categories, then be filled and reviewed in a later implementation task.

Starter categories:

- Hive and colony terms: hive, colony, brood, queen, worker bees, entrance, comb, frame, capped brood, capped honey.
- Pest and disease pressure terms: ants, wax moth, beetles, mites, weak colony, absconding pressure, abnormal smell, dead bees.
- Site and forage terms: shade, water source, wind, pesticide, flowering crops, forage gap, mango, pepper, vegetables, farm boundary.
- Harvest and honey quality terms: capped frame, uncapped honey, moisture, fermentation, smoker, smoke contamination, clean tools, food-grade container, storage.
- Signal/status terms: temperature, humidity, low activity, clustering, ventilation, heat stress, water scarcity, entrance activity.
- Safety and caution terms: possible concern, check first, avoid immediately, confirm by physical inspection, next safe action, consult an experienced beekeeper or extension officer.

The glossary should include English source term, Yoruba reviewed term or phrase, optional plain-language explanation, advisor category, and review status.

## 8. Hausa and Swahili Future-Ready Plan

The implementation should eventually allow additional language packs, but Hausa and Swahili language packs should not be implemented now.

Future-ready structures could include:

- `language_packs/yo/` for Yoruba labels, glossary, and templates.
- `language_packs/ha/` for Hausa labels, glossary, and templates when approved later.
- `language_packs/sw/` for Swahili labels, glossary, and templates when approved later.
- A language registry that lists available, reviewed language packs.
- A fallback policy shared by all language packs.
- Per-language review metadata that records reviewer status without adding private reviewer notes.

These structures are a planning direction only. Task 027 does not create them and does not commit to implementing Hausa or Swahili before Yoruba is proven.

## 9. IP and Public-Edition Boundary

Multilingual mode must not include:

- Proprietary hardware plans
- Sensor IP
- Firmware strategy
- Private datasets
- Partner strategy
- Commercial roadmap
- Honey Flow Africa internal strategy
- Investor materials
- Patent-sensitive claims

Allowed content remains limited to public apiculture notes, public sources, open-source model components, challenge-safe code, basic local retrieval, manual/sample field inputs, and reviewed public Yoruba templates.

## 10. Future Implementation Breakdown

Task 028: Implement Yoruba UI labels, glossary, and controlled templates.

- Add the minimum source changes required for English/Yoruba toggle support.
- Add reviewed starter Yoruba labels and glossary material.
- Add controlled Yoruba response templates.
- Preserve existing English behavior.

Task 029: Yoruba advisor flow smoke tests.

- Smoke-test the Yoruba demo flow locally.
- Confirm fallback behavior.
- Confirm no cloud dependency and no raw runtime leakage.
- Record evidence for the demo path.

Task 030: Optional Hausa/Swahili scaffold only if Yoruba passes.

- Add only a scaffold for future language packs if the Yoruba path is reviewed and stable.
- Do not fill Hausa or Swahili content without proper review.
- Keep English and Yoruba behavior unchanged.

## 11. Task 027 Acceptance Criteria

- [x] Multilingual spec document exists at `specs/001-hyvegrid-offline/multilingual-mode.md`.
- [x] Yoruba-first decision is documented.
- [x] Hausa and Swahili are future-ready only.
- [x] No UI implementation was done.
- [x] No route, template, advisor source, test, runtime logic, or app behavior changes were made.
- [x] No source code changes were made.
- [x] No model files, `metadata.json`, `download_model.sh`, profiler artifacts, retrieval logic, prompt builder, or llama runtime files were changed.
- [x] No commit or push was performed.
