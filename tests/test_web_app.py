#!/usr/bin/env python3
"""Tests for the HyveGrid Offline local web UI skeleton.

Uses FastAPI's TestClient (httpx). No GGUF model is loaded: importing app.web_app
does not import the runtime, and the tests never call llama.cpp.
"""

import sys
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
