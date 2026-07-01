# Task 043D Remote Clean Clone Audit

## Purpose

Verify that the remote `phase-1-eval-harness` branch can be cloned cleanly from GitHub after the SSH sync repair, and that the public ADTC 2026 challenge repository is ready for the final submission packaging step without relying on local-only files.

This task was documentation and audit only. No app behavior, runtime behavior, metadata, model files, reports, tests, demo files, or scoring files were changed.

## Starting state

- Local branch: `phase-1-eval-harness`
- Local HEAD: `fb020c50c8084a4396937aa91b9f4af04cbae56b`
- Remote HEAD: `fb020c50c8084a4396937aa91b9f4af04cbae56b`
- Working tree: clean
- Origin URL: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`

## Remote clean clone

- Clone command: `git clone --branch phase-1-eval-harness git@github.com:amaeteventurestudios/hyvegrid-offline.git hyvegrid-offline-adtc-2026-remote-clean`
- Clone location: `/tmp/hyvegrid-task-043D-remote-clone/hyvegrid-offline-adtc-2026-remote-clean`
- Clone result: succeeded from GitHub over SSH. No local fallback clone was used.

## Remote clone Git checks

- Branch: `phase-1-eval-harness`
- HEAD: `fb020c50c8084a4396937aa91b9f4af04cbae56b`
- Working tree: clean
- Recent commits:
  - `fb020c5 Repair remote sync transport for Task 043C`
  - `ed1d873 Document remote sync repair for Task 043B`
  - `a0b4c49 Add clean clone audit for Task 043A`
  - `7cab725 Add demo script and local runbook for Task 042A`
  - `c7c713f Update REPORT final evidence Task 041A`
  - `d91293a Add final advisor flow QA Task 040A`
  - `f6ab035 Add African language QA and review export Task 039D`
  - `2d57874 Add African language structured templates Task 039C`

## Required root files

All required root files were present in the remote clean clone:

- `metadata.json`
- `download_model.sh`
- `REPORT.md`
- `SCORING.md`
- `README.md`
- `.gitignore`

## Required directories

All required directories were present in the remote clean clone:

- `app/`
- `data/`
- `scripts/`
- `tests/`
- `artifacts/`
- `specs/`

## Demo and audit artifacts

All required demo and recent audit artifacts were present:

- `artifacts/demo/demo-video-script-task-042A.md`
- `artifacts/demo/local-demo-runbook-task-042A.md`
- `artifacts/eval/demo-script-runbook-task-042A.md`
- `artifacts/eval/clean-clone-audit-task-043A.md`
- `artifacts/eval/final-offline-submission-readiness-task-043A.md`
- `artifacts/eval/push-verification-task-043A.md`
- `artifacts/eval/remote-sync-repair-task-043B.md`
- `artifacts/eval/remote-sync-transport-repair-task-043C.md`

## Model and gitignore safety

- `.gguf` files found in remote clean clone: none
- `model/` files found in remote clean clone: none
- Tracked `model/` or `.gguf` files: none
- `.gitignore` includes:
  - `model/`
  - `*.gguf`

Model weights remain uncommitted and excluded from Git.

## Disallowed dependency and claim scan

Scan command covered cloud/vendor terms, animation stack terms, generated-art references, and prohibited product-claim terms across the remote clean clone, excluding `.git`, `.venv`, `model`, and binary image files.

Classified findings:

- Safe constraint language:
  - Demo and evaluation artifacts repeatedly state that no cloud API, external API, CDN, Phaser, Remotion, WebGL, canvas, generated art dependency, live sensor claim, real-time sensor claim, digital twin claim, or autonomous-agent claim was added.
  - Runtime and CLI comments describe local/offline operation and explicitly avoid cloud calls.
  - `REPORT.md` preserves offline/local positioning and states that no external API dependency is required.
- Warning:
  - Historical walkthrough and sprite audit artifacts still mention sprites, animation, WebGL, canvas, Phaser, CDN, and related terms as past constraints, past experiments, or absence checks.
  - These are retained as audit history. Task 038A removed the live animation layer, and Task 042A directs the demo to use the simple local guidance waiting state rather than continuing animation work.
- Failure:
  - No active cloud runtime dependency, remote service dependency, animation stack dependency, generated-art dependency, or prohibited product claim was found.

## Metadata check

- `metadata.json` parsed as valid JSON.
- Official Hive Health prompt was present:
  - `A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?`
- Official Site Readiness prompt was present:
  - `An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?`

## download_model.sh check

- `bash -n download_model.sh` passed.
- The script keeps the model target at `model.gguf`.
- The script downloads the IBM Granite GGUF only when missing.
- The script verifies the expected SHA256.
- The script was inspected only. No model download was run.

## Local runtime diagnostics

Command run from the working repo:

```bash
source .venv/bin/activate
python3 scripts/check_local_runtime.py
```

Result:

- Platform: `macOS-12.7.6-x86_64-i386-64bit`
- Python: `.venv/bin/python3`
- `LLAMA_BIN` set: `False`
- Resolved llama-cli: `/Users/amaeteumanah/llama.cpp/build/bin/llama-cli`
- llama-cli exists: `True`
- llama-cli executable: `True`
- Intel macOS CPU-only fallback applies: `True`
- Expected model files exist:
  - `model/hyvegrid-offline.gguf`
  - `model/granite-3.3-2b-instruct-Q4_K_M.gguf`
  - `model.gguf`

## Optional app smoke check

Command run from the working repo:

```bash
source .venv/bin/activate
python -m app.web_app
```

Smoke checks:

- `/`: OK. Mission Control and all advisor/status links were present.
- `/status`: OK. Offline System Status was present.
- `/advisor/hive-health`: OK. Hive Health Advisor and language options `English`, `Yorùbá`, `Hausa`, and `Swahili` were present.

The server was stopped after the smoke check.

## Issues found

No blocking issues were found.

Historical artifacts still contain references to sprite and animation work because they document earlier completed tasks. Those references are warnings for context only, not active dependencies or current demo behavior.

## Conclusion

REMOTE_CLEAN_CLONE_PASSED_WITH_WARNINGS
