# Task 038B Local Runtime Path Resolver Audit

## Original Failing Path

The Mac preview was still reporting the Ubuntu/VM-only default path:

```text
/home/amaete/llama.cpp/build/bin/llama-cli
```

That path remains supported, but it is no longer the only path checked when the
app needs a local `llama-cli` binary.

## Files Changed

- `app/llama_runtime.py`
- `scripts/check_local_runtime.py`
- `tests/test_llama_runtime.py`
- `tests/test_web_app.py`
- `artifacts/eval/local-runtime-path-resolver-task-038B.md`

## Resolver Order

The local runtime resolver checks for an executable `llama-cli` in this order:

1. `LLAMA_BIN`, if set.
2. `/home/amaete/llama.cpp/build/bin/llama-cli`
3. `$HOME/llama.cpp/build/bin/llama-cli`
4. `./llama.cpp/build/bin/llama-cli`
5. `/opt/homebrew/bin/llama-cli`
6. `/usr/local/bin/llama-cli`

If no executable binary is found, the runtime error lists every checked path and
prints Mac and Ubuntu/VM export commands.

## How To Run On Mac

```bash
export LLAMA_BIN="$HOME/llama.cpp/build/bin/llama-cli"
python3 scripts/check_local_runtime.py
```

Then start the local app as usual from the repo root.

## How To Run On Ubuntu/VM

```bash
export LLAMA_BIN="/home/amaete/llama.cpp/build/bin/llama-cli"
python3 scripts/check_local_runtime.py
```

The original Ubuntu/VM default path is still preserved.

## Diagnostics Command

```bash
python3 scripts/check_local_runtime.py
```

On this Mac workspace the diagnostic resolved:

```text
/Users/amaeteumanah/llama.cpp/build/bin/llama-cli
```

It also confirmed that these model paths exist:

```text
model/hyvegrid-offline.gguf
model/granite-3.3-2b-instruct-Q4_K_M.gguf
model.gguf
```

The diagnostics script does not run inference.

## Test Results

Bare system Python command:

```text
python3 -m unittest tests.test_web_app
```

Result: failed before tests ran because the system Python environment does not
have `fastapi` installed.

Established preview venv focused web suite:

```text
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app
Ran 40 tests in 0.412s
OK
```

Runtime unit suite:

```text
python3 -m unittest tests.test_llama_runtime
Ran 20 tests in 0.026s
OK
```

## Confirmations

- No GGUF model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- No scoring files were changed.
- Inference prompt logic was not changed.
- Retrieval logic was not changed.
- llama.cpp remains the local runtime.
- GGUF remains the model format.
- No cloud API, external service, CDN, Phaser, WebGL, canvas, Remotion, remote
  runtime dependency, or remote asset was added.
- The resolver does not download, clone, build, or vendor llama.cpp.

## Final Status

LOCAL_RUNTIME_RESOLVER_READY
