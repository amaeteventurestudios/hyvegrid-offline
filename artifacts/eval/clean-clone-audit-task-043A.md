# Task 043A Clean Clone Audit

## Purpose

Verify that HyveGrid Offline can be checked out cleanly, inspected safely, started locally, and presented without hidden local-state assumptions.

This is an audit artifact only. No app behavior, runtime behavior, model behavior, retrieval behavior, language behavior, prompts, or metadata were changed.

## Audit source

Local clean clone fallback audit.

Remote clean clone was attempted first and succeeded technically, but the remote branch was stale and did not contain Task 042A. The current Task 042A state was therefore audited through a local clean clone fallback. This fallback proves local repository consistency, not remote availability.

## Local repo before audit

- Branch: `phase-1-eval-harness`
- Local HEAD: `7cab7250ca5b11b433df6e0fdae79066cfbb2951`
- Remote HEAD: `8786b8975a89b3d5b4e2b3ed8f612aa477e65026`
- Task 042A commit present on remote: no

Remote verification and push ambiguity are documented in:

```text
artifacts/eval/push-verification-task-043A.md
```

## Clean clone location

Remote clone location:

```text
/tmp/hyvegrid-task-043A-audit/hyvegrid-offline-adtc-2026-clean
```

Remote clone result:

```text
8786b8975a89b3d5b4e2b3ed8f612aa477e65026
8786b89 Refresh advisor page visual design for Task 031C
```

Local clean clone fallback location:

```text
/tmp/hyvegrid-task-043A-audit/hyvegrid-offline-adtc-2026-local-clean
```

Local fallback clone result:

```text
7cab7250ca5b11b433df6e0fdae79066cfbb2951
7cab725 Add demo script and local runbook for Task 042A
```

## Git checks

Commands run in the local clean clone fallback:

```bash
git status --short
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git log --oneline -8
```

Results:

- Working tree: clean
- Branch: `phase-1-eval-harness`
- HEAD: `7cab7250ca5b11b433df6e0fdae79066cfbb2951`
- Latest commit: `7cab725 Add demo script and local runbook for Task 042A`
- Recent history includes Tasks 038D through 042A.

## Required root files

Checked in local clean clone fallback:

| File | Result |
|---|---:|
| `metadata.json` | OK |
| `download_model.sh` | OK |
| `REPORT.md` | OK |
| `SCORING.md` | OK |
| `README.md` | OK |
| `.gitignore` | OK |

## Required directories

Checked in local clean clone fallback:

| Directory | Result |
|---|---:|
| `app/` | OK |
| `data/` | OK |
| `scripts/` | OK |
| `tests/` | OK |
| `artifacts/` | OK |
| `specs/` | OK |

## Demo artifacts

Checked in local clean clone fallback:

| Artifact | Result |
|---|---:|
| `artifacts/demo/demo-video-script-task-042A.md` | OK |
| `artifacts/demo/local-demo-runbook-task-042A.md` | OK |
| `artifacts/eval/demo-script-runbook-task-042A.md` | OK |

## Model and gitignore safety

Commands run:

```bash
find . -name "*.gguf" -o -path "./model/*"
git ls-files | grep -E '(^model/|\.gguf$)' || true
grep -n "gguf\|model/" .gitignore || true
```

Results:

- No `.gguf` files found in the clean clone.
- No `model/` files or `.gguf` files are tracked by git.
- `.gitignore` contains:

```text
15:model/
16:*.gguf
```

Conclusion: model weights are not committed, and `model/` plus `.gguf` files are ignored.

## Disallowed dependency and claim scan

Command run:

```bash
grep -RInE "OpenAI|Claude|Anthropic|Supabase|Vercel|CDN|cloud API|external API|Phaser|Remotion|WebGL|canvas|sprite|sprites|generated art|digital twin|autonomous agent|real-time sensor|live sensor" . \
  --exclude-dir=.git \
  --exclude-dir=.venv \
  --exclude-dir=model \
  --exclude='*.png' \
  --exclude='*.jpg' \
  --exclude='*.jpeg' \
  --exclude='*.webp' || true
```

