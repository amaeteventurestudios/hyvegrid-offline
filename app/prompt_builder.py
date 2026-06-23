"""Prompt builder for HyveGrid Offline.

Combines a user field question with public apiculture notes retrieved by the
local SQLite FTS layer into a single cautious, llama.cpp-ready prompt string.

This module builds prompts only. It does not call llama.cpp and does not run
model inference. Standard library only, plus the local app.retrieval layer.

HyveGrid is not a certified disease diagnosis tool. The prompts it builds ask
for field triage and next-step guidance only.
"""

from app.retrieval import (
    DEFAULT_DB_PATH,
    build_or_open_db,
    format_retrieval_context,
    search_knowledge,
)

# Only English is supported for now. Yoruba is intentionally not added yet.
SUPPORTED_LANGUAGES = {"en"}

REQUIRED_ANSWER_FORMAT = """Answer using exactly these five sections, in order:

1. Possible concern
2. Check first
3. Avoid doing immediately
4. Suggested next step
5. When to escalate

Keep wording cautious and practical. If the retrieved notes do not cover the
situation, say what to inspect next instead of pretending certainty."""


def build_system_instructions() -> str:
    """Return the cautious system instruction block for the assistant.

    This is the only place the assistant's role and constraints are stated, so
    the wording is kept deliberate: offline-only, public-notes-only, field
    triage (not certified diagnosis), cautious language, and escalation.
    """
    return (
        "You are HyveGrid Offline, an offline apiculture field assistant for "
        "beekeepers and extension workers.\n"
        "\n"
        "Base your answer only on the retrieved public apiculture notes provided "
        "below and the user's own observations. Do not use cloud results or any "
        "outside data.\n"
        "\n"
        "Provide field triage, checklist reasoning, and practical next steps.\n"
        "\n"
        "You are not a certified disease diagnosis tool. Do not claim certified "
        "diagnosis or certainty about disease. Use cautious language such as "
        "\"possible concern\", \"check first\", \"avoid doing immediately\", and "
        "\"confirm by physical inspection\".\n"
        "\n"
        "Recommend consulting an experienced beekeeper or extension officer when "
        "the situation is serious or unclear.\n"
        "\n"
        "Do not invent proprietary sensor data, private datasets, partner "
        "details, or cloud results. If the provided context is insufficient, say "
        "what to inspect next instead of pretending certainty."
    )


def build_user_task(question: str) -> str:
    """Return the structured task section containing the user's question."""
    question = (question or "").strip()
    return (
        "Read the field question below and answer using the retrieved public "
        "apiculture notes and the required answer format.\n"
        "\n"
        "Question:\n"
        f"{question}"
    )


def build_hyvegrid_prompt(question: str, context: str, language: str = "en") -> str:
    """Assemble the final prompt string from system, context, and user sections.

    Sections, in order: System, Retrieved public apiculture notes, User field
    question, Required answer format. Only language "en" is supported for now;
    any other value raises ValueError.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language {language!r}. "
            f"Only {sorted(SUPPORTED_LANGUAGES)} are supported for now; "
            "Yoruba is not added yet."
        )

    notes = (context or "").strip()
    if not notes:
        notes = (
            "(No relevant public apiculture notes were retrieved for this "
            "question. Rely on cautious field practice and say what to "
            "inspect next.)"
        )

    sections = [
        "# System",
        build_system_instructions(),
        "# Retrieved public apiculture notes",
        notes,
        "# User field question",
        build_user_task(question),
        "# Required answer format",
        REQUIRED_ANSWER_FORMAT,
    ]
    return "\n\n".join(sections)


def build_prompt_with_retrieval(
    question: str,
    db_path: str = DEFAULT_DB_PATH,
    limit: int = 5,
    max_context_chars: int = 3000,
) -> dict:
    """Build a prompt for a question, retrieving public apiculture notes first.

    Ensures the knowledge DB exists, searches it, formats the context, and
    returns a dict with the prompt, the retrieval results, and the context.
    """
    # Ensure the DB exists, building it from notes if needed.
    build_or_open_db(db_path)
    results = search_knowledge(question, db_path=db_path, limit=limit)
    context = format_retrieval_context(results, max_chars=max_context_chars)
    prompt = build_hyvegrid_prompt(question, context, language="en")
    return {"prompt": prompt, "results": results, "context": context}
