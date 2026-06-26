# Task 031B-runtime-submit-hotfix Evidence

Date/time: 2026-06-25T20:52:30-07:00

Starting commit: `94520fa42bed287a0a07d2f76c583b6bcba8843d`

## User-Reported Issue

The Mac browser could load Mission Control and advisor pages through the Ubuntu
VM, but submitting Hive Health Advisor or Site Readiness Advisor did not produce
a usable answer. Site Readiness eventually showed a generic local runtime error.

## Path Checks

- Repo root: `/home/amaete/hyvegrid-offline`
- `model.gguf` resolves to
  `/home/amaete/hyvegrid-offline/model-candidates/granite-3.3-2b-instruct-Q4_K_M.gguf`
- `model.gguf` symlink exists and points to the locked Granite GGUF model.
- `model.gguf` target size: about 1.5 GB.
- llama executable found:
  `/home/amaete/llama.cpp/build/bin/llama-cli`
- llama executable version: `9753 (7c082bc41)`

## Root Cause Found

Two app-side problems made the Mac preview submit path fragile and hard to
interpret:

1. The runtime wrapper passed a relative model path to `llama-cli`. That worked
   only when the app process current working directory was the repo root.
2. The advisor page gave no immediate loading feedback while the local model was
   loading and generating, so a several-minute offline inference looked broken.

The direct llama smoke test also showed why the app must keep using
`--single-turn`: a command without that flag can remain in llama.cpp interactive
mode after producing text.

## Fix Implemented

Runtime/logging:

- Added deterministic runtime path resolution anchored at the repo root.
- Kept the ADTC-compatible configured model path as `model.gguf`.
- Logged runtime diagnostics server-side:
  - repo root
  - resolved model path
  - model existence
  - resolved llama executable path
  - llama existence
  - llama executable bit
- Logged exception type and message server-side when advisor generation fails.
- Logged nonzero/timeout/no-answer metadata server-side without exposing raw
  prompt, stdout, command details, or stack traces to the user page.

Submit UX:

- Added a local loading state on advisor forms.
- On submit, the button is disabled and changed to `Working locally...`.
- The page immediately shows:
  `Running the local Granite model through llama.cpp. This may take several minutes on the offline laptop profile. Please do not refresh.`
- The loading behavior is local HTML/CSS/JS only.

Better user error:

- Advisor runtime failures now show:
  `HyveGrid could not complete this local answer. The advisor request reached the offline app, but the local model runtime failed. Check the server log for the exact model/runtime path issue.`

Advisor pages covered:

- Hive Health Advisor
- Site Readiness Advisor
- Harvest Quality Coach
- Forage & Pollination Guide
- Hive Signal Check

## Direct llama Smoke Test

Command type: local `llama-cli` direct smoke test using `model.gguf` and the
same single-turn style flags used by the app.

Result:

- Exit status: 0
- Wall time: 1:29.80
- The local model loaded and generated text.
- No internet, API, or cloud dependency was used.

Note: an earlier diagnostic run without `--single-turn` produced an answer
fragment but stayed in llama.cpp interactive mode. That smoke-test process was
terminated directly and was not an app server.

## Fresh Preview Server

A fresh preview server was started because the existing 8001 server was left
untouched.

- Port: `8002`
- PID: `140124`
- Log path: `artifacts/eval/task-031B-runtime-submit-preview-8002.log`
- Mac URL: `http://172.16.150.128:8002`
- The server was left running.

The existing local server on port 8001 was not stopped, restarted, killed, or
interfered with.

## Route Checks

Against `http://127.0.0.1:8002`:

| Route | HTTP status |
| --- | ---: |
| `/` | 200 |
| `/?lang=yo` | 200 |
| `/advisor/hive-health` | 200 |
| `/advisor/site-readiness` | 200 |

## Real Advisor POST Inference

Route: `POST /advisor/hive-health`

Prompt:

`Low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first?`

Result:

- HTTP status: 200
- Wall time: 5:04.92
- `curl` time_total: 300.482963 seconds
- Answer rendered: yes
- Sources rendered: yes
- Error appeared: no
- `Completed locally` rendered: yes
- Traceback appeared: no

Short answer excerpt:

`1. Possible concern: The observed symptoms of low hive activity, ants near the hive stand, normal smell, and partially capped brood could indicate a possible concern such as a queen issue, varroa mite infestation, or a parasite infestation. 2. Check first: Confirm by physical inspection before drawing conclusions...`

## Tests

Command:

`python3 -m unittest tests/test_web_app.py tests/test_llama_runtime.py`

Result:

- 47 tests ran.
- Result: OK.
- Existing warning: `StarletteDeprecationWarning` from FastAPI/TestClient.

## Files Changed

- `app/llama_runtime.py`
- `app/web_app.py`
- `app/templates/advisor_form.html`
- `app/static/style.css`
- `tests/test_web_app.py`
- `tests/test_llama_runtime.py`
- `artifacts/eval/advisor-runtime-submit-hotfix-task-031B.md`

The live preview log exists at
`artifacts/eval/task-031B-runtime-submit-preview-8002.log` and is intentionally
not staged because the 8002 preview server is still running and may append to
it.

## Compliance Notes

- No profiler was run.
- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- llama.cpp/runtime integration stayed local.
- Retrieval logic was not changed.
- Prompt builder behavior was not changed.
- No simulation was implemented.
- No real sensor integration was implemented.
- No Hausa or Swahili work was implemented.
- No external links, CDN assets, internet assets, external APIs, or cloud
  dependencies were added.
- Existing 8001 local server was not stopped, restarted, killed, or interfered
  with.
- Fresh 8002 preview server was started and left running.

## Next Recommended Task

Task 031C: Advisor page visual refresh after runtime/submit behavior is fixed.
