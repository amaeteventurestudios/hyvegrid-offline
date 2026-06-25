"""Local English web UI for HyveGrid Offline (ADTC 2026).

A minimal FastAPI app serving screens at localhost:

- Mission Control (/): overview and navigation cards.
- Offline System Status (/status): runtime, model, retrieval, compliance, and
  benchmark evidence.
- Hive Health Advisor (/advisor/hive-health): a form that runs a real local
  answer through the existing offline path (retrieval + prompt builder +
  llama.cpp + Granite).
- Site Readiness Advisor (/advisor/site-readiness): same, for apiary siting and
  site-readiness questions.

This is an English-only UI. It serves localhost only, uses no cloud services,
and loads no GGUF model at import time. The status values are drawn from the
completed profiler/runtime evidence (Tasks 014-018). The wired advisors call
answer_question() on submit, which runs the model; the other advisors
(harvest-quality, forage-pollination, hive-signals) remain placeholders.

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
        "slug": "hive-signal",
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

# Wired-advisor copy and messages. Each config holds the template fields the
# shared form template and shared submit logic need.
HIVE_HEALTH_EXAMPLE = (
    "A beekeeper reports low hive activity, ants near the hive stand, normal "
    "smell, and partially capped brood. What should they check first, and what "
    "should they avoid doing immediately?"
)
SITE_READINESS_EXAMPLE = (
    "An extension worker wants to place 20 hives near cassava, mango, pepper, "
    "and vegetable farms with a seasonal water source nearby. What site risks "
    "and forage factors should they evaluate before placing the hives?"
)
HARVEST_QUALITY_EXAMPLE = (
    "A beekeeper is preparing to harvest honey after a rainy week. Some frames "
    "are mostly capped, the smoker was used heavily, and the honey will be stored "
    "in plastic buckets. What quality risks should they check before harvesting "
    "and storing?"
)
FORAGE_POLLINATION_EXAMPLE = (
    "A beekeeper wants to support mango, pepper, and vegetable farms, but there "
    "may be a flowering gap after mango season and pesticide spraying nearby. "
    "What forage and pollination factors should they evaluate?"
)
HIVE_SIGNAL_EXAMPLE = (
    "A hive shows rising temperature, dropping humidity, low entrance activity, "
    "and bees clustering outside in the afternoon. What should the beekeeper "
    "check first, and what should they avoid doing immediately?"
)

HIVE_HEALTH = {
    "title": "Hive Health Advisor",
    "helper": (
        "Ask an English hive-health question. The answer runs locally through "
        "the Granite model and the public apiculture knowledge base. No cloud "
        "access."
    ),
    "page_note": NOT_DIAGNOSIS,
    "action": "/advisor/hive-health",
    "label": "Your hive-health question",
    "placeholder": "Describe what you are seeing at the hive...",
    "example": HIVE_HEALTH_EXAMPLE,
    "validation": "Please enter a hive-health question before submitting.",
    "error": (
        "HyveGrid could not complete this local answer. Confirm the model is "
        "downloaded and llama.cpp is available, then try again."
    ),
}

SITE_READINESS = {
    "title": "Site Readiness Advisor",
    "helper": (
        "Ask an English site-readiness or apiary-siting question. The answer "
        "runs locally through the Granite model and the public apiculture "
        "knowledge base. No cloud access."
    ),
    "page_note": (
        "Local and offline. HyveGrid is a field tool, not a certified site "
        "approval tool."
    ),
    "action": "/advisor/site-readiness",
    "label": "Your site-readiness question",
    "placeholder": "Describe the apiary site you are evaluating...",
    "example": SITE_READINESS_EXAMPLE,
    "validation": "Please enter a site-readiness question before submitting.",
    "error": (
        "HyveGrid could not complete this local site-readiness answer. Confirm "
        "the model is downloaded and llama.cpp is available, then try again."
    ),
}

HARVEST_QUALITY = {
    "title": "Harvest Quality Coach",
    "helper": (
        "Ask an English harvest and honey-handling question. The answer runs "
        "locally through the Granite model and the public apiculture knowledge "
        "base. No cloud access."
    ),
    "page_note": (
        "Local and offline. HyveGrid is a field tool, not a certified food-safety "
        "or lab test."
    ),
    "action": "/advisor/harvest-quality",
    "label": "Your harvest-quality question",
    "placeholder": "Describe the harvest, frames, and storage conditions...",
    "example": HARVEST_QUALITY_EXAMPLE,
    "validation": "Please enter a harvest-quality question before submitting.",
    "error": (
        "HyveGrid could not complete this local harvest-quality answer. Confirm "
        "the model is downloaded and llama.cpp is available, then try again."
    ),
}

FORAGE_POLLINATION = {
    "title": "Forage and Pollination Guide",
    "helper": (
        "Ask an English forage and pollination question. The answer runs locally "
        "through the Granite model and the public apiculture knowledge base. No "
        "cloud access."
    ),
    "page_note": (
        "Local and offline. HyveGrid is a field tool, not a certified agronomy "
        "recommendation."
    ),
    "action": "/advisor/forage-pollination",
    "label": "Your forage and pollination question",
    "placeholder": "Describe the crops, flowering season, and pesticide context...",
    "example": FORAGE_POLLINATION_EXAMPLE,
    "validation": "Please enter a forage and pollination question before submitting.",
    "error": (
        "HyveGrid could not complete this local forage and pollination answer. "
        "Confirm the model is downloaded and llama.cpp is available, then try again."
    ),
}

HIVE_SIGNAL = {
    "title": "Hive Signal Check",
    "helper": (
        "Ask an English hive-signal question (temperature, humidity, activity, "
        "clustering, ventilation). The answer runs locally through the Granite "
        "model and the public apiculture knowledge base. No cloud access."
    ),
    "page_note": (
        "Local and offline. Hive signals are not a diagnosis without physical "
        "inspection."
    ),
    "action": "/advisor/hive-signal",
    "label": "Your hive-signal question",
    "placeholder": "Describe the signals you are observing at the hive...",
    "example": HIVE_SIGNAL_EXAMPLE,
    "validation": "Please enter a hive-signal question before submitting.",
    "error": (
        "HyveGrid could not complete this local hive-signal answer. Confirm the "
        "model is downloaded and llama.cpp is available, then try again."
    ),
}

RUNTIME_OK = "Completed locally."


def _advisor_context(advisor: dict) -> dict:
    """Base template context for an advisor form page."""
    return {
        "title": advisor["title"],
        "helper": advisor["helper"],
        "page_note": advisor["page_note"],
        "action": advisor["action"],
        "label": advisor["label"],
        "placeholder": advisor["placeholder"],
        "example_prompt": advisor["example"],
        "not_diagnosis": NOT_DIAGNOSIS,
        "submitted_question": "",
    }


async def _submit_advisor_question(request: Request, advisor: dict) -> HTMLResponse:
    """Shared POST logic for advisor forms.

    Parses the urlencoded form body (no python-multipart dependency), validates
    the question, runs answer_question() off the event loop, and renders the
    advisor page with the answer and sources or a safe error. Raw stdout, prompt
    text, command details, and stack traces are never shown to the user.
    """
    ctx = _advisor_context(advisor)

    raw = await request.body()
    form = urllib.parse.parse_qs(
        raw.decode("utf-8", "replace"), keep_blank_values=True
    )
    question = (form.get("question", [""])[0] or "").strip()

    if not question:
        ctx["validation_error"] = advisor["validation"]
        return TEMPLATES.TemplateResponse(request, "advisor_form.html", ctx)

    ctx["submitted_question"] = question

    # answer_question() is blocking (model load + generation) and can take
    # minutes; run it off the event loop so the server stays responsive.
    try:
        bundle = await asyncio.to_thread(answer_question, question)
    except Exception:
        # Do not expose stack traces or internal details to the user.
        ctx["error_message"] = advisor["error"]
        return TEMPLATES.TemplateResponse(request, "advisor_form.html", ctx)

    runtime = bundle.get("runtime") or {}
    answer = (bundle.get("answer") or "").strip()
    ok = (
        not runtime.get("timed_out")
        and runtime.get("returncode") == 0
        and bool(answer)
    )
    if not ok:
        ctx["error_message"] = advisor["error"]
        return TEMPLATES.TemplateResponse(request, "advisor_form.html", ctx)

    ctx["answer"] = answer
    ctx["sources"] = bundle.get("results") or []
    ctx["runtime_ok"] = RUNTIME_OK
    return TEMPLATES.TemplateResponse(request, "advisor_form.html", ctx)


@app.get("/advisor/hive-health", response_class=HTMLResponse)
async def hive_health_form(request: Request) -> HTMLResponse:
    """Render the Hive Health Advisor form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(HIVE_HEALTH)
    )


