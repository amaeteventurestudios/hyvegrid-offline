# Task 038D Local Runtime Success And Answer Guard Audit

## Commit Reviewed

```text
dd0a1c0052534fa9bdcb6a0598c8c63f0956bdbd
Add Intel macOS CPU llama fallback Task 038C
```

## Manual Browser Success Observed

The manual Mac browser test now succeeds:

- local answer generated
- retrieved sources displayed
- `COMPLETED LOCALLY.` displayed

## Original Failure Chain

1. The app initially looked for the Ubuntu/VM llama.cpp path on Mac:

```text
/home/amaete/llama.cpp/build/bin/llama-cli
```

2. Task 038B added local runtime path resolution for Mac, VM, repo-local, and
   Homebrew locations.
3. The resolved Intel iMac llama.cpp binary then crashed through Metal with:

```text
GGML_ASSERT(buf_src) failed
libggml-metal...
zsh: abort
```

4. Task 038C added Intel macOS CPU-only fallback args:

```text
--device none -ngl 0
```

## Current Runtime State

- llama.cpp resolves locally to `/Users/amaeteumanah/llama.cpp/build/bin/llama-cli`
- GGUF model files are present
- Intel macOS CPU fallback applies
- runtime remains local and offline
- llama.cpp remains the runtime
- GGUF remains the model format

## Answer-Quality Issue Observed

The Hive Health Advisor prompt reported:

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood.
What should they check first, and what should they avoid doing immediately?
```

The generated answer inferred:

```text
no eggs or young brood
```

The user did not report that. The safer answer should frame this as a check:

```text
Check whether eggs and young larvae are present.
Do not assume eggs or young brood are absent unless the beekeeper reports that.
```

## Prompt Guard Added

`app/prompt_builder.py` now includes an unsupported-assumption guard instructing
the model to:

- use only reported observations and retrieved local notes
- distinguish reported observation, possible concern, check first, and avoid
  doing immediately
- avoid stating that eggs, larvae, queen, stores, mites, disease, robbing, or
  brood condition are absent or present unless reported or explicitly supported
  by retrieved notes
- phrase uncertain findings as checks
- for partially capped brood, confirm by physical inspection whether eggs and
  young larvae are present and whether the brood pattern is solid
- avoid saying `no eggs`, `no young brood`, `queen absent`, `mite infestation`,
  `virus`, or `disease` unless explicitly reported or carefully framed as a
  possible concern requiring inspection

This changes prompt guidance only. It does not run a live model in tests and
does not depend on model output randomness.

## Files Changed

- `app/prompt_builder.py`
- `tests/test_prompt_builder.py`
- `artifacts/eval/local-runtime-success-answer-guard-task-038D.md`

## Tests Run

Runtime diagnostics:

```text
python3 scripts/check_local_runtime.py
exit 0
```

Prompt builder tests:

```text
python3 -m unittest tests.test_prompt_builder
Ran 17 tests in 0.037s
OK
```

Runtime tests:

```text
python3 -m unittest tests.test_llama_runtime
Ran 26 tests in 0.031s
OK
```

Bare system Python web command:

```text
python3 -m unittest tests.test_web_app
```

Result: failed before tests ran because the system Python environment does not
have `fastapi` installed.

Focused web suite in the project preview venv:

```text
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app
Ran 40 tests in 0.459s
OK
```

## Confirmations

- No GGUF model files were changed.
- Model selection was not changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- No scoring files were changed.
- llama.cpp binary resolution was not changed.
- Intel macOS CPU fallback behavior was not changed.
- Retrieval logic was not changed.
- No cloud API, external service, remote runtime dependency, CDN, Phaser, WebGL,
  canvas, Remotion, internet dependency, or remote asset was added.
- Hausa and Swahili were not implemented in this task.
- No new UI screens were added.

## Final Status

LOCAL_RUNTIME_WORKING_ASSUMPTION_GUARD_READY
