# Task 045A Demo Recording Dry Run Evidence

## Purpose

Record the Task 045A dry run evidence for the final HyveGrid Offline demo recording package. This artifact documents checks only. It does not record or edit a final video.

## Starting state

- Branch: `phase-1-eval-harness`
- Local HEAD: `075b2682d54c61419a9a9402510e411c3c704985`
- Remote HEAD: `075b2682d54c61419a9a9402510e411c3c704985`
- Working tree: clean
- Origin URL: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`

## Source files reviewed

- `artifacts/demo/demo-video-script-task-042A.md`
- `artifacts/demo/local-demo-runbook-task-042A.md`
- `artifacts/submission/demo-video-recording-shot-list-task-044B.md`
- `artifacts/submission/devpost-copy-pack-task-044B.md`
- `artifacts/submission/devpost-form-fields-task-044B.md`
- `artifacts/eval/devpost-copy-review-task-044B.md`
- `README.md`
- `REPORT.md`
- `metadata.json`

## Fact verification

| Check | Status | Evidence |
|---|---:|---|
| metadata.json valid | PASS | `python3 -m json.tool metadata.json` passed. |
| Hive Health official prompt present | PASS | Prompt found in `metadata.json`. |
| Site Readiness official prompt present | PASS | Prompt found in `metadata.json`. |
| localhost positioning supported | PASS | README, REPORT, Task 042A, and Task 044B copy reference localhost/local app positioning. |
| llama.cpp positioning supported | PASS | README, REPORT, metadata, Task 042A, and Task 044B copy reference llama.cpp. |
| GGUF positioning supported | PASS | README, REPORT, metadata, Task 042A, and Task 044B copy reference GGUF. |
| SQLite/local retrieval positioning supported | PASS | README and REPORT document SQLite/local retrieval; demo/copy artifacts reference retrieved local notes. |
| language support documented | PASS | English, Yorùbá, Hausa, and Swahili are documented with Hausa/Swahili caveats. |
| safety limitation documented | PASS | Task 042A and Task 044B include the required safety language. |

## Runtime diagnostics

- Command: `source .venv/bin/activate && python3 scripts/check_local_runtime.py`
- Result: PASS
- Notes:
  - Resolved llama-cli: `/Users/amaeteumanah/llama.cpp/build/bin/llama-cli`
  - llama-cli exists: `True`
  - llama-cli executable: `True`
  - Intel macOS CPU-only fallback applies: `True`
  - Expected local model files were present, including `model.gguf`.

## App smoke check

| Route or screen | Status | Evidence |
|---|---:|---|
| / | PASS | Mission Control, five advisor areas, and Offline System Status link were present. |
| /status | PASS WITH WARNING | Route returned 200 and showed Offline System Status, Local, llama.cpp, and GGUF. Exact phrase `Network required` was still absent. |
| /advisor/hive-health | PASS | Hive Health Advisor and language selector labels were present. |
| Site Readiness Advisor | PASS | `/advisor/site-readiness` returned 200 and displayed the route. |
| Harvest Quality Coach | PASS | `/advisor/harvest-quality` returned 200 and displayed the route. |
| Forage & Pollination Guide | PASS | `/advisor/forage-pollination` returned 200 and displayed the route. |
| Hive Signal Check | PASS | `/advisor/hive-signal` returned 200 and displayed the route. |

## Demo dry run

| Demo item | Status | Evidence |
|---|---:|---|
| localhost visible | PASS | Local server ran at `http://127.0.0.1:8000`. |
| Mission Control visible | PASS | `/` route check passed. |
| five advisor areas visible | PASS | Mission Control route contained all five advisor names. |
| Hive Health prompt ready | PASS | Exact prompt confirmed in metadata and guide. |
| Hive Health answer completed locally | PASS | Web form POST to `/advisor/hive-health` completed in about 164.5 seconds. |
| retrieved sources visible | PASS | Returned page contained source/retrieval content. |
| Completed locally visible | PASS | Returned page contained `Completed locally.` |
| Site Readiness prompt ready | PASS | Exact prompt confirmed in metadata and guide. |
| language selector visible | PASS | English, Yorùbá, Hausa, and Swahili labels were present on advisor routes. |
| Hausa/Swahili caveat visible or documented | PASS | Task 042A and Task 044B document human-review-needed caveats; recording guide repeats the caveat. |
| Offline System Status visible | PASS | `/status` route returned 200 and showed offline/local runtime positioning. |
| safety limitation ready | PASS | Required safety paragraph is included in recording and upload artifacts. |

Hive Health dry-run checks:

- `answer`: `True`
- `Completed locally.`: `True`
- `sources`: `True`
- no certified diagnosis claim in returned page: `True`
- possible concern/check/avoid style language present: `True`
- local runtime error absent: `True`

## Known issues or warnings

- The Hive Health local answer completed successfully, but took about 164.5 seconds on the local CPU path. The final recording should start inference early and use backup narration while waiting.
- Task 044A's non-blocking `/status` wording mismatch remains: the exact phrase `Network required` was not present. The status route still loaded and showed local/offline runtime positioning.
- The Site Readiness prompt was verified as ready and the route loaded, but a second live inference run was not performed in this dry run to keep the recording package check short.

## Conclusion

DEMO_DRY_RUN_PASSED_WITH_WARNINGS
