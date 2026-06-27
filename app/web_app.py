"""Local web UI for HyveGrid Offline (ADTC 2026).

A minimal FastAPI app serving screens at localhost:

- Mission Control (/): overview and navigation cards.
- Offline System Status (/status): runtime, model, retrieval, compliance, and
  benchmark evidence.
- Hive Health Advisor (/advisor/hive-health): a form that runs a real local
  answer through the existing offline path (retrieval + prompt builder +
  llama.cpp + Granite).
- Site Readiness Advisor (/advisor/site-readiness): same, for apiary siting and
  site-readiness questions.

It serves localhost only, uses no cloud services, and loads no GGUF model at
import time. The status values are drawn from completed profiler/runtime
evidence. The wired advisors call answer_question() on submit, which runs the
model. Yoruba mode uses controlled UI labels, glossary terms, and template
headings; it does not ask Granite to freestyle Yoruba.

Run with:
    python3 -m app.web_app
or:
    python3 scripts/run_web_app.py

Then open http://127.0.0.1:8000
"""

import asyncio
import logging
import os
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
from app.llama_runtime import (
    DEFAULT_LLAMA_BIN,
    DEFAULT_MODEL_PATH,
    answer_question,
    log_runtime_diagnostics,
)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))
STATIC_DIR = BASE_DIR / "static"
LOGGER = logging.getLogger(__name__)

LLAMA_BIN_ENV = "LLAMA_BIN"
MODEL_PATH_ENV = "HYVEGRID_MODEL_PATH"

