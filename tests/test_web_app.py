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

    def test_mission_control_visual_sections_and_assets(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "mission-control-page",
            "/static/assets/hero-honeycomb-bg.webp",
            "/static/assets/logo-honeycomb-mark.webp",
            "/static/assets/hero-bee.webp",
            "/static/assets/card-hive-health.webp",
            "/static/assets/card-site-readiness.webp",
            "/static/assets/card-harvest-quality.webp",
            "/static/assets/card-forage-pollination.webp",
            "/static/assets/card-hive-signal.webp",
            "/static/assets/card-offline-status.webp",
            "Guidance at Your Fingertips",
            "At a Glance",
            "HyveGrid Offline provides field triage",
            "Model: Granite 3.3 2B",
            "System Ready",
        ]:
            self.assertIn(needle, resp.text)

    def test_mission_control_guidance_assets(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "/static/assets/guide-yoruba-template.webp",
            "/static/assets/guide-ask-advisor.webp",
            "/static/assets/guide-daily-checklist.webp",
            "/static/assets/guide-storage-handling.webp",
            "/static/assets/guide-pesticide-awareness.webp",
            "/static/assets/guide-forage-calendar.webp",
            "Yoruba Template",
            "Ask the Hive Advisor",
            "Daily Hive Checklist",
            "Storage &amp; Handling",
            "Pesticide Awareness",
            "Forage Calendar",
        ]:
            self.assertIn(needle, resp.text)

    def test_language_dropdown_defaults_to_english_on_mission_control(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<label class="language-select" for="language-select">', resp.text)
        self.assertIn('<select id="language-select"', resp.text)
        self.assertIn('<option value="/" selected>English</option>', resp.text)
        self.assertIn('<option value="/?lang=yo" >Yorùbá</option>', resp.text)

    def test_mission_control_yoruba_mode_labels_and_glossary(self):
        resp = self.client.get("/?lang=yo")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "Ibi Ìṣàkóso",
            "Olùrànlọ́wọ́ Ìlera Ilé Oyin",
            "Ipò Ẹ̀rọ Àìsí Ayélujára",
            "Àkójọ ọ̀rọ̀ pápá Yorùbá",
            "Ọ̀rọ̀ ilé oyin àti agbo oyin",
            "ilé oyin",
            "Yoruba field labels and templates are controlled draft support",
            "/advisor/hive-health?lang=yo",
        ]:
            self.assertIn(needle, resp.text)
        self.assertIn('<option value="/" >Gẹ̀ẹ́sì</option>', resp.text)
        self.assertIn('<option value="/?lang=yo" selected>Yorùbá</option>', resp.text)
        self.assertIn("mission-control-page", resp.text)

    def test_language_dropdown_uses_same_page_urls(self):
        resp = self.client.get("/advisor/hive-health?lang=yo")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            '<option value="/advisor/hive-health" >Gẹ̀ẹ́sì</option>',
            resp.text,
        )
        self.assertIn(
            '<option value="/advisor/hive-health?lang=yo" selected>Yorùbá</option>',
            resp.text,
        )

        resp = self.client.get("/status")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<option value="/status" selected>English</option>', resp.text)
        self.assertIn('<option value="/status?lang=yo" >Yorùbá</option>', resp.text)

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

    def test_status_yoruba_mode_keeps_runtime_markers(self):
        resp = self.client.get("/status?lang=yo")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "Ipò Ẹ̀rọ Àìsí Ayélujára",
            "Ìpo àìsí ayélujára",
            "Módẹ́lì ti wà fún lílò",
            "Kò sí ìráyè sí cloud",
            "llama.cpp",
            "GGUF",
            "SQLite FTS5",
        ]:
            self.assertIn(needle, resp.text)

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
        self.assertIn('body class="advisor-page advisor-hive-health"', resp.text)
        self.assertIn("/static/assets/card-hive-health.webp", resp.text)
        self.assertIn("/static/assets/logo-honeycomb-mark.webp", resp.text)
        self.assertIn("Granite 3.3 2B", resp.text)
        self.assertIn("llama.cpp", resp.text)
        self.assertIn("<form", resp.text)
        self.assertIn('method="post"', resp.text)
        self.assertIn('data-local-advisor-form', resp.text)
        self.assertIn('name="question"', resp.text)
        self.assertIn('type="submit"', resp.text)
        self.assertIn("Working locally...", resp.text)
        self.assertIn("Running the local Granite model through llama.cpp", resp.text)
        self.assertIn("data-local-runtime-loading", resp.text)
        self.assertIn("data-submit-label", resp.text)
        # Example prompt is shown but not auto-run.
        self.assertIn("Example prompt", resp.text)
        self.assertIn("low hive activity", resp.text)
        # No answer section on a plain GET.
        self.assertNotIn("Completed locally", resp.text)

    def test_advisor_pages_include_walkthrough_container_and_script(self):
        for slug in [
            "hive-health",
            "site-readiness",
            "harvest-quality",
            "forage-pollination",
            "hive-signal",
        ]:
            resp = self.client.get(f"/advisor/{slug}")
            self.assertEqual(resp.status_code, 200, slug)
            for needle in [
                "data-hive-walkthrough",
                "Hive State Walkthrough",
                "Local walkthrough while Granite thinks",
                "Guided field walkthrough",
                "Visual inspection support while the local model prepares guidance",
                "Manual observations or sample edge-signal inputs",
                "beekeeper-avatar",
                "bee-dot",
                "ant-dot",
                "data-walkthrough-step",
                "data-walkthrough-step-item",
                "window.setInterval",
                "Working locally...",
                "data-local-runtime-loading",
                "data-submit-label",
            ]:
                self.assertIn(needle, resp.text, f"{slug} missing {needle!r}")

    def test_hive_health_walkthrough_steps_render(self):
        resp = self.client.get("/advisor/hive-health")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "Walking to hive",
            "Checking entrance activity",
            "Looking for ant trails near the stand",
            "Inspecting brood pattern",
            "Confirming normal smell report",
            "Checking food stores",
            "Preparing local guidance",
        ]:
            self.assertIn(needle, resp.text)

    def test_site_readiness_walkthrough_steps_render(self):
        resp = self.client.get("/advisor/site-readiness")
        self.assertEqual(resp.status_code, 200)
        for needle in [
            "Reviewing proposed apiary area",
            "Checking crop zones",
            "Checking water reliability",
            "Checking shade and wind exposure",
            "Looking for pesticide risk",
            "Checking human and livestock safety",
            "Preparing placement guidance",
        ]:
            self.assertIn(needle, resp.text)

    def test_advisor_language_dropdown_and_yoruba_route_still_render(self):
        resp = self.client.get("/advisor/hive-health")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<label class="language-select" for="language-select">', resp.text)
        self.assertIn('<select id="language-select"', resp.text)

        resp = self.client.get("/advisor/hive-health?lang=yo")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Olùrànlọ́wọ́ Ìlera Ilé Oyin", resp.text)
        self.assertIn("Hive State Walkthrough", resp.text)
        self.assertIn("Walking to hive", resp.text)
        self.assertIn('<option value="/advisor/hive-health?lang=yo" selected>Yorùbá</option>', resp.text)

    def test_hive_health_post_valid_calls_answer_and_displays(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_bundle()) as m:
            resp = self.client.post(
                "/advisor/hive-health", data={"question": self.HIVE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_called_once_with(self.HIVE_QUESTION)
        self.assertIn("example field answer", resp.text)
        self.assertIn("Completed locally", resp.text)

    def test_hive_health_yoruba_mode_uses_controlled_template(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_bundle()) as m:
            resp = self.client.post(
                "/advisor/hive-health?lang=yo", data={"question": self.HIVE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_called_once_with(self.HIVE_QUESTION)
        for needle in [
            "Àwọn template ìtọ́nisọ́nà Yorùbá",
            "Àkótán ohun tí a rí ní pápá",
            "Ohun tó lè jẹ́ ìṣòro",
            "Ṣàyẹ̀wò èyí kọ́kọ́",
            "Má ṣe èyí lẹ́sẹ̀kẹsẹ̀",
            "Ìdáhùn módẹ́lì ní Gẹ̀ẹ́sì",
            "example field answer",
            "Yoruba field labels and templates are controlled draft support",
        ]:
            self.assertIn(needle, resp.text)
        self.assertIn('body class="advisor-page advisor-hive-health"', resp.text)
        self.assertIn("/static/assets/card-hive-health.webp", resp.text)
        self.assertIn('<option value="/advisor/hive-health?lang=yo" selected>Yorùbá</option>', resp.text)

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
        self.assertIn("local model runtime failed", resp.text)
        self.assertIn("Check the server log", resp.text)
        # No stack trace or internal detail leaks to the user.
        self.assertNotIn("secret internal detail boom", resp.text)
        self.assertNotIn("Traceback", resp.text)

    def test_all_advisors_are_wired(self):
        # All five advisors now render a real form; none remain placeholders.
        expected_assets = {
            "hive-health": "/static/assets/card-hive-health.webp",
            "site-readiness": "/static/assets/card-site-readiness.webp",
            "harvest-quality": "/static/assets/card-harvest-quality.webp",
            "forage-pollination": "/static/assets/card-forage-pollination.webp",
            "hive-signal": "/static/assets/card-hive-signal.webp",
        }
        for slug, asset in expected_assets.items():
            resp = self.client.get(f"/advisor/{slug}")
            self.assertEqual(resp.status_code, 200, slug)
            self.assertIn(f'body class="advisor-page advisor-{slug}"', resp.text)
            self.assertIn(asset, resp.text)
            self.assertIn("/static/assets/logo-honeycomb-mark.webp", resp.text)
            self.assertIn("<form", resp.text)
            self.assertIn('method="post"', resp.text)
            self.assertIn('data-local-advisor-form', resp.text)
            self.assertIn('name="question"', resp.text)
            self.assertIn("Running the local Granite model through llama.cpp", resp.text)

    # --- Harvest Quality / Forage & Pollination / Hive Signal (wired) -------

    HARVEST_QUESTION = (
        "A beekeeper is preparing to harvest honey after a rainy week. Some "
        "frames are mostly capped. What quality risks should they check?"
    )
    FORAGE_QUESTION = (
        "A beekeeper wants to support mango, pepper, and vegetable farms, but "
        "there may be a flowering gap after mango season. What factors?"
    )
    HIVE_SIGNAL_QUESTION = (
        "A hive shows rising temperature, dropping humidity, low entrance "
        "activity, and bees clustering outside. What should they check first?"
    )

    def _assert_wired_advisor(self, slug, question, source_file, marker):
        bundle = {
            "question": question,
            "prompt": "PROMPT",
            "context": "CTX",
            "results": [
                {"source_file": source_file, "heading": "Key checks"},
                {"source_file": "site_readiness.md", "heading": "Check first"},
            ],
            "answer": f"1. Possible concern: {marker}.\n2. Check first: inspect.",
            "runtime": {"returncode": 0, "timed_out": False, "answer": "x"},
        }
        # GET renders the form; no answer yet.
        resp = self.client.get(f"/advisor/{slug}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("<form", resp.text)
        self.assertIn('name="question"', resp.text)
        self.assertIn("Example prompt", resp.text)
        self.assertNotIn("Completed locally", resp.text)
        # POST valid: calls answer_question and renders answer + sources.
        with mock.patch("app.web_app.answer_question", return_value=bundle) as m:
            resp = self.client.post(f"/advisor/{slug}", data={"question": question})
        self.assertEqual(resp.status_code, 200)
        m.assert_called_once_with(question)
        self.assertIn(marker, resp.text)
        self.assertIn("Completed locally", resp.text)
        self.assertIn(source_file, resp.text)
        # Empty input: validation, no model call.
        with mock.patch("app.web_app.answer_question") as m:
            resp = self.client.post(f"/advisor/{slug}", data={"question": ""})
        self.assertEqual(resp.status_code, 200)
        m.assert_not_called()
        self.assertNotIn("Completed locally", resp.text)
        # Exception: safe error, no stack trace or raw exception text.
        with mock.patch(
            "app.web_app.answer_question",
            side_effect=RuntimeError("secret internal detail boom"),
        ):
            resp = self.client.post(f"/advisor/{slug}", data={"question": question})
        self.assertEqual(resp.status_code, 200)
        self.assertIn("HyveGrid could not complete this local", resp.text)
        self.assertNotIn("secret internal detail boom", resp.text)
        self.assertNotIn("Traceback", resp.text)

    def test_harvest_quality_advisor_wired(self):
        self._assert_wired_advisor(
            "harvest-quality", self.HARVEST_QUESTION,
            "harvest_quality.md", "example harvest answer",
        )

    def test_forage_pollination_advisor_wired(self):
        self._assert_wired_advisor(
            "forage-pollination", self.FORAGE_QUESTION,
            "forage_pollination.md", "example forage answer",
        )

    def test_hive_signal_advisor_wired(self):
        self._assert_wired_advisor(
            "hive-signal", self.HIVE_SIGNAL_QUESTION,
            "hive_signals.md", "example signal answer",
        )

    # --- Site Readiness Advisor (wired to the offline answer path) ----------

    SITE_QUESTION = (
        "An extension worker wants to place 20 hives near cassava, mango, "
        "pepper, and vegetable farms with a seasonal water source nearby. What "
        "site risks should they evaluate before placing the hives?"
    )

    def _fake_site_bundle(self):
        return {
            "question": self.SITE_QUESTION,
            "prompt": "PROMPT",
            "context": "CTX",
            "results": [
                {"source_file": "site_readiness.md", "heading": "Check first"},
                {"source_file": "forage_pollination.md", "heading": "Key checks"},
            ],
            "answer": (
                "1. Possible concern: example site answer.\n"
                "2. Check first: walk the site in wet and dry conditions."
            ),
            "runtime": {"returncode": 0, "timed_out": False, "answer": "x"},
        }

    def test_site_readiness_get_returns_form(self):
        resp = self.client.get("/advisor/site-readiness")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Site Readiness Advisor", resp.text)
        self.assertIn("<form", resp.text)
        self.assertIn('name="question"', resp.text)
        # Example prompt shown, not auto-run.
        self.assertIn("Example prompt", resp.text)
        self.assertIn("20 hives near cassava", resp.text)
        # Site-specific field-tool note, not a certified approval tool.
        self.assertIn("not a certified site approval tool", resp.text)
        self.assertNotIn("Completed locally", resp.text)

    def test_site_readiness_post_valid_calls_answer_and_displays(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_site_bundle()) as m:
            resp = self.client.post(
                "/advisor/site-readiness", data={"question": self.SITE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_called_once_with(self.SITE_QUESTION)
        self.assertIn("example site answer", resp.text)
        self.assertIn("Completed locally", resp.text)

    def test_site_readiness_post_displays_sources(self):
        with mock.patch("app.web_app.answer_question", return_value=self._fake_site_bundle()):
            resp = self.client.post(
                "/advisor/site-readiness", data={"question": self.SITE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("site_readiness.md", resp.text)
        self.assertIn("Check first", resp.text)
        self.assertIn("forage_pollination.md", resp.text)

    def test_site_readiness_post_empty_shows_validation_no_call(self):
        with mock.patch("app.web_app.answer_question") as m:
            resp = self.client.post(
                "/advisor/site-readiness", data={"question": ""}
            )
        self.assertEqual(resp.status_code, 200)
        m.assert_not_called()
        self.assertIn("Please enter a site-readiness question", resp.text)
        self.assertNotIn("Completed locally", resp.text)

    def test_site_readiness_post_exception_shows_safe_error(self):
        boom = RuntimeError("secret internal detail boom")
        with mock.patch("app.web_app.answer_question", side_effect=boom):
            resp = self.client.post(
                "/advisor/site-readiness", data={"question": self.SITE_QUESTION}
            )
        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            "HyveGrid could not complete this local answer", resp.text
        )
        self.assertIn("local model runtime failed", resp.text)
        self.assertNotIn("secret internal detail boom", resp.text)
        self.assertNotIn("Traceback", resp.text)


if __name__ == "__main__":
    unittest.main()
