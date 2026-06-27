# Task 034B Mac Preview Runtime Path Override Evidence

Date/time: 2026-06-26T20:36:40-0700

Starting commit: `042960e0d9a8db96253982cf7cd01d53b5bf3cf5`

## Task Name

Task 034B: Mac Preview Runtime Path Override.

## Files Changed

- `app/web_app.py`
- `tests/test_web_app.py`
- `README.md`
- `artifacts/eval/mac-preview-runtime-path-override-task-034B.md`

## Diagnostic Root Cause

Task 034A found that Mac preview failed because the app tried to run llama.cpp
from the Ubuntu-specific default path:

```text
/home/amaete/llama.cpp/build/bin/llama-cli
```

The repo-local `model.gguf` symlink existed and resolved to the Granite GGUF.
The missing piece was a local Mac `llama-cli` binary at the configured path.

## Runtime Override Support

Supported environment variables:

- `LLAMA_BIN`
- `HYVEGRID_MODEL_PATH`

Default behavior is preserved when environment variables are not set:

- Default llama path: `/home/amaete/llama.cpp/build/bin/llama-cli`
- Default model path: `model.gguf`

The advisor submit path now passes the resolved paths into the existing
`answer_question()` runtime call. Retrieval logic, prompt building, and answer
format behavior were not changed.

## Test Summary

System Python command:

```bash
python3 -m unittest tests/test_web_app.py
```

Result:

- Failed before importing the app because `/usr/bin/python3` did not have
  `fastapi` installed.
- This was a local dependency-environment issue, not an app test failure.

Temporary venv command:

```bash
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests/test_web_app.py
```

Result:

- `Ran 39 tests in 0.680s OK`

## Boundary Confirmations

- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- Retrieval logic was not changed.
- Prompt builder logic was not changed.
- Answer-generation behavior was not changed except runtime path resolution.
- No profiler was run.
- No long model inference was run.
- No external packages, CDNs, or assets were added.
- No Phaser, WebGL, canvas, or autonomous agent work was added.
- No Hausa or Swahili work was added.

## Mac Preview Command Example

```bash
LLAMA_BIN=/path/to/llama.cpp/build/bin/llama-cli \
HYVEGRID_MODEL_PATH=model.gguf \
/tmp/hyvegrid-task-033-test-venv/bin/python -m app.web_app
```

## Known Limitation

The user still needs a local Mac `llama.cpp` `llama-cli` binary. This task only
adds safe path configuration for preview.

## Next Recommended Task

Task 034C: Build or point Mac preview to local llama.cpp binary and visually
audit walkthrough animation.
