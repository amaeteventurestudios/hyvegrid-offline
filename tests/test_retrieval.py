#!/usr/bin/env python3
"""Tests for the local SQLite FTS5 retrieval layer.

Standard library only. Tests build a private copy of the knowledge database in a
temporary directory so the real data/knowledge/knowledge.db is never touched.
"""

import shutil
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

# Make the repo root importable when run as a plain script or via unittest.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app import retrieval  # noqa: E402
from app.retrieval import (  # noqa: E402
    build_database,
    build_or_open_db,
    format_retrieval_context,
    search_knowledge,
)

KNOWLEDGE_DIR = _REPO_ROOT / "data" / "knowledge"

REQUIRED_KEYS = {"source_file", "title", "heading", "body", "score"}


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="hyvegrid_retrieval_")
        cls.db_path = Path(cls.tmp) / "knowledge.db"
        # Seed a private DB from the public knowledge notes.
        build_database(KNOWLEDGE_DIR, cls.db_path)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    # --- DB build -----------------------------------------------------------

    def test_db_builds_from_knowledge(self):
        # The private DB exists and holds both required tables.
        self.assertTrue(self.db_path.exists())
        con = sqlite3.connect(self.db_path)
        try:
            tables = {
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        finally:
            con.close()
        self.assertIn("knowledge_chunks", tables)
        self.assertIn("knowledge_chunks_fts", tables)

        con = sqlite3.connect(self.db_path)
        try:
            count = con.execute(
                "SELECT COUNT(*) FROM knowledge_chunks"
            ).fetchone()[0]
            sources = {
                row[0]
                for row in con.execute(
                    "SELECT DISTINCT source_file FROM knowledge_chunks"
                )
            }
        finally:
            con.close()

        self.assertGreater(count, 0)
        # Every public knowledge note is represented in the index.
        expected_sources = {
            p.name for p in KNOWLEDGE_DIR.glob("*.md")
        }
        self.assertTrue(expected_sources)
        self.assertEqual(sources, expected_sources)

    def test_build_is_idempotent(self):
        # Rebuilding over the same path must not duplicate rows.
        first = build_database(KNOWLEDGE_DIR, self.db_path)
        second = build_database(KNOWLEDGE_DIR, self.db_path)
        self.assertEqual(first, second)
        self.assertGreater(first, 0)

    def test_build_or_open_db_opens_existing(self):
        # An existing complete DB must not be rebuilt.
        before = sqlite3.connect(self.db_path).execute(
            "SELECT COUNT(*) FROM knowledge_chunks"
        ).fetchone()[0]
        build_or_open_db(str(self.db_path))
        after = sqlite3.connect(self.db_path).execute(
            "SELECT COUNT(*) FROM knowledge_chunks"
        ).fetchone()[0]
        self.assertEqual(before, after)

    # --- FTS search ---------------------------------------------------------

    def _top_source(self, query, limit=5):
        results = search_knowledge(query, db_path=str(self.db_path), limit=limit)
        self.assertTrue(results, f"No results for query: {query!r}")
        for r in results:
            self.assertEqual(set(r.keys()), REQUIRED_KEYS)
        return results[0]["source_file"]

    def test_search_ants_low_activity_brood_returns_hive_health(self):
        self.assertEqual(
            self._top_source("ants low activity brood"), "hive_health.md"
        )

    def test_search_hives_cassava_mango_returns_site_or_forage(self):
        top = self._top_source(
            "20 hives cassava mango pepper vegetable water pesticide"
        )
        self.assertIn(top, {"site_readiness.md", "forage_pollination.md"})

    def test_search_uncapped_nectar_returns_harvest_quality(self):
        self.assertEqual(
            self._top_source("uncapped nectar brood frames moisture fermentation"),
            "harvest_quality.md",
        )

    def test_search_results_ranked_by_score(self):
        results = search_knowledge(
            "brood queen eggs", db_path=str(self.db_path), limit=5
        )
        scores = [r["score"] for r in results]
        self.assertEqual(scores, sorted(scores, reverse=True))

    # --- Generic-source ranking (README/glossary) --------------------------

    HIVE_HEALTH_PROMPT = (
        "A beekeeper reports low hive activity, ants near the hive stand, "
        "normal smell, and partially capped brood. What should they check "
        "first, and what should they avoid doing immediately?"
    )

    SITE_READINESS_PROMPT = (
        "An extension worker wants to place 20 hives near cassava, mango, "
        "pepper, and vegetable farms with a seasonal water source nearby. "
        "What site risks and forage factors should they evaluate before "
        "placing the hives?"
    )

    def test_readme_not_top_for_hive_health_prompt(self):
        results = search_knowledge(
            self.HIVE_HEALTH_PROMPT, db_path=str(self.db_path), limit=5
        )
        sources = [r["source_file"] for r in results]
        self.assertTrue(sources)
        self.assertNotEqual(sources[0], "README.md")
        # README excluded entirely for this field question.
        self.assertNotIn("README.md", sources)
        # The relevant field note ranks first.
        self.assertEqual(sources[0], "hive_health.md")

    def test_glossary_does_not_outrank_field_notes(self):
        for query in (self.HIVE_HEALTH_PROMPT, self.SITE_READINESS_PROMPT):
            results = search_knowledge(query, db_path=str(self.db_path), limit=5)
            sources = [r["source_file"] for r in results]
            self.assertNotIn("glossary.md", sources, f"glossary leaked: {query[:40]!r}")
            self.assertNotIn("README.md", sources, f"README leaked: {query[:40]!r}")
            self.assertTrue(
                sources[0].endswith("_health.md")
                or sources[0] in ("site_readiness.md", "forage_pollination.md"),
                f"unexpected top source {sources[0]!r}",
            )

    def test_glossary_intent_returns_generic_sources(self):
        query = (
            "What is the definition of an apiary and the glossary term brood?"
        )
        results = search_knowledge(query, db_path=str(self.db_path), limit=5)
        sources = {r["source_file"] for r in results}
        self.assertIn("glossary.md", sources)

    def test_include_generic_override(self):
        default = search_knowledge(
            self.HIVE_HEALTH_PROMPT, db_path=str(self.db_path), limit=10
        )
        self.assertNotIn("README.md", {r["source_file"] for r in default})
        forced = search_knowledge(
            self.HIVE_HEALTH_PROMPT,
            db_path=str(self.db_path),
            limit=10,
            include_generic=True,
        )
        self.assertIn("README.md", {r["source_file"] for r in forced})

    # --- Fallback -----------------------------------------------------------

    def test_fts5_query_sanitizer_ors_terms(self):
        self.assertEqual(
            retrieval._to_fts_query("ants, low activity!"),
            "ants OR low OR activity",
        )
        self.assertEqual(retrieval._to_fts_query("   "), "")

    def test_like_fallback_when_fts_query_fails(self):
        # Simulate FTS5 being unavailable at query time: force the LIKE fallback
        # path without disturbing build_or_open_db's table detection.
        original = retrieval._fts_search

        def boom(con, query, limit, exclude=None):
            raise sqlite3.OperationalError("simulated FTS5 query failure")

        retrieval._fts_search = boom
        try:
            results = search_knowledge(
                "ants brood", db_path=str(self.db_path), limit=5
            )
        finally:
            retrieval._fts_search = original
        self.assertTrue(results)
        self.assertEqual(set(results[0].keys()), REQUIRED_KEYS)

    # --- Context formatting -------------------------------------------------

    def test_format_context_has_labels_and_stays_under_limit(self):
        results = search_knowledge(
            "ants low activity brood", db_path=str(self.db_path), limit=3
        )
        out = format_retrieval_context(results, max_chars=300)
        self.assertLessEqual(len(out), 300)
        self.assertIn("hive_health.md", out)
        self.assertIn(">", out)  # "source > heading" label separator

    def test_format_context_empty(self):
        self.assertEqual(format_retrieval_context([], max_chars=300), "")

    def test_format_context_truncates_long_input(self):
        big = [
            {
                "source_file": "note.md",
                "heading": "Heading",
                "body": "x" * 500,
            }
        ]
        out = format_retrieval_context(big, max_chars=80)
        self.assertLessEqual(len(out), 80)


if __name__ == "__main__":
    unittest.main()