app = FastAPI(
    title="HyveGrid Offline",
    description="Local offline apiculture assistant (ADTC 2026 public edition).",
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

APP_DESCRIPTION = (
    "Offline apiculture intelligence for African beekeepers and extension workers."
)

LANGUAGES = {
    "en": {"code": "en", "name": "English", "native": "English"},
    "yo": {"code": "yo", "name": "Yoruba", "native": "Yorùbá"},
}

ACTIVE_LANGUAGE_CODES = ("en", "yo")

YO_REVIEW_NOTE = (
    "Yoruba field labels and templates are controlled draft support and should "
    "be reviewed by a fluent Yoruba speaker before final submission."
)

UI_TEXT = {
    "en": {
        "mission_control": "Mission Control",
        "hive_health": "Hive Health Advisor",
        "site_readiness": "Site Readiness Advisor",
        "harvest_quality": "Harvest Quality Coach",
        "forage_pollination": "Forage and Pollination Guide",
        "hive_signal": "Hive Signal Check",
        "offline_status": "Offline System Status",
        "ask_locally": "Ask locally",
        "back_to_mission_control": "Back to Mission Control",
        "example_prompt": "Example prompt",
        "example_hint": "does not run automatically",
        "offline_mode": "Offline mode",
        "model_loaded": "Model loaded",
        "local_app": "Local app",
        "no_cloud_access": "No cloud access",
        "public_challenge_edition": "Public challenge edition",
        "field_guidance_only": "Field guidance only",
        "answer": "Answer",
        "english_answer": "English model answer",
        "retrieved_sources": "Retrieved sources",
        "glossary": "Yoruba field glossary",
        "language": "Language",
        "english": "English",
        "yoruba": "Yorùbá",
        "available_now": "Available now",
        "planned_for_demo": "Planned for demo",
        "system_facts": "System facts",
        "latest_benchmark": "Latest benchmark evidence",
        "accuracy_status": "Accuracy status",
    },
    # Provisional reviewed-by-human-needed labels for Task 028.
    "yo": {
        "mission_control": "Ibi Ìṣàkóso",
        "hive_health": "Olùrànlọ́wọ́ Ìlera Ilé Oyin",
        "site_readiness": "Olùrànlọ́wọ́ Ìmúrasílẹ̀ Ibi Ilé Oyin",
        "harvest_quality": "Olùkọ́ Didara Ikórè Oyin",
        "forage_pollination": "Ìtọ́nisọ́nà Oúnjẹ Oyin àti Ìpolínéṣọ̀nù",
        "hive_signal": "Àyẹ̀wò Àmì Ilé Oyin",
        "offline_status": "Ipò Ẹ̀rọ Àìsí Ayélujára",
        "ask_locally": "Béèrè lórí kọ̀ǹpútà yìí",
        "back_to_mission_control": "Padà sí Ibi Ìṣàkóso",
        "example_prompt": "Àpẹẹrẹ ìbéèrè",
        "example_hint": "kì í ṣiṣẹ́ fúnra rẹ̀",
        "offline_mode": "Ìpo àìsí ayélujára",
        "model_loaded": "Módẹ́lì ti wà fún lílò",
        "local_app": "App lórí kọ̀ǹpútà yìí",
        "no_cloud_access": "Kò sí ìráyè sí cloud",
        "public_challenge_edition": "Ẹ̀dà ìdíje fún gbogbo ènìyàn",
        "field_guidance_only": "Ìtọ́nisọ́nà pápá nìkan",
        "answer": "Ìdáhùn",
        "english_answer": "Ìdáhùn módẹ́lì ní Gẹ̀ẹ́sì",
        "retrieved_sources": "Àwọn orísun tí a rí",
        "glossary": "Àkójọ ọ̀rọ̀ pápá Yorùbá",
        "language": "Èdè",
        "english": "Gẹ̀ẹ́sì",
        "yoruba": "Yorùbá",
        "available_now": "Ó wà báyìí",
        "planned_for_demo": "A pèsè fún ìfihàn",
        "system_facts": "Àwọn òtítọ́ nípa ẹ̀rọ",
        "latest_benchmark": "Ẹ̀rí benchmark tuntun",
        "accuracy_status": "Ipò ìpéye",
    },
}

YO_CONTROLLED_HEADINGS = [
    ("field_observation_summary", "Àkótán ohun tí a rí ní pápá"),
    ("possible_concern", "Ohun tó lè jẹ́ ìṣòro"),
    ("check_first", "Ṣàyẹ̀wò èyí kọ́kọ́"),
    ("avoid_immediately", "Má ṣe èyí lẹ́sẹ̀kẹsẹ̀"),
    ("next_safe_action", "Ìgbésẹ̀ àìléwu tó kàn"),
    (
        "consult",
        "Bèrè lọ́wọ́ agbẹ oyin tó ní ìrírí tàbí òṣiṣẹ́ ìtẹ̀síwájú agbẹ",
    ),
    ("english_fallback", "Àkọsílẹ̀ ìpadà sí Gẹ̀ẹ́sì"),
]

YO_CONTROLLED_GUIDANCE = {
    "field_observation_summary": (
        "Lo àwọn ohun tí agbẹ oyin kọ sínú fọ́ọ̀mù gẹ́gẹ́ bí àkótán pápá."
    ),
    "possible_concern": (
        "Wo èyí gẹ́gẹ́ bí ohun tó lè jẹ́ ìṣòro, kì í ṣe ìdánimọ̀ àrùn tó dájú."
    ),
    "check_first": (
        "Ṣàyẹ̀wò ilé oyin, oyin, omi, afẹ́fẹ́, oúnjẹ, àti àyíká pẹ̀lú ojú àti ọwọ́."
    ),
    "avoid_immediately": (
        "Má ṣe ìtọ́jú tó lágbára tàbí ìyípadà ńlá lẹ́sẹ̀kẹsẹ̀ láì jẹ́rìí sí i."
    ),
    "next_safe_action": (
        "Jẹ́rìí sí i pẹ̀lú àyẹ̀wò ojú àti ọwọ́, kí o sì kọ ohun tí o rí sílẹ̀."
    ),
    "consult": (
        "Bèrè lọ́wọ́ agbẹ oyin tó ní ìrírí tàbí òṣiṣẹ́ ìtẹ̀síwájú agbẹ tí ọ̀rọ̀ bá "
        "le, bá burú, tàbí kò ye ọ."
    ),
    "english_fallback": (
        "Ìdáhùn kikún ti módẹ́lì wà ní Gẹ̀ẹ́sì ní isalẹ. Àwọn gbolohun Yorùbá "
        "wọ̀nyí jẹ́ template tó ní ààbò, kì í ṣe ìtumọ̀ aládàáṣiṣẹ́."
    ),
}

YO_GLOSSARY = [
    {
        "category": "Hive and colony terms",
        "yo_category": "Ọ̀rọ̀ ilé oyin àti agbo oyin",
        "terms": [
            ("hive", "ilé oyin"),
            ("colony", "agbo oyin"),
            ("brood", "ọmọ oyin"),
            ("queen", "ayaba oyin"),
            ("entrance", "ẹnu-ọ̀nà ilé oyin"),
        ],
    },
    {
        "category": "Pest and disease pressure terms",
        "yo_category": "Ọ̀rọ̀ kokoro àti ìfihàn àìlera",
        "terms": [
            ("ants", "kokoro èèrà"),
            ("wax moth", "kokoro wax moth"),
            ("weak colony", "agbo oyin aláìlera"),
            ("abnormal smell", "òórùn tí kò bójú mu"),
        ],
    },
    {
        "category": "Site and forage terms",
        "yo_category": "Ọ̀rọ̀ ibi, ewéko, àti oúnjẹ oyin",
        "terms": [
            ("shade", "òjìji"),
            ("water source", "orisun omi"),
            ("pesticide", "oògùn kokoro"),
            ("flowering crops", "irúgbìn tó ń yọ òdòdó"),
        ],
    },
    {
        "category": "Harvest and honey quality terms",
        "yo_category": "Ọ̀rọ̀ ikórè àti didara oyin",
        "terms": [
            ("capped frame", "fireemu tí oyin ti bo"),
            ("moisture", "ọrinrin"),
            ("smoke contamination", "ìdọ̀tí ẹfin"),
            ("food-grade container", "àpò ìpamọ́ tó yẹ fún oúnjẹ"),
        ],
    },
    {
        "category": "Signal/status terms",
        "yo_category": "Ọ̀rọ̀ àmì àti ipò",
        "terms": [
            ("temperature", "ìwọ̀n ooru"),
            ("humidity", "ọrinrin afẹ́fẹ́"),
            ("entrance activity", "ìrìn-àjò ní ẹnu-ọ̀nà"),
            ("ventilation", "ìfẹ́fẹ́ wọlé-jáde"),
        ],
    },
    {
        "category": "Safety and caution terms",
        "yo_category": "Ọ̀rọ̀ ààbò àti ìkìlọ̀",
        "terms": [
            ("possible concern", "ohun tó lè jẹ́ ìṣòro"),
            ("check first", "ṣàyẹ̀wò èyí kọ́kọ́"),
            ("avoid immediately", "má ṣe èyí lẹ́sẹ̀kẹsẹ̀"),
            (
                "confirm by physical inspection",
                "jẹ́rìí sí i pẹ̀lú àyẹ̀wò ojú àti ọwọ́",
            ),
        ],
    },
]

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

ADVISOR_ASSETS = {
    "hive-health": "/static/assets/card-hive-health.webp",
    "site-readiness": "/static/assets/card-site-readiness.webp",
    "harvest-quality": "/static/assets/card-harvest-quality.webp",
    "forage-pollination": "/static/assets/card-forage-pollination.webp",
    "hive-signal": "/static/assets/card-hive-signal.webp",
}

MISSION_ASSETS = {
    "hero_bg": "/static/assets/hero-honeycomb-bg.webp",
    "logo_mark": "/static/assets/logo-honeycomb-mark.webp",
    "hero_bee": "/static/assets/hero-bee.webp",
    "offline_status": "/static/assets/card-offline-status.webp",
}

GUIDANCE_CARDS = [
    {
        "title": "Yoruba Template",
        "body": "Controlled Yoruba labels and field guidance templates.",
        "asset": "/static/assets/guide-yoruba-template.webp",
        "href": "/?lang=yo",
    },
    {
        "title": "Ask the Hive Advisor",
        "body": "Start with a local advisor question and public field notes.",
        "asset": "/static/assets/guide-ask-advisor.webp",
        "href": "/advisor/hive-health",
    },
    {
        "title": "Daily Hive Checklist",
        "body": "Observe activity, brood, pests, stores, water, and shade.",
        "asset": "/static/assets/guide-daily-checklist.webp",
        "href": None,
    },
    {
        "title": "Storage & Handling",
        "body": "Keep harvest checks focused on clean, dry, food-safe handling.",
        "asset": "/static/assets/guide-storage-handling.webp",
        "href": "/advisor/harvest-quality",
    },
    {
        "title": "Pesticide Awareness",
        "body": "Coordinate with farms and avoid exposure during bee flight.",
        "asset": "/static/assets/guide-pesticide-awareness.webp",
        "href": "/advisor/forage-pollination",
    },
    {
        "title": "Forage Calendar",
        "body": "Track flowering gaps, crop seasons, and backup forage.",
        "asset": "/static/assets/guide-forage-calendar.webp",
        "href": "/advisor/forage-pollination",
    },
]

AT_A_GLANCE = [
    ("Offline local app", "Runs at localhost with no judged-runtime cloud dependency."),
    ("llama.cpp runtime", "Local GGUF inference path for advisor answers."),
    ("GGUF model", "Locked Granite 3.3 2B Instruct Q4_K_M candidate."),
    ("SQLite FTS5 retrieval", "Public apiculture notes remain local."),
    ("Yoruba mode", "Controlled labels, glossary, and English fallback."),
    ("Public challenge edition", "No proprietary hardware, sensor IP, or private data."),
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
LOCAL_RUNTIME_ERROR = (
    "HyveGrid could not complete this local answer. The advisor request reached "
    "the offline app, but the local model runtime failed. Check the server log "
    "for the exact model/runtime path issue."
)


def _advisor_runtime_paths() -> tuple[str, str]:
    """Resolve preview/runtime paths from env while preserving Ubuntu defaults."""
    llama_bin = os.environ.get(LLAMA_BIN_ENV, DEFAULT_LLAMA_BIN)
    model_path = os.environ.get(MODEL_PATH_ENV, DEFAULT_MODEL_PATH)
    return llama_bin, model_path


def _runtime_error_message(exc: Exception) -> str:
    """Add local-preview repair hints to runtime path errors for server logs."""
    message = str(exc)
    if message.startswith("llama.cpp binary not found at "):
        return message.replace(
            "Build llama.cpp and check the path.",
            "Set LLAMA_BIN to a local llama-cli path or build llama.cpp and check the path.",
        )
    if message.startswith("Model file not found at "):
        return message.replace(
            "Model file not found",
            "GGUF model not found",
        ).replace(
            "Download or link the GGUF model and check the path.",
            "Set HYVEGRID_MODEL_PATH or run the model download/setup step.",
        )
    return message

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
    "slug": "hive-health",
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
    "error": LOCAL_RUNTIME_ERROR,
}

SITE_READINESS = {
    "slug": "site-readiness",
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
    "error": LOCAL_RUNTIME_ERROR,
}

HARVEST_QUALITY = {
    "slug": "harvest-quality",
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
    "error": LOCAL_RUNTIME_ERROR,
}

FORAGE_POLLINATION = {
    "slug": "forage-pollination",
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
    "error": LOCAL_RUNTIME_ERROR,
}

HIVE_SIGNAL = {
    "slug": "hive-signal",
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
    "error": LOCAL_RUNTIME_ERROR,
}

ADVISOR_WALKTHROUGH_STEPS = {
    "hive-health": [
        "Walking to hive",
        "Checking entrance activity",
        "Looking for ant trails near the stand",
        "Inspecting brood pattern",
        "Confirming normal smell report",
        "Checking food stores",
        "Preparing local guidance",
    ],
    "site-readiness": [
        "Reviewing proposed apiary area",
        "Checking crop zones",
        "Checking water reliability",
        "Checking shade and wind exposure",
        "Looking for pesticide risk",
        "Checking human and livestock safety",
        "Preparing placement guidance",
    ],
    "harvest-quality": [
        "Reviewing harvest timing",
        "Checking capped honey",
        "Watching moisture risk",
        "Checking smoke exposure",
        "Reviewing filtering and storage",
        "Preparing quality guidance",
    ],
    "forage-pollination": [
        "Mapping forage sources",
        "Checking flowering gaps",
        "Reviewing crop pollination needs",
        "Checking pesticide timing",
        "Reviewing water and shade",
        "Preparing forage guidance",
    ],
    "hive-signal": [
        "Reviewing sample edge-signal inputs",
        "Checking activity level",
        "Checking temperature pattern",
        "Checking humidity pattern",
        "Looking for clustering outside",
        "Preparing signal guidance",
    ],
}

ADVISOR_ROUTE_POINTS = {
    "hive-health": [
        "Walking to hive",
        "Checking entrance activity",
        "Looking for ant trails near the stand",
        "Reviewing brood and food check",
        "Preparing local guidance",
    ],
    "site-readiness": [
        "Walking the proposed apiary area",
        "Checking water source",
        "Checking crop zones",
        "Checking shade and wind exposure",
        "Reviewing pesticide risk",
        "Preparing placement guidance",
    ],
    "harvest-quality": [
        "Walking to hive area",
        "Reviewing harvest timing",
        "Checking capped honey marker",
        "Moving toward storage/hut area",
        "Reviewing filtering and storage",
        "Preparing harvest guidance",
    ],
    "forage-pollination": [
        "Walking from apiary to crop edge",
        "Checking crop plots",
        "Checking flowering/forage area",
        "Checking water and shade",
        "Preparing forage guidance",
    ],
    "hive-signal": [
        "Walking to hive area",
        "Checking activity marker",
        "Checking temperature-style marker",
        "Checking humidity-style marker",
        "Reviewing clustering/activity note",
        "Preparing signal guidance",
    ],
}

RUNTIME_OK = "Completed locally."


def _lang_from_request(request: Request) -> str:
    lang = (request.query_params.get("lang") or "en").lower()
    return lang if lang in LANGUAGES else "en"


def _url_with_lang(path: str, lang: str) -> str:
    return f"{path}?lang={lang}" if lang != "en" else path


def _localize_advisor(advisor: dict, lang: str) -> dict:
    text = UI_TEXT[lang]
    names = {
        "hive-health": text["hive_health"],
        "site-readiness": text["site_readiness"],
        "harvest-quality": text["harvest_quality"],
        "forage-pollination": text["forage_pollination"],
        "hive-signal": text["hive_signal"],
    }
    localized = dict(advisor)
    localized["name"] = names.get(advisor["slug"], advisor["name"])
    localized["href"] = _url_with_lang(f"/advisor/{advisor['slug']}", lang)
    localized["asset"] = ADVISOR_ASSETS.get(advisor["slug"])
    return localized


def _localized_guidance_cards(lang: str) -> list[dict]:
    cards = []
    for card in GUIDANCE_CARDS:
        localized = dict(card)
        if card["href"]:
            localized["href"] = _url_with_lang(card["href"], lang)
        cards.append(localized)
    return cards


def _base_context(request: Request) -> dict:
    lang = _lang_from_request(request)
    text = UI_TEXT[lang]
    language_options = [
        {
            "code": code,
            "label": text["english"] if code == "en" else text["yoruba"],
            "url": _url_with_lang(request.url.path, code),
            "selected": code == lang,
        }
        for code in ACTIVE_LANGUAGE_CODES
    ]
    return {
        "lang": lang,
        "html_lang": "yo" if lang == "yo" else "en",
        "text": text,
        "is_yoruba": lang == "yo",
        "lang_en_url": _url_with_lang(request.url.path, "en"),
        "lang_yo_url": _url_with_lang(request.url.path, "yo"),
        "language_options": language_options,
        "mission_control_url": _url_with_lang("/", lang),
        "status_url": _url_with_lang("/status", lang),
        "not_diagnosis": NOT_DIAGNOSIS,
        "yo_review_note": YO_REVIEW_NOTE,
    }


def _advisor_context(request: Request, advisor: dict) -> dict:
    """Base template context for an advisor form page."""
    ctx = _base_context(request)
    lang = ctx["lang"]
    localized = _localize_advisor(
        {"slug": advisor["slug"], "name": advisor["title"], "blurb": ""}, lang
    )
    ctx.update({
        "title": localized["name"],
        "advisor_slug": advisor["slug"],
        "advisor_asset": ADVISOR_ASSETS.get(advisor["slug"]),
        "advisor_logo_mark": MISSION_ASSETS["logo_mark"],
        "helper": advisor["helper"],
        "page_note": advisor["page_note"],
        "action": _url_with_lang(advisor["action"], lang),
        "label": advisor["label"],
        "placeholder": advisor["placeholder"],
        "example_prompt": advisor["example"],
        "submitted_question": "",
        "walkthrough_steps": ADVISOR_WALKTHROUGH_STEPS[advisor["slug"]],
        "walkthrough_route_points": ADVISOR_ROUTE_POINTS[advisor["slug"]],
        "controlled_headings": YO_CONTROLLED_HEADINGS if lang == "yo" else [],
        "controlled_guidance": YO_CONTROLLED_GUIDANCE,
        "glossary": YO_GLOSSARY if lang == "yo" else [],
    })
    return ctx


def _status_facts(lang: str) -> list[tuple[str, str]]:
    if lang != "yo":
        return STATUS_FACTS

    text = UI_TEXT["yo"]
    return [
        ("Runtime", "llama.cpp"),
        ("Model format", "GGUF"),
        (text["model_loaded"], "Granite 3.3 2B Instruct Q4_K_M"),
        ("Profiler model path", "model.gguf"),
        (text["local_app"], "localhost (http://127.0.0.1:8000)"),
        ("Retrieval", "SQLite FTS5 local knowledge base"),
        (text["no_cloud_access"], "none during judged runtime"),
        (text["public_challenge_edition"], "yes"),
        ("Proprietary hardware or sensor IP included", "no"),
        ("Metadata email finalized", "yes"),
        ("Two official prompts configured", "yes"),
    ]


async def _submit_advisor_question(request: Request, advisor: dict) -> HTMLResponse:
    """Shared POST logic for advisor forms.

    Parses the urlencoded form body (no python-multipart dependency), validates
    the question, runs answer_question() off the event loop, and renders the
    advisor page with the answer and sources or a safe error. Raw stdout, prompt
    text, command details, and stack traces are never shown to the user.
    """
    ctx = _advisor_context(request, advisor)

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
        llama_bin, model_path = _advisor_runtime_paths()
        log_runtime_diagnostics(model_path=model_path, llama_bin=llama_bin)
        bundle = await asyncio.to_thread(
            answer_question,
            question,
            model_path=model_path,
            llama_bin=llama_bin,
        )
    except Exception as exc:
        # Do not expose stack traces or internal details to the user.
        LOGGER.error(
            "Local advisor generation failed for %s: %s: %s",
            advisor["slug"],
            type(exc).__name__,
            _runtime_error_message(exc),
        )
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
        LOGGER.error(
            "Local advisor runtime returned no answer for %s: returncode=%s "
            "timed_out=%s stderr_chars=%s stdout_chars=%s",
            advisor["slug"],
            runtime.get("returncode"),
            runtime.get("timed_out"),
            len(runtime.get("stderr") or ""),
            len(runtime.get("stdout") or ""),
        )
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
        request, "advisor_form.html", _advisor_context(request, HIVE_HEALTH)
    )


