"""Local English web UI for HyveGrid Offline (ADTC 2026).

A minimal FastAPI app serving screens at localhost:

- Mission Control (/): overview and navigation cards.
- Offline System Status (/status): runtime, model, retrieval, compliance, and
  benchmark evidence.
- Hive Health Advisor (/advisor/hive-health): a form that runs a real local
  answer through the existing offline path (retrieval + prompt builder +
  llama.cpp + Granite).

This is an English-only UI. It serves localhost only, uses no cloud services,
and loads no GGUF model at import time. The status values are drawn from the
completed profiler/runtime evidence (Tasks 014-018). The Hive Health Advisor
calls answer_question() on submit, which runs the model; no other advisor is
wired yet.

Run with:
    python3 -m app.web_app
or:
    python3 scripts/run_web_app.py

Then open http://127.0.0.1:8000
"""

import asyncio
import urllib.parse
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# The existing offline answer path: retrieval + prompt builder + llama.cpp run
# + output cleanup. Imported here so the Hive Health Advisor can call it without
# duplicating that logic. Tests monkeypatch this name.
from app.llama_runtime import answer_question

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="HyveGrid Offline",
    description="Local offline apiculture assistant (ADTC 2026 public edition).",
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

APP_DESCRIPTION = (
    "Offline apiculture intelligence for African beekeepers and extension workers."
)

# Advisor modules are shown as navigation cards. They are planned for a later
# demo phase and are not enabled in this English skeleton beyond a placeholder.
ADVISORS = [
    {
        "slug": "hive-health",
        "name": "Hive Health Advisor",
        "blurb": "Colony strength, queen signs, brood pattern, food stores, pests.",
    },
    {
        "slug": "site-readiness",
        "name": "Site Readiness Advisor",
        "blurb": "Placement, drainage, water, shade, safety, pesticide risk.",
    },
    {
        "slug": "harvest-quality",
        "name": "Harvest Quality Coach",
        "blurb": "Capped honey, moisture risk, food-safe handling, storage.",
    },
    {
        "slug": "forage-pollination",
        "name": "Forage and Pollination Guide",
        "blurb": "Forage diversity, flowering gaps, pesticide coordination.",
    },
    {
        "slug": "hive-signals",
        "name": "Hive Signal Check",
        "blurb": "Temperature, humidity, activity, ventilation. Signals are not diagnosis.",
    },
]

STATUS_FACTS = [
    ("Runtime", "llama.cpp"),
    ("Model format", "GGUF"),
    ("Locked model", "Granite 3.3 2B Instruct Q4_K_M"),
    ("Profiler model path", "model.gguf"),
    ("Local app mode", "localhost (http://127.0.0.1:8000)"),
    ("Retrieval", "SQLite FTS5 local knowledge base"),
    ("Network dependency during judged runtime", "none"),
    ("Public challenge edition", "yes"),
    ("Proprietary hardware or sensor IP included", "no"),
    ("Metadata email finalized", "yes"),
    ("Two official prompts configured", "yes"),
]

BENCHMARK_EVIDENCE = [
    {
        "run": "Task 016 profiler",
        "detail": "Participant mode with --skip-accuracy. 6.12 tokens/sec generation, "
        "~2.67 GB peak RSS, no throttle, no OOM/crash, exit 0.",
    },
    {
        "run": "Task 017 profiler",
        "detail": "Participant mode without --skip-accuracy. 4.38 tokens/sec generation, "
        "~2.67 GB peak RSS, no throttle. Accuracy empty because lm_eval was not "
        "installed locally. Exit 0.",
    },
]

ACCURACY_STATUS = "No local hidden-validation accuracy score is claimed."

NOT_DIAGNOSIS = (
    "HyveGrid is a field triage assistant, not a certified disease diagnosis tool."
)

# Hive Health Advisor copy and messages.
HIVE_HEALTH_EXAMPLE = (
    "A beekeeper reports low hive activity, ants near the hive stand, normal "
    "smell, and partially capped brood. What should they check first, and what "
    "should they avoid doing immediately?"
)
HIVE_HEALTH_HELPER = (
    "Ask an English hive-health question. The answer runs locally through the "
    "Granite model and the public apiculture knowledge base. No cloud access."
)
VALIDATION_EMPTY = "Please enter a hive-health question before submitting."
ANSWER_ERROR = (
    "HyveGrid could not complete this local answer. Confirm the model is "
    "downloaded and llama.cpp is available, then try again."
)
RUNTIME_OK = "Completed locally."


