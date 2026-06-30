# Task 038C Intel macOS CPU llama.cpp Fallback Audit

## Original Metal Crash Symptom

Direct local llama.cpp inference on this Intel iMac resolved the correct Mac
binary, but the Metal-enabled path crashed with:

```text
GGML_ASSERT(buf_src) failed
libggml-metal...
zsh: abort
```

## Direct CPU-Only Command That Worked

```bash
"$HOME/llama.cpp/build/bin/llama-cli" \
  --device none \
  -ngl 0 \
  -m model/hyvegrid-offline.gguf \
  -p "A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first?" \
  -n 80
```

## Files Changed

- `app/llama_runtime.py`
- `scripts/check_local_runtime.py`
- `tests/test_llama_runtime.py`
- `artifacts/eval/mac-cpu-llama-runtime-fallback-task-038C.md`

## Runtime Arg Resolution Behavior

The runtime still uses llama.cpp and GGUF locally. Extra llama-cli args are
resolved without shell execution:

1. If `LLAMA_EXTRA_ARGS` is set, parse it with `shlex.split()` and append those
   args to the `llama-cli` command.
2. If `LLAMA_EXTRA_ARGS` is not set and the host is Intel macOS
   (`Darwin` + `x86_64`/`i386`/`i686`), default to:

```text
--device none -ngl 0
```

3. On Ubuntu/VM or other non-Intel-macOS hosts, no extra args are added unless
   `LLAMA_EXTRA_ARGS` is explicitly set.

The args are inserted immediately after the `llama-cli` binary and before the
model path flags. Existing `--single-turn`, `--no-display-prompt`, `--simple-io`,
and `--no-warmup` behavior is preserved.

If llama.cpp returns a Metal/ggml crash signature, the runtime attaches and logs
this local setup hint:

```text
On Intel macOS, try LLAMA_EXTRA_ARGS="--device none -ngl 0".
```

The browser-facing advisor message remains safe and non-technical.

## How To Run On Mac

```bash
export LLAMA_BIN="$HOME/llama.cpp/build/bin/llama-cli"
export LLAMA_EXTRA_ARGS="--device none -ngl 0"
python3 scripts/check_local_runtime.py
```

On Intel macOS, `LLAMA_EXTRA_ARGS` can be omitted because the runtime now applies
the same CPU-only args by default.

## How To Run On Ubuntu/VM

```bash
export LLAMA_BIN="/home/amaete/llama.cpp/build/bin/llama-cli"
unset LLAMA_EXTRA_ARGS
python3 scripts/check_local_runtime.py
```

Ubuntu/VM behavior remains unchanged unless `LLAMA_EXTRA_ARGS` is explicitly set.

## Diagnostics Command

```bash
python3 scripts/check_local_runtime.py
```

On this Mac workspace, diagnostics reported:

```text
machine: x86_64
resolved llama-cli: /Users/amaeteumanah/llama.cpp/build/bin/llama-cli
LLAMA_EXTRA_ARGS set: False
Intel macOS detected: True
Intel macOS CPU-only fallback applies: True
final llama extra args source: intel-macos-default
final llama extra args: --device none -ngl 0
```

The diagnostics script does not run inference.

## Test Results

Runtime diagnostics:

```text
python3 scripts/check_local_runtime.py
exit 0
```

Runtime unit suite:

```text
python3 -m unittest tests.test_llama_runtime
Ran 26 tests in 0.029s
OK
```

Bare system Python web command:

```text
python3 -m unittest tests.test_web_app
```

Result: failed before tests ran because the system Python environment does not
have `fastapi` installed.

Established preview venv focused web suite:

```text
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app
Ran 40 tests in 0.379s
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
- Advisor prompt content and answer formatting were not changed.
- Retrieval logic was not changed.
- llama.cpp remains the local runtime.
- GGUF remains the model format.
- No cloud API, external service, remote runtime dependency, CDN, Phaser, WebGL,
  canvas, Remotion, internet dependency, or remote asset was added.
- llama.cpp was not added to this repo.
- The runtime does not download, clone, or build llama.cpp.

## Final Status

MAC_CPU_LLAMA_FALLBACK_READY
