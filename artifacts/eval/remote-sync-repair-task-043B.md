# Task 043B Remote Sync Repair

## Purpose

Repair or fully diagnose the Git push problem so the remote `phase-1-eval-harness` branch can contain all local completed work through Task 043A.

This task is Git synchronization and evidence only. No app behavior, runtime behavior, model behavior, retrieval behavior, language behavior, prompts, metadata, report content, or demo artifacts were changed.

## Starting state

- Local HEAD: `a0b4c49d7c63d131425dbd335de04cf60a31302c`
- Remote HEAD before repair: `8786b8975a89b3d5b4e2b3ed8f612aa477e65026`
- Working tree before repair: clean
- Remote URL type: HTTPS

Remote URL:

```text
https://github.com/amaeteventurestudios/hyvegrid-offline.git
```

Local latest commit:

```text
a0b4c49 Add clean clone audit for Task 043A
```

Remote latest commit:

```text
8786b89 Refresh advisor page visual design for Task 031C
```

## Problem observed

Previous pushes reported:

```text
error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
Everything up-to-date
```

Task 043A confirmed that `Everything up-to-date` could not be trusted by itself, because `origin/phase-1-eval-harness` remained stale after fetch.

## Commands run

Baseline verification:

```bash
git status --short
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git remote -v
git fetch origin phase-1-eval-harness
git rev-parse origin/phase-1-eval-harness
git log --oneline --decorate -8
git log --oneline --decorate -8 origin/phase-1-eval-harness
git log --oneline origin/phase-1-eval-harness..HEAD
```

Object and file safety:

```bash
git count-objects -vH
git fsck --full
git ls-files | grep -E '(^model/|\.gguf$)' || true
find . -path ./.git -prune -o -name "*.gguf" -print
find . -path ./.git -prune -o -type f -size +50M -print
```

Push repair attempts:

```bash
git push --porcelain origin HEAD:phase-1-eval-harness
git config http.version HTTP/1.1
git push --porcelain origin HEAD:phase-1-eval-harness
git gc
git push --porcelain origin HEAD:phase-1-eval-harness
GIT_TRACE=1 GIT_CURL_VERBOSE=1 git push --porcelain origin HEAD:phase-1-eval-harness 2>&1 | tee /tmp/hyvegrid-task-043B-push-trace.txt
```

Verification after attempts:

```bash
git fetch origin phase-1-eval-harness
git rev-parse HEAD
git rev-parse origin/phase-1-eval-harness
git branch -r --contains a0b4c49d7c63d131425dbd335de04cf60a31302c
```

## Object and file safety checks

- git count-objects result before `git gc`:

```text
count: 1405
size: 28.30 MiB
in-pack: 316
packs: 2
size-pack: 795.11 KiB
prune-packable: 8
garbage: 0
size-garbage: 0 bytes
```

- git count-objects result after `git gc`:

```text
count: 711
size: 16.41 MiB
in-pack: 993
packs: 1
size-pack: 9.87 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
```

- git fsck result: no repository corruption error was reported. It printed many dangling tree objects, which are unreachable objects rather than corruption.
- tracked GGUF/model files: none. `git ls-files | grep -E '(^model/|\.gguf$)'` produced no output.
- local untracked GGUF/model files exist, but are not tracked:

```text
./model/candidates/step7c-baseline-reset/gemma-2-2b-it-q4km/gemma-2-2b-it-q4_k_m.gguf
./model/candidates/step7c-baseline-reset/granite-3.3-2b-q4km/granite-3.3-2b-instruct-Q4_K_M.gguf
./model/granite-3.3-2b-instruct-Q4_K_M.gguf
./model/hyvegrid-offline.gguf
./model.gguf
```

- large files over 50 MB found locally:

```text
./model/candidates/step7c-baseline-reset/gemma-2-2b-it-q4km/gemma-2-2b-it-q4_k_m.gguf
./model/candidates/step7c-baseline-reset/granite-3.3-2b-q4km/granite-3.3-2b-instruct-Q4_K_M.gguf
./model/granite-3.3-2b-instruct-Q4_K_M.gguf
./model/hyvegrid-offline.gguf
```

These are local model files and are not tracked by git.

## Push repair attempts

| Attempt | Command | Result |
|---|---|---|
| Direct push | `git push --porcelain origin HEAD:phase-1-eval-harness` | Failed: `error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400`; `send-pack: unexpected disconnect while reading sideband packet`; `fatal: the remote end hung up unexpectedly`; `Done`. |
| HTTP/1.1 push | `git config http.version HTTP/1.1`; `git push --porcelain origin HEAD:phase-1-eval-harness` | Failed: `send-pack: unexpected disconnect while reading sideband packet`; `fatal: the remote end hung up unexpectedly`; `Done`. |
| git gc + retry | `git gc`; `git push --porcelain origin HEAD:phase-1-eval-harness` | Failed: `send-pack: unexpected disconnect while reading sideband packet`; `fatal: the remote end hung up unexpectedly`; `Done`. |
| traced push | `GIT_TRACE=1 GIT_CURL_VERBOSE=1 git push --porcelain origin HEAD:phase-1-eval-harness 2>&1 \| tee /tmp/hyvegrid-task-043B-push-trace.txt` | Failed: `send-pack: unexpected disconnect while reading sideband packet`; `fatal: the remote end hung up unexpectedly`; `Done`. |

## Trace summary

Trace file:

```text
/tmp/hyvegrid-task-043B-push-trace.txt
```

The visible trace showed:

- Git used HTTPS remote `https://github.com/amaeteventurestudios/hyvegrid-offline.git`.
- Initial unauthenticated receive-pack discovery returned `401 Unauthorized`.
- Git invoked GitHub CLI credential helper.
- Authenticated receive-pack discovery returned `200 OK`.
- The request used HTTP/1.1 after repo-local config was set.
- GitHub returned `200 OK` to receive-pack POSTs.
- The final receive-pack response had no sideband content, followed by:

```text
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
Done
```

The trace output shown by Git redacted the Authorization header as `Authorization: Basic <redacted>`. No credentials or tokens were committed.

## Final remote verification

- Local HEAD: `a0b4c49d7c63d131425dbd335de04cf60a31302c`
- Remote HEAD: `8786b8975a89b3d5b4e2b3ed8f612aa477e65026`
- Remote contains Task 042A commit (`7cab7250ca5b11b433df6e0fdae79066cfbb2951`): no
- Remote contains Task 043A commit (`a0b4c49d7c63d131425dbd335de04cf60a31302c`): no

`git branch -r --contains a0b4c49d7c63d131425dbd335de04cf60a31302c` produced no remote branch output.

## Conclusion

REMOTE_SYNC_STILL_BLOCKED

The local branch is clean and contains all local completed work through Task 043A. The remote branch is still stale at Task 031C. Direct push, repo-local HTTP/1.1 retry, `git gc` retry, and traced push all failed with GitHub receive-pack sideband disconnect behavior. No force push, history rewrite, rebase, branch deletion, remote URL change, app edit, runtime edit, metadata edit, model edit, or protected-file edit was performed.
