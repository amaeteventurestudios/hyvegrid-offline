# Task 044A Final Submission Manifest

## Repository

- SSH remote: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`
- Public-facing repository URL to verify before submission: `https://github.com/amaeteventurestudios/hyvegrid-offline`

## Branch

`phase-1-eval-harness`

## Commit

Task 044A started from:

`99031bcc873c4eab2b3344199aa2022d69a60d6b`

Use the final pushed Task 044A commit after this task completes.

## Required files

- `metadata.json`
- `download_model.sh`
- `REPORT.md`
- `SCORING.md`
- `README.md`
- `.gitignore`
- `LICENSE`

## Required artifacts

- `artifacts/demo/demo-video-script-task-042A.md`
- `artifacts/demo/local-demo-runbook-task-042A.md`
- `artifacts/eval/demo-script-runbook-task-042A.md`
- `artifacts/eval/clean-clone-audit-task-043A.md`
- `artifacts/eval/final-offline-submission-readiness-task-043A.md`
- `artifacts/eval/push-verification-task-043A.md`
- `artifacts/eval/remote-sync-repair-task-043B.md`
- `artifacts/eval/remote-sync-transport-repair-task-043C.md`
- `artifacts/eval/remote-clean-clone-audit-task-043D.md`
- `artifacts/eval/remote-submission-readiness-task-043D.md`
- `artifacts/eval/final-submission-package-checklist-task-044A.md`
- `artifacts/eval/devpost-upload-readiness-task-044A.md`

## Demo materials

- Demo script: ready
- Local demo runbook: ready
- Demo video: not confirmed in this task
- Screenshots or stills: not checked in this task

## Runtime checks

- `metadata.json` valid JSON: passed
- Official ADTC prompts present: passed
- `download_model.sh` syntax: passed
- `llama-cli` local diagnostics: passed
- App smoke check: routes loaded; `/status` exact phrase `Network required` was not present
- Model weights tracked by Git: no
- `.gitignore` excludes `model/` and `*.gguf`: yes

## Known limitations

- Devpost copy still needs final review.
- Demo video still needs recording or confirmation.
- Hausa and Swahili should remain framed as structured field-template modes that need human review.
- HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

## Not included by design

- No model weights committed.
- No Devpost submission in this task.
- No release tag in this task.
- No app, runtime, retrieval, language, metadata, report, scoring, or demo behavior changes.
- No cloud runtime dependency, external API dependency, CDN asset, remote runtime asset, Phaser, Remotion, WebGL, canvas, generated image, generated art, or animation dependency added.
- No proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims added.

## Final status

FINAL_SUBMISSION_MANIFEST_READY