@app.post("/advisor/hive-health", response_class=HTMLResponse)
async def hive_health_submit(request: Request) -> HTMLResponse:
    """Handle a submitted hive-health question through the offline answer path."""
    return await _submit_advisor_question(request, HIVE_HEALTH)


@app.get("/advisor/site-readiness", response_class=HTMLResponse)
async def site_readiness_form(request: Request) -> HTMLResponse:
    """Render the Site Readiness Advisor form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(request, SITE_READINESS)
    )


@app.post("/advisor/site-readiness", response_class=HTMLResponse)
async def site_readiness_submit(request: Request) -> HTMLResponse:
    """Handle a submitted site-readiness question through the offline answer path."""
    return await _submit_advisor_question(request, SITE_READINESS)


@app.get("/advisor/harvest-quality", response_class=HTMLResponse)
async def harvest_quality_form(request: Request) -> HTMLResponse:
    """Render the Harvest Quality Coach form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(request, HARVEST_QUALITY)
    )


@app.post("/advisor/harvest-quality", response_class=HTMLResponse)
async def harvest_quality_submit(request: Request) -> HTMLResponse:
    """Handle a submitted harvest-quality question through the offline answer path."""
    return await _submit_advisor_question(request, HARVEST_QUALITY)


@app.get("/advisor/forage-pollination", response_class=HTMLResponse)
async def forage_pollination_form(request: Request) -> HTMLResponse:
    """Render the Forage and Pollination Guide form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(request, FORAGE_POLLINATION)
    )


@app.post("/advisor/forage-pollination", response_class=HTMLResponse)
async def forage_pollination_submit(request: Request) -> HTMLResponse:
    """Handle a submitted forage and pollination question through the offline path."""
    return await _submit_advisor_question(request, FORAGE_POLLINATION)


@app.get("/advisor/hive-signal", response_class=HTMLResponse)
async def hive_signal_form(request: Request) -> HTMLResponse:
    """Render the Hive Signal Check form (no model load on GET)."""
    return TEMPLATES.TemplateResponse(
        request, "advisor_form.html", _advisor_context(request, HIVE_SIGNAL)
    )


@app.post("/advisor/hive-signal", response_class=HTMLResponse)
async def hive_signal_submit(request: Request) -> HTMLResponse:
    """Handle a submitted hive-signal question through the offline answer path."""
    return await _submit_advisor_question(request, HIVE_SIGNAL)


@app.get("/", response_class=HTMLResponse)
async def mission_control(request: Request) -> HTMLResponse:
    """Mission Control: overview and navigation cards."""
    ctx = _base_context(request)
    lang = ctx["lang"]
    text = ctx["text"]
    ctx.update({
        "description": APP_DESCRIPTION,
        "advisors": [_localize_advisor(a, lang) for a in ADVISORS],
        "status_card_url": _url_with_lang("/status", lang),
        "status_card_title": text["offline_status"],
        "status_card_blurb": (
            "Runtime, model, retrieval, compliance, and benchmark evidence."
        ),
        "status_markers": [
            text["offline_mode"],
            text["local_app"],
            text["no_cloud_access"],
            text["public_challenge_edition"],
            text["field_guidance_only"],
        ],
        "mission_assets": MISSION_ASSETS,
        "guidance_cards": _localized_guidance_cards(lang),
        "at_a_glance": AT_A_GLANCE,
        "glossary": YO_GLOSSARY if lang == "yo" else [],
    })
    return TEMPLATES.TemplateResponse(
        request,
        "index.html",
        ctx,
    )


@app.get("/status", response_class=HTMLResponse)
async def offline_system_status(request: Request) -> HTMLResponse:
    """Offline System Status: runtime, model, retrieval, compliance, evidence."""
    ctx = _base_context(request)
    lang = ctx["lang"]
    text = ctx["text"]
    ctx.update({
        "title": text["offline_status"],
        "facts": _status_facts(lang),
        "benchmarks": BENCHMARK_EVIDENCE,
        "accuracy_status": ACCURACY_STATUS,
        "status_markers": [
            text["offline_mode"],
            text["model_loaded"],
            text["local_app"],
            text["no_cloud_access"],
            text["public_challenge_edition"],
            text["field_guidance_only"],
        ],
    })
    return TEMPLATES.TemplateResponse(
        request,
        "status.html",
        ctx,
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
        {**_base_context(request), "advisor": _localize_advisor(advisor, _lang_from_request(request))},
    )


@app.get("/health")
async def health() -> dict:
    """Lightweight liveness check for local testing (no model load)."""
    return {"status": "ok", "mode": "localhost"}


if __name__ == "__main__":
    # Pass the app object (not an import string) so `python3 -m app.web_app`
    # does not import the module twice.
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
