# Task 044B Devpost Form Fields

## Purpose

Prepare copy-paste-ready Devpost form fields for HyveGrid Offline. This task does not submit to Devpost.

## Project name

HyveGrid Offline

## Elevator pitch

HyveGrid Offline is a localhost apiculture field assistant for African beekeepers and extension workers, using local GGUF inference through llama.cpp and public local apiculture notes.

## Inspiration

Beekeepers and extension workers often need practical guidance in field conditions where internet access is limited or unreliable. HyveGrid Offline was built to show how a low-cost laptop can provide cautious apiculture triage support with a local model, local retrieval, and clear safety boundaries.

## What it does

HyveGrid Offline helps users reason through hive health, site readiness, harvest quality, forage, pollination, and simple hive signal checks. A user opens the localhost app, chooses an advisor area, enters a field question, and receives a cautious answer with retrieved local source references and a Completed locally status.

The app is designed for field guidance and triage support. It helps structure observations around possible concern, check first, avoid doing immediately, and confirm by physical inspection.

## How we built it

HyveGrid Offline is a Python local web app with a browser interface served at localhost. The local answer path uses llama.cpp with a GGUF model and public apiculture notes. The report documents SQLite/FTS5 local retrieval for the demo layer.

The project includes local runtime diagnostics for checking llama.cpp and model paths, a model download script for the GGUF file, focused tests, demo runbooks, and a remote clean clone audit. The public challenge edition keeps the runtime offline and avoids cloud runtime dependencies.

## Challenges we ran into

The main challenge was making local inference practical for an 8 GB laptop target while keeping the runtime offline. We also had to preserve cautious field guidance, avoid cloud dependencies, and keep the automated scoring path focused on the GGUF model.

Language support required careful boundaries. English remains the default, Yorùbá support is included, and Hausa and Swahili are structured field-template modes that still need human language review. We avoided claiming more language quality than the project evidence supports.

## Accomplishments

We built a local app with five advisor areas: Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, and Hive Signal Check. The browser flow can run local GGUF answers through llama.cpp, show retrieved local sources, and display Completed locally.

We added a language selector, preserved Yorùbá support, added structured Hausa and Swahili field-template modes with caveats, and verified remote clean clone readiness. The repo includes demo scripts, runbooks, runtime diagnostics, and submission-readiness audit artifacts.

## What we learned

We learned that an offline assistant needs more than a model file. It needs clear setup checks, cautious prompting, local retrieval, safety language, and evidence that the public repository can be cloned and reviewed without hidden local state.

We also learned that multilingual support should be framed honestly. A useful structured field-template mode is not the same thing as native-quality or human-reviewed translation, especially for field use.

## What is next

Public next steps include adding more public apiculture notes, expanding field review, completing human language review, improving low-resource laptop testing, and making local setup and packaging smoother.

These next steps should remain within the public challenge-edition boundary and should not include private datasets, proprietary hardware plans, sensor IP, partner strategy, investor materials, or commercial roadmap details.

## Built with

- Python
- local web app stack
- FastAPI
- HTML/CSS
- llama.cpp
- GGUF
- SQLite/local retrieval
- public apiculture notes

## Repository

SSH:

```text
git@github.com:amaeteventurestudios/hyvegrid-offline.git
```

Public HTTPS display version:

```text
https://github.com/amaeteventurestudios/hyvegrid-offline
```

## Branch

```text
phase-1-eval-harness
```

## Commit

To be finalized after Task 044B commit.

## Demo video status

Demo script and local runbook are ready. Video recording still needs to be completed unless the user has already recorded it.

## Run instructions summary

1. Clone the repo.
2. Run `download_model.sh`.
3. Activate the virtual environment.
4. Run local diagnostics.
5. Start the local app.
6. Open localhost in the browser.

Use `README.md` as the source of truth for run instructions.

## Safety limitation field

HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

## Public edition boundary field

This is a public challenge edition. It does not include proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims.
