# Task 046B Demo Video File Handling

## Purpose

Define how the HyveGrid Offline final demo video file is named, stored, uploaded, and kept out of the repository. The demo video must never be committed to Git.

This task is documentation only. It does not record, edit, or upload a video, and does not change any app, test, runtime, model, retrieval, metadata, report, README, `.gitignore`, `download_model.sh`, or Devpost copy.

## Starting state

- Branch: `phase-1-eval-harness`
- Local HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Remote HEAD: `29be2f7ef3cf9ab0822d79314f1e046c0175115d`
- Working tree: clean
- Origin URL: `git@github.com:amaeteventurestudios/hyvegrid-offline.git`

## Suggested file name

```text
hyvegrid-offline-adtc-2026-demo.mp4
```

## Storage rule

Store the recorded video file outside the repository working tree. Recommended location: a Desktop or Movies folder, never inside `/Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026`.

Do not stage, add, or commit any video file (`*.mp4`, `*.mov`, `*.avi`, `*.mkv`, `*.webm`, `*.m4v`) to the repository.

## Upload destination

Upload the final video to the Devpost submission form or an external video host, then paste the public link into the Devpost demo video field. Do not commit the video binary to the repo.

## Verification commands

Before staging the Task 046B artifacts, confirm no video files are tracked or staged:

```bash
git ls-files '*.mp4' '*.mov' '*.avi' '*.mkv' '*.webm' '*.m4v'
git status --porcelain
```

Expected: `git ls-files` returns nothing. `git status` should show only the Task 046B markdown artifacts.

## Do not

- do not `git add` any video file
- do not store the video inside the repository directory
- do not link to a private/local file path in the Devpost form
- do not include private desktop files, API keys, or secrets in the recording

## Conclusion

FILE_HANDLING_POLICY_READY