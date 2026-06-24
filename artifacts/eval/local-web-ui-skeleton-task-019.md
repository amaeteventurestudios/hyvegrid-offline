# Local Web UI Skeleton (Task 019)

1. **Task title and date:** English local web UI skeleton and Offline System
   Status screen. Date: 2026-06-24.

## Starting commit

- `4ebefe99afce5d6dbbe7a2429a29b8a5c3df6417`

## Branch

- `phase-1-eval-harness`

## Scope

First local browser UI for HyveGrid Offline. Minimal FastAPI app with simple
HTML/CSS, English only. Mission Control at `/` and Offline System Status at
`/status`, with placeholder navigation for the five advisor modules. The app
serves localhost, uses no cloud services, and loads no GGUF model at import or
request time. No Yoruba.

## Files inspected

- `app/` (retrieval.py, prompt_builder.py, llama_runtime.py)
- `scripts/`
- `README.md`, `REPORT.md`, `SCORING.md`
- Profiler artifacts and JSONs (read only) for the status-screen evidence values

## Files changed

All new files. No existing source/config/model files were modified.

- `requirements.txt` (new) - fastapi, uvicorn, jinja2, httpx (local web deps only)
- `app/web_app.py` (new) - FastAPI app, routes, status data constants
- `app/templates/base.html` (new)
- `app/templates/index.html` (new) - Mission Control
- `app/templates/status.html` (new) - Offline System Status
- `app/templates/advisor.html` (new) - advisor placeholder
- `app/static/style.css` (new)
- `scripts/run_web_app.py` (new) - run wrapper
- `tests/test_web_app.py` (new)
- `artifacts/eval/local-web-ui-skeleton-task-019.md` (this artifact)

## Routes added

- `GET /` - Mission Control (HTML)
- `GET /status` - Offline System Status (HTML)
- `GET /advisor/{slug}` - placeholder page for the five advisor modules (200 for
  known slugs, 404 for unknown)
- `GET /health` - lightweight JSON liveness check (no model load)

## How to run the local web app

Install deps once (system Python 3.10 used here for parity with the test suite):

```
python3 -m pip install --user -r requirements.txt
```

Run:

```
python3 -m app.web_app
# or
python3 scripts/run_web_app.py
```

Open http://127.0.0.1:8000

Smoke-checked live: `GET /` and `GET /status` both returned HTTP 200, and
`GET /health` returned `{"status":"ok","mode":"localhost"}`. The process binds
127.0.0.1:8000 only.

## What the Mission Control screen includes

- Title: **HyveGrid Offline**
- Description: "Offline apiculture intelligence for African beekeepers and
  extension workers."
- A badge stating this is the ADTC 2026 public challenge edition, runs locally at
  localhost, and needs no cloud access during judged runtime.
- Navigation cards for: Hive Health Advisor, Site Readiness Advisor, Harvest
  Quality Coach, Forage and Pollination Guide, Hive Signal Check (all marked
  "Planned for demo"), and Offline System Status (marked "Available now").
- Footer reminder that HyveGrid is a field triage assistant, not a certified
  disease diagnosis tool.

## What the Offline System Status screen includes

A facts table plus benchmark and accuracy sections:

- Runtime: llama.cpp
- Model format: GGUF
- Locked model: Granite 3.3 2B Instruct Q4_K_M
- Profiler model path: model.gguf
- Local app mode: localhost (http://127.0.0.1:8000)
- Retrieval: SQLite FTS5 local knowledge base
- Network dependency during judged runtime: none
- Public challenge edition: yes
- Proprietary hardware or sensor IP included: no
- Metadata email finalized: yes
- Two official prompts configured: yes
- Latest benchmark evidence:
  - Task 016 profiler: participant mode with --skip-accuracy; 6.12 tokens/sec
    generation, ~2.67 GB peak RSS, no throttle, no OOM/crash, exit 0.
  - Task 017 profiler: participant mode without --skip-accuracy; 4.38 tokens/sec
    generation, ~2.67 GB peak RSS, no throttle, accuracy empty because lm_eval
    was not installed locally, exit 0.
- Accuracy status: "No local hidden-validation accuracy score is claimed."

Values are drawn from the completed Task 016/017 evidence, not computed by
loading the model.

## Confirmation of boundaries

- No model files, `model.gguf`, or anything under `model/` touched.
- No `metadata.json` change.
- No `download_model.sh` change.
- No cloud/API runtime dependency added (FastAPI/uvicorn serve localhost only).
- No Yoruba added.
- No existing runtime/RAG code refactored (`app/retrieval.py`,
  `app/prompt_builder.py`, `app/llama_runtime.py` unchanged).
- No private/proprietary material added.

## Test command and result

Existing suite plus the new web suite (TestClient, no model load):

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests ... OK

python3 -m unittest tests/test_web_app.py
Ran 9 tests ... OK
```

Total: 54/54 pass. The tests verify `/` returns 200 and includes
"HyveGrid Offline"; `/status` returns 200 and includes "llama.cpp", "GGUF",
"Granite 3.3 2B Instruct Q4_K_M", "model.gguf", "SQLite FTS5", and the accuracy
statement; the advisor placeholder returns 200 for a known slug and 404 for an
unknown one; and `/health` returns ok.

Note: Starlette prints a deprecation warning that the httpx-based TestClient is
deprecated in favor of `httpx2`. It is a library notice only; all tests pass.

## Decision

**PASS**

The local web app runs at 127.0.0.1:8000; Mission Control and Offline System
Status routes return 200; the status page accurately reflects current
profiler/model/submission evidence; no model load is required for page tests;
existing and new web tests pass (54/54); no metadata/download/model changes; no
cloud/Yoruba work.

## Remaining issues and recommended next task

- The five advisor screens are placeholders only; they are not yet wired to the
  retrieval/prompt-builder/runtime path.
- Throughput (6.12 / 4.38 t/s) and accuracy (not locally measured) caveats are
  unchanged from Task 017; the UI simply reports them.
- Recommended **Task 020**: wire at least one advisor screen (for example, Hive
  Health Advisor) to `answer_question()` so a question typed in the UI returns a
  real local Granite answer through the existing offline path. Keep it
  English-only and localhost, no cloud.
