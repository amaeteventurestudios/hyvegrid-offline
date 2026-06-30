#!/usr/bin/env python3
"""Tests for the HyveGrid prompt builder.

Standard library only. Retrieval-based tests build a private knowledge database
in a temporary directory so the real data/knowledge/knowledge.db is untouched.
"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Make the repo root importable when run as a plain script or via unittest.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app.retrieval import build_database  # noqa: E402
from app.prompt_builder import (  # noqa: E402
    UNSUPPORTED_ASSUMPTION_GUARD,
    build_hyvegrid_prompt,
    build_prompt_with_retrieval,
    build_system_instructions,
    build_user_task,
)

KNOWLEDGE_DIR = _REPO_ROOT / "data" / "knowledge"

FIELD_QUESTION = (
    "A beekeeper reports low hive activity, ants near the hive stand, normal "
    "smell, and partially capped brood. What should they check first, and what "
    "should they avoid doing immediately?"
)

REQUIRED_SECTIONS = [
    "# System",
    "# Retrieved public apiculture notes",
    "# User field question",
    "# Required answer format",
]

REQUIRED_FORMAT_ITEMS = [
    "1. Possible concern",
    "2. Check first",
    "3. Avoid doing immediately",
    "4. Suggested next step",
    "5. When to escalate",
]


class PromptBuilderUnitTests(unittest.TestCase):
    """Pure prompt-building tests (no retrieval, no DB)."""

    def setUp(self):
        self.prompt = build_hyvegrid_prompt(
            FIELD_QUESTION, context="Sample retrieved note body.", language="en"
        )

    def test_includes_all_required_sections(self):
        for section in REQUIRED_SECTIONS:
            self.assertIn(section, self.prompt, f"Missing section: {section}")

    def test_includes_required_answer_format_items(self):
        for item in REQUIRED_FORMAT_ITEMS:
            self.assertIn(item, self.prompt, f"Missing format item: {item}")

    def test_english_language_works(self):
        # No exception, returns a non-empty string.
        self.assertIsInstance(self.prompt, str)
        self.assertGreater(len(self.prompt), 0)

    def test_non_english_language_raises_value_error(self):
        # Yoruba is intentionally not supported yet.
        with self.assertRaises(ValueError):
            build_hyvegrid_prompt("q", context="c", language="yo")
        with self.assertRaises(ValueError):
            build_hyvegrid_prompt("q", context="c", language="fr")

    def test_prompt_includes_caution_language(self):
        lowered = self.prompt.lower()
        for phrase in [
            "possible concern",
            "check first",
            "avoid doing immediately",
            "confirm by physical inspection",
            "consulting an experienced beekeeper or extension officer",
        ]:
            self.assertIn(phrase, lowered, f"Missing caution language: {phrase}")

    def test_prompt_makes_no_certified_diagnosis_claim(self):
        lowered = self.prompt.lower()
        # The prompt must instruct the model NOT to claim certified diagnosis.
        self.assertIn("do not claim certified diagnosis", lowered)
        self.assertIn("not a certified disease diagnosis tool", lowered)

    def test_user_question_appears_in_prompt(self):
        self.assertIn(FIELD_QUESTION, self.prompt)

    def test_empty_context_uses_placeholder(self):
        prompt = build_hyvegrid_prompt("q", context="", language="en")
        self.assertIn("No relevant public apiculture notes", prompt)

    def test_build_user_task_contains_question(self):
        task = build_user_task("Why are my bees clustering outside?")
        self.assertIn("Why are my bees clustering outside?", task)
        self.assertIn("Question", task)

    def test_system_instructions_mention_offline_role(self):
        instructions = build_system_instructions()
        self.assertIn("HyveGrid Offline", instructions)
        self.assertIn("offline apiculture field assistant", instructions)

    def test_prompt_contains_unsupported_assumption_guard(self):
        lowered = self.prompt.lower()
        normalized = " ".join(lowered.split())
        for phrase in [
            "unsupported-assumption guard",
            "use only reported observations and retrieved local notes",
            "distinguish reported observation, possible concern, check first",
            "do not state that eggs, larvae, queen, stores, mites, disease",
        ]:
            self.assertIn(phrase, lowered)
        self.assertIn(
            "unless the user reported it or the retrieved source explicitly supports it",
            normalized,
        )

    def test_hive_health_prompt_says_check_eggs_and_larvae_not_assume_absent(self):
        self.assertIn(
            "Check whether eggs and young larvae are present.",
            self.prompt,
        )
        self.assertIn(
            "Confirm by physical inspection whether eggs and young larvae are present",
            self.prompt,
        )
        self.assertIn('"no eggs"', self.prompt)
        self.assertIn('"no young brood"', self.prompt)
        self.assertIn("unless explicitly reported", self.prompt)

    def test_assumption_guard_constant_is_in_system_instructions(self):
        self.assertIn(UNSUPPORTED_ASSUMPTION_GUARD, build_system_instructions())


class PromptBuilderRetrievalTests(unittest.TestCase):
    """Tests that combine the prompt builder with the retrieval layer."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="hyvegrid_prompt_")
        cls.db_path = Path(cls.tmp) / "knowledge.db"
        build_database(KNOWLEDGE_DIR, cls.db_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_build_prompt_with_retrieval_returns_bundle(self):
        bundle = build_prompt_with_retrieval(
            FIELD_QUESTION, db_path=str(self.db_path), limit=5
        )
        # Returns a dict with the three expected keys.
        self.assertEqual(set(bundle.keys()), {"prompt", "results", "context"})

        # Prompt is a non-empty string containing all required sections.
        self.assertIsInstance(bundle["prompt"], str)
        for section in REQUIRED_SECTIONS:
            self.assertIn(section, bundle["prompt"])

        # Results and context are non-empty for this question.
        self.assertTrue(bundle["results"])
        self.assertTrue(bundle["context"])

    def test_retrieval_results_include_hive_health(self):
        bundle = build_prompt_with_retrieval(
            FIELD_QUESTION, db_path=str(self.db_path), limit=5
        )
        sources = {r["source_file"] for r in bundle["results"]}
        self.assertIn("hive_health.md", sources)

    def test_prompt_length_reasonable_with_default_context(self):
        # Default max_context_chars=3000 should keep the prompt well bounded.
        bundle = build_prompt_with_retrieval(
            FIELD_QUESTION, db_path=str(self.db_path)  # defaults: limit=5, 3000
        )
        self.assertLess(len(bundle["prompt"]), 7000)

    def test_respects_max_context_chars(self):
        bundle = build_prompt_with_retrieval(
            FIELD_QUESTION, db_path=str(self.db_path), limit=5, max_context_chars=500
        )
        self.assertLessEqual(len(bundle["context"]), 500)
        self.assertLess(len(bundle["prompt"]), 7000)


if __name__ == "__main__":
    unittest.main()
