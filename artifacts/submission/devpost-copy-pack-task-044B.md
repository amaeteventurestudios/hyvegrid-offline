# Task 044B Devpost Copy Pack

## Purpose

Prepare copy-paste-ready Devpost submission text for HyveGrid Offline. This task prepares submission text only. It does not submit to Devpost.

## Project name

HyveGrid Offline

## One-line description

Offline apiculture field guidance for African beekeepers using local GGUF inference and public notes.

## Short description

HyveGrid Offline is a local apiculture intelligence assistant for African beekeepers and extension workers. It runs on a low-cost laptop at localhost, uses a local GGUF model through llama.cpp, retrieves public local apiculture notes, and supports field triage for hive health, site readiness, harvest quality, forage, pollination, and simple hive signal checks.

The public challenge edition is designed for offline review without a cloud model or external API during judged runtime.

## Long description

Many beekeepers and extension workers need practical field support in places where internet access is limited, unreliable, or too costly for routine use. HyveGrid Offline focuses on field triage and cautious inspection support for African apiculture contexts.

HyveGrid Offline is a localhost app that helps users ask field questions about hive health, site readiness, honey quality, forage, pollination, and simple hive signal patterns. It organizes the experience through Mission Control and five advisor areas: Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, and Hive Signal Check.

The runtime is local. The answer path uses a local GGUF model through llama.cpp, local retrieval over public apiculture notes, and a local browser interface served from the laptop. The app is designed so no cloud model or external API is required during judged runtime after local setup and model availability.

The demo layer uses local retrieval over public apiculture notes, including SQLite/FTS5 retrieval where documented in the project report. Answers show retrieved local sources and a completion status so reviewers can see the local path rather than a remote service.

English remains the default. Yorùbá is preserved as a supported African language layer. Hausa and Swahili are included as structured field-template modes for demonstration and reviewer evaluation. They are not claimed as human-reviewed or native-quality translations.

HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

This is a public challenge edition. It does not include proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims.

## What it does

HyveGrid Offline gives a beekeeper, field operator, or extension worker a local question-and-answer workspace for practical apiculture concerns. A user selects an advisor area, enters a field observation or site question, and receives a cautious structured answer with local source references.

The app emphasizes phrases such as possible concern, check first, avoid doing immediately, confirm by physical inspection, and consult an experienced beekeeper or extension officer when needed. It is built for field guidance and triage support, not final certification or disease confirmation.

## How it works

HyveGrid Offline runs as a local web app at localhost. The user opens the browser interface on the laptop, chooses an advisor, submits a field question, and the app prepares local guidance.

The answer path uses a local GGUF model through llama.cpp. The app also retrieves from public local apiculture notes, with SQLite/FTS5 local retrieval documented in the report for the demo layer.

The advisor flows cover hive health, site readiness, harvest quality, forage and pollination, and simple hive signal checks. The Offline System Status page summarizes the local runtime positioning for reviewers.

## African use case

African beekeepers and extension workers often need practical, low-cost field guidance in conditions where cloud access may be unavailable. HyveGrid Offline demonstrates how a small local model, local notes, and cautious templates can support inspection conversations without requiring a remote service during judged runtime.

The project keeps the language layer careful: English is the default, Yorùbá support is included, and Hausa and Swahili are structured field-template modes that need human language review before field deployment.

## Offline runtime

HyveGrid Offline is designed around local runtime constraints. The app runs at localhost, uses llama.cpp, and keeps the model format as GGUF. No cloud model or external API is required during judged runtime after local setup and model availability.

## Language support

- English is the default.
- Yorùbá is preserved as a supported African language layer.
- Hausa is included as a structured field-template mode for demonstration and reviewer evaluation.
- Swahili is included as a structured field-template mode for demonstration and reviewer evaluation.

Hausa and Swahili are included as structured field-template modes for demonstration and reviewer evaluation. They are not claimed as human-reviewed or native-quality translations.

## Safety and limitations

HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

The system should be used to organize observations, check likely next steps, and support field conversations. It should not replace physical inspection, local expertise, or professional extension guidance.

## Public challenge edition boundary

This is a public challenge edition. It does not include proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims.

## Demo video narration short version

This is HyveGrid Offline, the public ADTC 2026 challenge edition. It is a local apiculture intelligence assistant for African beekeepers and extension workers. The app runs locally at localhost. The answer path uses a local GGUF model through llama.cpp and local retrieved apiculture notes, with no cloud model or external API required during the demo. Mission Control organizes five advisor areas: Hive Health, Site Readiness, Harvest Quality, Forage and Pollination, and Hive Signal Check. I will run the Hive Health Advisor with the official prompt, show the local waiting state, then show the returned answer, retrieved sources, and Completed locally status. HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool.

## Demo video narration full version

This is HyveGrid Offline, the public ADTC 2026 challenge edition. It is a local, offline apiculture intelligence assistant for African beekeepers and extension workers.

The app is running on this laptop at localhost. The answer path uses a local GGUF model through llama.cpp and local retrieved apiculture notes. No cloud model or external API is needed during the demo.

Mission Control organizes five field-support areas: Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, and Hive Signal Check. Each area keeps the same local pattern: a field question, local retrieval, local GGUF inference, retrieved sources, and a completion status.

For the main live run, I will use the Hive Health Advisor with the first official prompt. The app retrieves local apiculture notes, builds the prompt locally, and runs the local model through llama.cpp. On a CPU-only machine, the first answer can take a little time. That wait is part of the offline tradeoff.

When the answer returns, I will show the cautious field guidance, the retrieved local sources, and the Completed locally status. The answer should help the user think in terms of possible concern, check first, avoid doing immediately, and confirm by physical inspection.

The language selector keeps English as the default and includes Yorùbá support. Hausa and Swahili are structured field-template modes for demonstration and reviewer evaluation, with human review still needed before field deployment.

HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

## What to avoid saying during demo

- Do not claim a certified disease diagnosis.
- Do not claim live sensor support.
- Do not claim real-time sensor readings.
- Do not claim autonomous agents.
- Do not claim digital twin functionality.
- Do not claim proprietary hardware.
- Do not claim a deployed partner network.
- Do not claim investor traction.
- Do not claim a commercial roadmap.
- Do not claim cloud service dependency.
- Do not claim production medical or agricultural certification.
- Do not claim native-quality Hausa.
- Do not claim native-quality Swahili.
- Do not claim human-reviewed Hausa.
- Do not claim human-reviewed Swahili.

## Suggested tags

- offline AI
- apiculture
- agriculture
- Africa
- llama.cpp
- GGUF
- local-first
- field guidance
- beekeeping
- Yorùbá

## Final copy review notes

- Devpost was not submitted in this task.
- Demo video recording still needs to be completed unless already recorded separately.
- Final Devpost fields should be reviewed against official ADTC upload requirements before pressing submit.
- Keep Hausa and Swahili caveats visible.
- Keep the safety paragraph and public challenge edition boundary intact.
