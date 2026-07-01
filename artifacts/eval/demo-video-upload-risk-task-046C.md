# Task 046C Demo Video Upload Risk

## Purpose

Capture the upload-time risks for the HyveGrid Offline demo video, given that the video has not been recorded yet. This artifact is documentation only.

## Risks

| Risk | Status | Mitigation |
|---|---|---|
| video not recorded | OPEN | Record the demo using `artifacts/submission/final-demo-recording-session-plan-task-046B.md`. |
| video file accidentally committed | CONTROLLED | Store the video outside the repo; verify `git ls-files` returns no video files; follow Task 046B file handling policy. |
| video misses required proof point | OPEN | Use the Task 046C proof-point checklist during recording and review before upload. |
| video shows private desktop files | OPEN | Close unrelated windows, tabs, terminals, and desktop files before recording. |
| video overclaims diagnosis | CONTROLLED | Use the exact safety limitation; say field guidance/triage support only. |
| video overclaims Hausa/Swahili quality | CONTROLLED | Use the exact Hausa/Swahili caveat; no human-reviewed or native-quality claims. |
| video is too long | CONTROLLED | Target 2 minutes, 3 minutes hard ceiling; start Hive Health inference early. |
| upload link unavailable | OPEN | Upload to Devpost directly or a video host and capture the public link before final submission. |

## Conclusion

The dominant upload risk is that the video is not recorded yet. Once recorded, the remaining risks are manageable with the recording session plan, the proof-point checklist, and the file-handling policy.