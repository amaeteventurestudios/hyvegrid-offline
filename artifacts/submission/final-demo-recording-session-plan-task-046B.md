# Task 046B Final Demo Recording Session Plan

## Purpose

Consolidate the HyveGrid Offline final demo recording into one operational session plan. This plan references the existing recording package without duplicating or altering it, and is the single document to follow during the actual recording session.

This task is documentation only. It does not record, edit, or upload a video, and does not change app behavior, runtime behavior, model behavior, retrieval behavior, metadata, report numbers, demo scripts, or Devpost copy.

## Starting state

- Branch: `phase-1-eval-harness`
- Local HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Remote HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Working tree: clean
- Origin URL: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`

## Source package

| Component | Source artifact |
|---|---|
| Presenter script | `artifacts/demo/demo-video-script-task-042A.md` |
| Local runbook | `artifacts/demo/local-demo-runbook-task-042A.md` |
| Shot list | `artifacts/submission/demo-video-recording-shot-list-task-044B.md` |
| Final recording guide | `artifacts/demo/final-demo-recording-guide-task-045A.md` |
| Dry-run evidence | `artifacts/eval/demo-recording-dry-run-evidence-task-045A.md` |
| Risk register | `artifacts/eval/demo-recording-risk-register-task-045A.md` |
| Upload checklist | `artifacts/submission/demo-video-upload-checklist-task-045A.md` |

## Recording target

2 minutes recommended, 3 minutes hard ceiling if local inference is slow.

Known warning: the Task 045A dry run completed the Hive Health local answer in about 164.5 seconds. Start the live inference as early as practical and use backup narration while the local answer is prepared.

## Pre-recording setup

1. Open a clean terminal.
2. Close unrelated browser tabs, terminals, and desktop files.
3. Activate the local environment.
4. Run diagnostics.
5. Start the local app.
6. Open localhost in the browser.

## Exact commands

```bash
cd /Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026
source .venv/bin/activate
python3 scripts/check_local_runtime.py
python -m app.web_app
```

## Local URL

```text
http://127.0.0.1:8000
```

## Shot order

1. Terminal and local app startup
2. Mission Control
3. Offline/local positioning (localhost URL bar)
4. Hive Health Advisor live run
5. Waiting state
6. Answer, retrieved local sources, Completed locally.
7. Site Readiness Advisor quick run or mention
8. Language selector
9. Hausa/Swahili human-review-needed caveat
10. Offline System Status (Network required: No)
11. Safety limitation and close

## Main prompt to paste

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

## Second prompt to paste

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

## Backup narration if inference is slow

```text
This pause is expected on a local CPU path. The app is preparing local guidance using the GGUF model through llama.cpp and local retrieved apiculture notes. I will keep the screen on the waiting state so the offline flow is visible.
```

## Required on-screen proof points

- [ ] localhost URL visible
- [ ] Mission Control visible
- [ ] five advisor areas visible
- [ ] Hive Health official prompt submitted
- [ ] local guidance waiting state shown
- [ ] local answer returned
- [ ] retrieved local sources shown
- [ ] Completed locally. shown
- [ ] Site Readiness official prompt shown or narrated
- [ ] language selector visible (English, Yorùbá, Hausa, Swahili)
- [ ] Hausa/Swahili human-review-needed caveat stated
- [ ] Offline System Status shown with Network required: No
- [ ] safety limitation stated

## Must not show or say

- cloud model dependency
- external API dependency
- live sensor support
- real-time sensor readings
- autonomous agents
- digital twin functionality
- certified disease diagnosis claim
- human-reviewed Hausa
- human-reviewed Swahili
- native-quality Hausa
- native-quality Swahili
- proprietary hardware plans
- sensor IP
- firmware strategy
- private datasets
- commercial roadmap
- partner strategy
- investor materials
- patent-sensitive claims
- removed animation work

## Safety limitation

HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.

## Hausa/Swahili caveat

Hausa and Swahili are included as structured field-template modes for demonstration and reviewer evaluation. They are not claimed as human-reviewed or native-quality translations.

## Public challenge edition boundary

This is a public challenge edition. It does not include proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims.

## Conclusion

SESSION_PLAN_READY