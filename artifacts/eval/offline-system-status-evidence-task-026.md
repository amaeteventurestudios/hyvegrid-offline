# Task 026: Offline System Status evidence refresh

Date: 2026-06-25

Starting branch: `phase-1-eval-harness`

Starting HEAD: `7ef8c68decc4ef6f26a18dae9bd85f5b718f59c8`

Working tree at start: clean

Runtime path: local web app started with `python3 -m app.web_app`. Evidence was captured with local HTTP GET requests only. No advisor POST route was submitted and no real Granite inference was run.

## Routes Tested

| Route | HTTP status | Wall time | Rendered |
| --- | ---: | ---: | --- |
| `GET /` | 200 | 0.018469 seconds | yes |
| `GET /status` | 200 | 0.004713 seconds | yes |
| `GET /health` | 200 | 0.006200 seconds | yes |

## Mission Control Markers Found

The `GET /` response rendered Mission Control and included these advisor/status navigation markers:

- `Offline System Status`
- `Hive Health Advisor`
- `Site Readiness Advisor`
- `Harvest Quality Coach`
- `Forage and Pollination Guide`
- `Hive Signal Check`

## Offline System Status Markers Found

The `GET /status` response rendered Offline System Status and included these markers:

- Local runtime evidence: `Local runtime and submission-path evidence for the locked Granite model.`
- Runtime: `llama.cpp`
- Model format: `GGUF`
- Locked model: `Granite 3.3 2B Instruct Q4_K_M`
- Profiler model path: `model.gguf`
- Local app mode: `localhost (http://127.0.0.1:8000)`
- Retrieval: `SQLite FTS5 local knowledge base`
- Network dependency during judged runtime: `none`
- Public challenge edition: `yes`
- Footer boundary: `HyveGrid Offline ... ADTC 2026 public challenge edition ... local offline build, no cloud access during judged runtime.`
- Accuracy boundary: `No local hidden-validation accuracy score is claimed.`

## Health Response

The `GET /health` response returned HTTP 200 with:

```json
{"status":"ok","mode":"localhost"}
```

Summary: the health endpoint reports an OK localhost mode response.

## Clean-Output Check

Passed. The captured `/`, `/status`, and `/health` responses did not expose traceback text, stack traces, raw command details, internal filesystem paths, raw stdout/stderr, llama.cpp runtime logs, or hidden runtime command details.

The `/status` page intentionally includes public offline-runtime markers such as `llama.cpp`, `GGUF`, `SQLite FTS5 local knowledge base`, `localhost`, `Network dependency during judged runtime: none`, and public challenge-edition/no-cloud boundary text.

## Tests

Commands run after evidence capture:

```bash
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
python3 -m unittest tests/test_web_app.py
```

Results:

- `tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py`: 45 tests passed.
- `tests/test_web_app.py`: 23 tests passed.

Note: `tests/test_web_app.py` emitted an existing `StarletteDeprecationWarning` from `fastapi.testclient`; the suite still passed.

## Boundary Confirmation

No real model inference was run.

No app architecture, source code, metadata, model files, profiler artifacts, retrieval logic, prompt builder, llama runtime, Yoruba feature, Guided Hive Walkthrough, cloud/API dependency, or UI refactor changes were made.
