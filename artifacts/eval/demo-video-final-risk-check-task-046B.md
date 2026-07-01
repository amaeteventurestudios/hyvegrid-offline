# Task 046B Demo Video Final Risk Check

## Purpose

Final focused risk check for the HyveGrid Offline demo video recording session, consolidating the residual recording risks and their mitigations.

This task is documentation only.

## Starting state

- Branch: `phase-1-eval-harness`
- Local HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Remote HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Working tree: clean
- Origin URL: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`

## Risks

| Risk | Severity | Status | Mitigation |
|---|---:|---|---|
| Local inference is slow | Medium | OPEN | Start the Hive Health run early, keep the waiting state visible, use backup narration. Dry run was about 164.5 seconds. |
| Wrong Python environment | Medium | CONTROLLED | Activate `.venv` and run `python3 scripts/check_local_runtime.py` before recording. |
| Model path missing | High | CONTROLLED | Run diagnostics before recording and confirm local model files; do not commit model weights. |
| localhost app not running | Medium | CONTROLLED | Start `python -m app.web_app` and verify `http://127.0.0.1:8000` before recording. |
| Private files visible during recording | High | OPEN | Close unrelated windows, tabs, terminals, and desktop files before recording. |
| Video file accidentally committed | Medium | CONTROLLED | Store video outside the repo; verify `git ls-files` returns no video files; follow Task 046B file handling policy. |
| Overclaiming diagnosis | High | CONTROLLED | Use the exact safety limitation; say field guidance/triage support only. |
| Overclaiming Hausa/Swahili quality | Medium | CONTROLLED | Use the exact Hausa/Swahili caveat; no human-reviewed or native-quality claims. |
| Mentioning removed animation work | Medium | CONTROLLED | Keep the demo on the simple local guidance waiting state. |

## Conclusion

RISKS_MANAGEABLE. Remaining open risks are recording-environment hygiene and slow local inference; both have documented mitigations.