def _hive_health_context() -> dict:
    """Base template context for the Hive Health Advisor page."""
    return {
        "example_prompt": HIVE_HEALTH_EXAMPLE,
        "helper": HIVE_HEALTH_HELPER,
        "not_diagnosis": NOT_DIAGNOSIS,
        "submitted_question": "",
    }


@app.get("/advisor/hive-health", response_class=HTMLResponse)
async def hive_health_form(request: Request) -> HTMLResponse:
    """Render the Hive Health Advisor form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(request, "hive_health.html", _hive_health_context())


@app.post("/advisor/hive-health", response_class=HTMLResponse)
async def hive_health_submit(request: Request) -> HTMLResponse:
    """Handle a submitted hive-health question through the offline answer path."""
    ctx = _hive_health_context()

    # Parse the urlencoded form body manually so the app needs no
    # python-multipart dependency.
    raw = await request.body()
    form = urllib.parse.parse_qs(
        raw.decode("utf-8", "replace"), keep_blank_values=True
    )
    question = (form.get("question", [""])[0] or "").strip()

    if not question:
        ctx["validation_error"] = VALIDATION_EMPTY
        return TEMPLATES.TemplateResponse(request, "hive_health.html", ctx)

    ctx["submitted_question"] = question

    # answer_question() is blocking (model load + generation) and can take
    # minutes; run it off the event loop so the server stays responsive.
    try:
        bundle = await asyncio.to_thread(answer_question, question)
    except Exception:
        # Do not expose stack traces or internal details to the user.
        ctx["error_message"] = ANSWER_ERROR
        return TEMPLATES.TemplateResponse(request, "hive_health.html", ctx)

    runtime = bundle.get("runtime") or {}
    answer = (bundle.get("answer") or "").strip()
    ok = (
        not runtime.get("timed_out")
        and runtime.get("returncode") == 0
        and bool(answer)
    )
    if not ok:
        ctx["error_message"] = ANSWER_ERROR
        return TEMPLATES.TemplateResponse(request, "hive_health.html", ctx)

    ctx["answer"] = answer
    ctx["sources"] = bundle.get("results") or []
    ctx["runtime_ok"] = RUNTIME_OK
    return TEMPLATES.TemplateResponse(request, "hive_health.html", ctx)


@app.get("/", response_class=HTMLResponse)
async def mission_control(request: Request) -> HTMLResponse:
    """Mission Control: overview and navigation cards."""
    return TEMPLATES.TemplateResponse(
        request,
        "index.html",
        {
            "description": APP_DESCRIPTION,
            "advisors": ADVISORS,
            "not_diagnosis": NOT_DIAGNOSIS,
        },
    )


@app.get("/status", response_class=HTMLResponse)
async def offline_system_status(request: Request) -> HTMLResponse:
    """Offline System Status: runtime, model, retrieval, compliance, evidence."""
    return TEMPLATES.TemplateResponse(
        request,
        "status.html",
        {
            "facts": STATUS_FACTS,
            "benchmarks": BENCHMARK_EVIDENCE,
            "accuracy_status": ACCURACY_STATUS,
            "not_diagnosis": NOT_DIAGNOSIS,
        },
    )


@app.get("/advisor/{slug}", response_class=HTMLResponse)
async def advisor_placeholder(slug: str, request: Request) -> HTMLResponse:
    """Navigation placeholder for advisor modules not yet enabled."""
    advisor = next((a for a in ADVISORS if a["slug"] == slug), None)
    if advisor is None:
        raise HTTPException(status_code=404, detail="Unknown advisor")
    return TEMPLATES.TemplateResponse(
        request,
        "advisor.html",
        {"advisor": advisor, "not_diagnosis": NOT_DIAGNOSIS},
    )


@app.get("/health")
async def health() -> dict:
    """Lightweight liveness check for local testing (no model load)."""
    return {"status": "ok", "mode": "localhost"}


if __name__ == "__main__":
    # Pass the app object (not an import string) so `python3 -m app.web_app`
    # does not import the module twice.
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
