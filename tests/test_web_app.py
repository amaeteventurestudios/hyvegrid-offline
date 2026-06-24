#!/usr/bin/env python3
"""Tests for the HyveGrid Offline local web UI skeleton.

Uses FastAPI's TestClient (httpx). No GGUF model is loaded: importing app.web_app
does not import the runtime, and the tests never call llama.cpp.
"""

import sys
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from app.web_app import app  # noqa: E402


class WebAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_mission_control_returns_200(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_mission_control_has_title(self):
        resp = self.client.get("/")
        self.assertIn("HyveGrid Offline", resp.text)
        self.assertIn("Mission Control", resp.text)

    def test_mission_control_lists_modules(self):
        resp = self.client.get("/")
        for name in [
            "Hive Health Advisor",
            "Site Readiness Advisor",
            "Harvest Quality Coach",
            "Forage and Pollination Guide",
            "Hive Signal Check",
            "Offline System Status",
        ]:
            self.assertIn(name, resp.text, f"Missing module card: {name}")

    def test_status_returns_200(self):
        resp = self.client.get("/status")
        self.assertEqual(resp.status_code, 200)

    def test_status_has_required_info(self):
        resp = self.client.get("/status")
        for needle in [
            "llama.cpp",
            "GGUF",
            "Granite 3.3 2B Instruct Q4_K_M",
            "model.gguf",
            "SQLite FTS5",
            "No local hidden-validation accuracy score is claimed.",
        ]:
            self.assertIn(needle, resp.text, f"Status page missing: {needle!r}")

    def test_status_has_benchmark_evidence(self):
        resp = self.client.get("/status")
        self.assertIn("6.12", resp.text)  # Task 016 gen t/s
        self.assertIn("4.38", resp.text)  # Task 017 gen t/s
        self.assertIn("~2.67 GB", resp.text)

    def test_advisor_placeholder_known_slug(self):
        resp = self.client.get("/advisor/hive-health")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Hive Health Advisor", resp.text)

    def test_advisor_placeholder_unknown_slug_404(self):
        resp = self.client.get("/advisor/does-not-exist")
        self.assertEqual(resp.status_code, 404)

    def test_health_endpoint(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")

    # --- Hive Health Advisor (wired to the offline answer path) -------------

    HIVE_QUESTION = (
        "A beekeeper reports low hive activity, ants near the hive stand, "
        "normal smell, and partially capped brood. What should they check first?"
    )

    def _fake_bundle(self):
        return {
            "question": self.HIVE_QUESTION,
            "prompt": "PROMPT",
            "context": "CTX",
            "results": [
                {"source_file": "hive_health.md", "heading": "Avoid doing immediately"},
                {"source_file": "site_readiness.md", "heading": "Check first"},
            ],
            "answer": (
                "1. Possible concern: example field answer.\n"
                "2. Check first: inspect the hive."
            ),
            "runtime": {"returncode": 0, "timed_out": False, "answer": "x"},
        }

    def test_hive_health_get_returns_form(self):
        resp = self.client.get("/advisor/hive-health")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Hive Health Advisor", resp.text)
        self.assertIn("<form", resp.text)
        self.assertIn('name="question"', resp.text)
        # Example prompt is shown but not auto-run.
        self.assertIn("Example prompt", resp.text)
        self.assertIn("low hive activity", resp.text)
        # No answer section on a plain GET.
        self.assertNotIn("Completed locally", resp.text)

    def test_hive_health_post_valid_calls_answer_and_displays(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_bundle()) as m:
            resp = self.client.post(
                "/advisor/hive-health", data={"question": self.HIVE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_called_once_with(self.HIVE_QUESTION)
        self.assertIn("example field answer", resp.text)
        self.assertIn("Completed locally", resp.text)

    def test_hive_health_post_displays_sources(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_bundle()):
            resp = self.client.post(
                "/advisor/hive-health", data={"question": self.HIVE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("hive_health.md", resp.text)
        self.assertIn("Avoid doing immediately", resp.text)
        self.assertIn("site_readiness.md", resp.text)

    def test_hive_health_post_empty_shows_validation_no_call(self):
        with mock.patch("app.web_app.answer_question") as m:
            resp = self.client.post(
                "/advisor/hive-health", data={"question": ""}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_not_called()
        self.assertIn("Please enter a hive-health question", resp.text)
        self.assertNotIn("Completed locally", resp.text)

    def test_hive_health_post_exception_shows_safe_error(self):
        boom = RuntimeError("secret internal detail boom")
        with mock.patch("app.web_app.answer_question", side_effect=boom):
            resp = self.client.post(
                "/advisor/hive-health", data={"question": self.HIVE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("HyveGrid could not complete this local answer", resp.text)
        # No stack trace or internal detail leaks to the user.
        self.assertNotIn("secret internal detail boom", resp.text)
        self.assertNotIn("Traceback", resp.text)

    def test_other_advisors_remain_placeholders(self):
        resp = self.client.get("/advisor/site-readiness")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Site Readiness Advisor", resp.text)
        self.assertIn("not enabled in this English skeleton", resp.text)


if __name__ == "__main__":
    unittest.main()
