# Task 045A Demo Recording Risk Register

## Purpose

List practical risks for recording the final HyveGrid Offline demo video and the recommended mitigation for each.

## Risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Local inference is slow | Medium | Start the Hive Health run early, keep the waiting state visible, and use backup narration. |
| Wrong Python environment | Medium | Activate `.venv` and run `python3 scripts/check_local_runtime.py` before recording. |
| Model path missing | High | Run diagnostics before recording and confirm local model files are present; do not add model files to Git. |
| localhost app not running | Medium | Start `python -m app.web_app` and verify `http://127.0.0.1:8000` before recording. |
| private files visible during recording | High | Close unrelated windows, tabs, terminals, and desktop files before recording. |
| overclaiming diagnosis | High | Use the exact safety paragraph and say field guidance/triage support only. |
| overclaiming Hausa/Swahili quality | Medium | Use the exact Hausa/Swahili caveat and avoid human-reviewed or native-quality claims. |
| mentioning removed animation work | Medium | Keep the demo on the simple local guidance waiting state and do not mention removed visual experiments. |

## Conclusion

The main recording risks are manageable. The most important operational risk is slow local CPU inference; the dry run completed successfully but took about 164.5 seconds.