### Safe constraint language

The scan found many explicit constraints and negative claims such as:

- no cloud or external API dependency
- no CDN assets
- no Phaser, WebGL, canvas, or Remotion
- no live sensor, real-time sensor, autonomous agent, or digital twin claim
- no generated art or animation dependency

These appear in audit artifacts, demo docs, REPORT notes, and specs as safety boundaries.

### Warning

Historical artifacts from Tasks 031E through 038A still mention the earlier walkthrough/sprite experiment and its later removal. This is historical evidence, not current planned work. The current demo script and runbook do not restart or present that work as planned.

The scan also found test assertions referencing removed sprite asset names. These are safe because the tests assert those assets and animation classes are absent from the current waiting state.

### Failure

No failure found. The scan did not identify an active runtime dependency or product claim for OpenAI, Claude, Anthropic, Supabase, Vercel, CDN, cloud API, external API, Phaser, Remotion, WebGL, canvas, generated art, digital twin, autonomous agent behavior, real-time sensor readings, or live sensor support.

## Metadata check

Commands run:

```bash
python3 -m json.tool metadata.json >/tmp/hyvegrid-metadata-check.json && echo "metadata json valid"
grep -n "A beekeeper reports low hive activity" metadata.json
grep -n "An extension worker wants to place 20 hives" metadata.json
```

Results:

- `metadata.json` is valid JSON.
- Official Hive Health prompt is present.
- Official Site Readiness prompt is present.
- No metadata edits were made.

Prompt lines found:

```text
23:      "prompt": "A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?"
27:      "prompt": "An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?"
```

## download_model.sh check

Commands run:

```bash
bash -n download_model.sh
sed -n '1,220p' download_model.sh
```

Results:

- Shell syntax check passed.
- Script points to `model.gguf`.
- Script downloads the Granite 3.3 2B Instruct Q4_K_M GGUF.
- Script verifies SHA256.
- Script skips download if `model.gguf` already exists.
- No credentials are required by the script.
- The script was inspected only; no large model download was run.

## Runtime diagnostics check

Runtime diagnostics were run from the original working repo with `.venv` active:

```bash
source .venv/bin/activate
python3 scripts/check_local_runtime.py
```

Result: passed.

Observed:

- resolved llama-cli: `/Users/amaeteumanah/llama.cpp/build/bin/llama-cli`
- llama-cli exists: true
- llama-cli executable: true
- Intel macOS detected: true
- Intel macOS CPU-only fallback applies: true
- final llama extra args: `--device none -ngl 0`
- model files exist:
  - `model/hyvegrid-offline.gguf`
  - `model/granite-3.3-2b-instruct-Q4_K_M.gguf`
  - `model.gguf`

## Optional app start smoke check

The app was started from the original working repo:

```bash
source .venv/bin/activate
python -m app.web_app
```

Local URL checked:

```text
http://127.0.0.1:8000
```

Rendered-route checks passed:

- `/`: Mission Control loaded and included the five advisor areas plus Offline System Status.
- `/status`: Offline System Status loaded.
- `/advisor/hive-health`: Hive Health Advisor loaded and included English, Yorùbá, Hausa, and Swahili labels.

The app was stopped with `Control-C` after the smoke check.

## Issues found

1. Remote branch is stale. `origin/phase-1-eval-harness` remains at `8786b8975a89b3d5b4e2b3ed8f612aa477e65026`, while local HEAD is `7cab7250ca5b11b433df6e0fdae79066cfbb2951`.
2. Pushing produced:

```text
error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
Everything up-to-date
```

3. The clean clone proof for the current state is therefore a local clean clone fallback, not a remote clean clone proof.
4. Historical artifacts still mention the removed walkthrough/sprite work. They are archival evidence and not current planned work.

## Conclusion

Local clean clone fallback audit passed for the current Task 042A state. Required files, directories, demo artifacts, metadata, download script syntax, gitignore/model safety, runtime diagnostics, and local app smoke checks passed.

Remote branch availability is not ready: the remote does not contain Task 042A, and push attempts fail with RPC HTTP 400 despite also printing `Everything up-to-date`.
