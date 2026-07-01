# Task 044A Devpost Upload Readiness

## Purpose

Prepare factual Devpost upload-readiness notes for HyveGrid Offline before final copy review and submission.

## Do not submit yet

This artifact prepares the submission. It does not confirm that Devpost was submitted.

## Upload readiness status

READY WITH WARNINGS

Warnings: the demo video still needs to be recorded or confirmed, final Devpost copy still needs review, and official ADTC upload requirements should be checked before pressing submit.

## Devpost items to prepare

| Item | Status | Source or evidence |
|---|---:|---|
| Project name | READY | HyveGrid Offline |
| Short description | DRAFT READY | See recommended summary below. |
| Long description | READY FOR COPY EDIT | `REPORT.md` and `README.md` |
| GitHub repository URL | READY | `git@github.com:amaeteventurestudios/hyvegrid-offline.git`; public-facing URL should be `https://github.com/amaeteventurestudios/hyvegrid-offline` if the repo is public. |
| Branch or commit to submit | READY | Branch `phase-1-eval-harness`, starting commit for this task `99031bcc873c4eab2b3344199aa2022d69a60d6b`; final Task 044A commit should be used after this task is pushed. |
| Demo video | WARNING | Task 042A script exists; video still needs recording unless already done. |
| How to run | READY | `README.md` and `artifacts/demo/local-demo-runbook-task-042A.md` |
| Model download instructions | READY | `download_model.sh` |
| Technical report | READY | `REPORT.md` |
| Offline runtime explanation | READY | `REPORT.md`, `README.md`, and Task 042A demo script |
| African use case explanation | READY | `REPORT.md`, `README.md`, and Task 042A demo script |
| Safety limitations | READY | `REPORT.md` and Task 042A demo script |
| Screenshots or video stills | NOT CHECKED | Not required in this task unless already available. |

## Recommended Devpost project summary draft

HyveGrid Offline is an offline apiculture intelligence assistant for African beekeepers and extension workers. It runs as a localhost app and uses a local GGUF model through llama.cpp with local public apiculture notes. The app supports English and Yorùbá, with Hausa and Swahili provided as structured field-template modes that still need human language review. HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

## Recommended Devpost technical summary draft

HyveGrid Offline is a Python local web app designed for offline use on an 8 GB laptop target. The answer path uses llama.cpp with a GGUF model and local retrieval over public apiculture notes. The app includes local runtime diagnostics, model download verification, focused tests, demo runbooks, and remote clean clone evidence. The public challenge edition has no cloud runtime dependency and does not require internet access during judged runtime after setup.

## Recommended demo video notes

Summarize the Task 042A demo flow:

1. Start the local app at localhost.
2. Show Mission Control.
3. Open Hive Health Advisor and submit the official prompt.
4. Show retrieved sources.
5. Show `Completed locally.`
6. Mention Site Readiness Advisor and its official prompt.
7. Show the language selector, with Yorùbá support and Hausa/Swahili structured modes needing human review.
8. Show Offline System Status.
9. Close with the safety limitation: field guidance and triage support, not certified disease diagnosis.

## Submission warnings

- Do not submit to Devpost until the final copy is reviewed.
- Demo video recording is not confirmed in this task.
- Check official ADTC template and upload requirements before pressing submit.
- Do not include private IP, commercial strategy, partner strategy, investor materials, sensor IP, firmware strategy, private datasets, or patent-sensitive claims.
- Do not claim live sensor support, real-time sensor readings, autonomous agents, digital twin functionality, or certified disease diagnosis.
- Keep Hausa and Swahili framed as structured modes that need human review.

## Final pre-submit checklist

| Check | Status | Notes |
|---|---:|---|
| Remote branch synced | PASS | Local and remote matched at start of Task 044A. |
| Clean clone verified | PASS | Task 043D verified remote clean clone. |
| Required files present | PASS | Root files and required directories found. |
| Runtime diagnostics passed | PASS | `scripts/check_local_runtime.py` passed locally. |
| Demo script ready | PASS | Task 042A demo script exists. |
| Demo video recorded | WARNING | Not confirmed in this task. |
| Devpost copy reviewed | WARNING | Next task should prepare and review final copy. |
| IP boundary reviewed | PASS | Claim/dependency scan found no active prohibited claim. |
| Safety language reviewed | PASS | Field triage and physical inspection language preserved. |
| Final commit selected | PENDING | Use the final pushed Task 044A commit after this task completes. |

## Conclusion

HyveGrid Offline is ready for Devpost copy preparation, not direct submission. The repository and evidence package are in good shape, with demo video and final copy review still pending.

Final status:

DEVPOST_UPLOAD_READINESS_PREPARED