@app.post("/advisor/hive-health", response_class=HTMLResponse)
async def hive_health_submit(request: Request) -> HTMLResponse:
    """Handle a submitted hive-health question through the offline answer path."""
    return await _submit_advisor_question(request, HIVE_HEALTH)


@app.get("/advisor/site-readiness", response_class=HTMLResponse)
async def site_readiness_form(request: Request) -> HTMLResponse:
    """Render the Site Readiness Advisor form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(SITE_READINESS)
    )


@app.post("/advisor/site-readiness", response_class=HTMLResponse)
async def site_readiness_submit(request: Request) -> HTMLResponse:
    """Handle a submitted site-readiness question through the offline answer path."""
    return await _submit_advisor_question(request, SITE_READINESS)


@app.get("/advisor/harvest-quality", response_class=HTMLResponse)
async def harvest_quality_form(request: Request) -> HTMLResponse:
    """Render the Harvest Quality Coach form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(HARVEST_QUALITY)
    )


@app.post("/advisor/harvest-quality", response_class=HTMLResponse)
async def harvest_quality_submit(request: Request) -> HTMLResponse:
    """Handle a submitted harvest-quality question through the offline answer path."""
    return await _submit_advisor_question(request, HARVEST_QUALITY)


@app.get("/advisor/forage-pollination", response_class=HTMLResponse)
async def forage_pollination_form(request: Request) -> HTMLResponse:
    """Render the Forage and Pollination Guide form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(FORAGE_POLLINATION)
    )


@app.post("/advisor/forage-pollination", response_class=HTMLResponse)
async def forage_pollination_submit(request: Request) -> HTMLResponse:
    """Handle a submitted forage and pollination question through the offline path."""
    return await _submit_advisor_question(request, FORAGE_POLLINATION)


@app.get("/advisor/hive-signal", response_class=HTMLResponse)
async def hive_signal_form(request: Request) -> HTMLResponse:
    """Render the Hive Signal Check form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(HIVE_SIGNAL)
    )


@app.post("/advisor/hive-signal", response_class=HTMLResponse)
async def hive_signal_submit(request: Request) -> HTMLResponse:
    """Handle a submitted hive-signal question through the offline answer path."""
    return await _submit_advisor_question(request, HIVE_SIGNAL)


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
