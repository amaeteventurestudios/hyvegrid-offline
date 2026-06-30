#!/usr/bin/env python3
"""Tests for the local llama.cpp runtime wrapper.

Standard library only. Uses unittest.mock so the real GGUF model and llama-cli
binary are never required.
"""

import re
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app import llama_runtime as rt  # noqa: E402

# A regex that would match any stdlib/third-party networking import.
NETWORK_IMPORT_RE = re.compile(
    r"^\s*(?:import|from)\s+("
    r"requests|urllib|http|socket|ftplib|smtplib|telnetlib|xmlrpc|"
    r"boto|boto3|openai|anthropic|google\.generativeai|gemini|cohere|"
    r"websocket|aiohttp|httpx"
    r")",
    re.MULTILINE,
)

REQUIRED_FLAGS = ["-m", "-p", "-n", "-t", "--temp", "--single-turn"]


class BuildCommandTests(unittest.TestCase):
    """Directly verify the constructed llama-cli argv (no subprocess needed)."""

    def test_command_contains_required_flags_and_values(self):
        cmd = rt._build_command(
            llama_bin="/bin/llama-cli",
            model_path="model/x.gguf",
            prompt="hello bees",
            max_tokens=128,
            temperature=0.3,
            threads=2,
        )
        self.assertEqual(cmd[0], "/bin/llama-cli")
        for flag in REQUIRED_FLAGS:
            self.assertIn(flag, cmd)
        # Values are positioned right after their flags.
        self.assertEqual(cmd[cmd.index("-m") + 1], "model/x.gguf")
        self.assertEqual(cmd[cmd.index("-p") + 1], "hello bees")
        self.assertEqual(cmd[cmd.index("-n") + 1], "128")
        self.assertEqual(cmd[cmd.index("-t") + 1], "2")
        self.assertEqual(cmd[cmd.index("--temp") + 1], "0.3")


class RunLlamaPromptTests(unittest.TestCase):
    """Mock subprocess + filesystem so no real model/binary is needed."""

    def _fake_proc(self, stdout="answer", returncode=0, stderr=""):
        return subprocess.CompletedProcess(
            args=[], returncode=returncode, stdout=stdout, stderr=stderr
        )

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", return_value=True)
    @mock.patch("app.llama_runtime.os.access", return_value=True)
    def test_builds_expected_subprocess_command(self, _access, _isfile, run_mock):
        run_mock.return_value = self._fake_proc(stdout="possible concern")
        result = rt.run_llama_prompt(
            "PROMPT",
            model_path="model/x.gguf",
            llama_bin="/bin/llama-cli",
            max_tokens=64,
            temperature=0.2,
            threads=4,
        )
        run_mock.assert_called_once()
        cmd = run_mock.call_args[0][0]
        for flag in REQUIRED_FLAGS:
            self.assertIn(flag, cmd)
        self.assertTrue(cmd[cmd.index("-m") + 1].endswith("/model/x.gguf"))
        self.assertEqual(cmd[cmd.index("-p") + 1], "PROMPT")
        self.assertEqual(cmd[cmd.index("-n") + 1], "64")
        # Successful run: answer is the stripped stdout.
        self.assertEqual(result["answer"], "possible concern")
        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assertTrue(result["model_path"].endswith("/model/x.gguf"))
        self.assertEqual(result["llama_bin"], "/bin/llama-cli")

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", return_value=False)
    def test_missing_llama_binary_raises(self, _isfile, run_mock):
        with self.assertRaises(RuntimeError) as ctx:
            rt.run_llama_prompt("p", llama_bin="/nope/llama-cli")
        self.assertIn("binary", str(ctx.exception).lower())
        run_mock.assert_not_called()

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", side_effect=lambda p: p == "/bin/llama-cli")
    @mock.patch("app.llama_runtime.os.access", side_effect=lambda p, mode: p == "/bin/llama-cli")
    def test_missing_model_raises(self, _access, _isfile, run_mock):
        with self.assertRaises(RuntimeError) as ctx:
            rt.run_llama_prompt(
                "p", model_path="model/missing.gguf", llama_bin="/bin/llama-cli"
            )
        self.assertIn("model", str(ctx.exception).lower())
        run_mock.assert_not_called()

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", return_value=True)
    @mock.patch("app.llama_runtime.os.access", return_value=True)
    def test_timeout_returns_useful_info(self, _access, _isfile, run_mock):
        run_mock.side_effect = subprocess.TimeoutExpired(
            cmd=[], timeout=1, output="partial", stderr=""
        )
        result = rt.run_llama_prompt("p", timeout_seconds=1)
        self.assertTrue(result["timed_out"])
        self.assertIsNone(result["returncode"])
        self.assertEqual(result["stdout"], "partial")
        self.assertEqual(result["answer"], "partial")

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", return_value=True)
    @mock.patch("app.llama_runtime.os.access", return_value=True)
    def test_nonzero_exit_returns_error_info(self, _access, _isfile, run_mock):
        run_mock.return_value = self._fake_proc(
            stdout="", returncode=1, stderr="model load failed"
        )
        result = rt.run_llama_prompt("p")
        self.assertEqual(result["returncode"], 1)
        self.assertEqual(result["answer"], "")
        self.assertIn("model load failed", result["stderr"])

    @mock.patch("app.llama_runtime.subprocess.run")
    @mock.patch("app.llama_runtime.os.path.isfile", return_value=True)
    @mock.patch("app.llama_runtime.os.access", return_value=True)
    def test_no_network_flags_in_command(self, _access, _isfile, run_mock):
        run_mock.return_value = self._fake_proc()
        rt.run_llama_prompt("p")
        cmd = run_mock.call_args[0][0]
        joined = " ".join(cmd)
        # No cloud/remote endpoints sneaking into the invocation.
        for bad in ("http://", "https://", "amazonaws", "openai.com"):
            self.assertNotIn(bad, joined)


class AnswerQuestionTests(unittest.TestCase):
    """Verify answer_question wires the prompt builder and runtime together."""

    @mock.patch("app.llama_runtime.run_llama_prompt")
    @mock.patch("app.llama_runtime.build_prompt_with_retrieval")
    def test_calls_builder_and_runtime_and_combines(self, build_mock, run_mock):
        build_mock.return_value = {
            "prompt": "PROMPT",
            "results": [{"source_file": "hive_health.md", "heading": "Key checks"}],
            "context": "CTX",
        }
        run_mock.return_value = {
            "answer": "possible concern",
            "stdout": "possible concern",
            "stderr": "",
            "returncode": 0,
            "model_path": "model/x.gguf",
            "llama_bin": "/bin/llama-cli",
            "timed_out": False,
        }

        out = rt.answer_question(
            "What about the bees?",
            model_path="model/x.gguf",
            llama_bin="/bin/llama-cli",
            limit=3,
            max_context_chars=500,
            max_tokens=64,
        )

        build_mock.assert_called_once_with("What about the bees?", limit=3, max_context_chars=500)
        run_mock.assert_called_once_with(
            "PROMPT", model_path="model/x.gguf", llama_bin="/bin/llama-cli", max_tokens=64
        )

        self.assertEqual(out["question"], "What about the bees?")
        self.assertEqual(out["prompt"], "PROMPT")
        self.assertEqual(out["context"], "CTX")
        self.assertEqual(out["results"], build_mock.return_value["results"])
        self.assertEqual(out["answer"], "possible concern")
        self.assertEqual(out["runtime"], run_mock.return_value)


class CleanLlamaOutputTests(unittest.TestCase):
    """Verify the output cleaner strips chrome/echo and keeps only the answer."""

    # A realistic conversation-mode stdout: banner/logo, build/model lines,
    # "available commands" help, an echoed prompt (which itself lists the format
    # headings "1. Possible concern"), then the real answer, then the timing
    # footer and "Exiting...".
    CHROME_STDOUT = (
        "\nLoading model... \n\n"
        "▄▄ ▄▄\n██ ██\n██ ██  ▀▀█▄ ███▄███▄  ▀▀█▄\n\n"
        "build      : b9753-7c082bc41\n"
        "model      : model/granite-3.3-2b-instruct-q4_k_m.gguf\n"
        "modalities : text\n\n"
        "available commands:\n"
        "  /exit or Ctrl+C     stop or exit\n"
        "  /regen              regenerate the last response\n"
        "  /clear              clear the chat history\n"
        "  /read <file>        add a text file\n"
        "  /glob <pattern>     add text files using globbing pattern\n\n\n"
        "> # System\n"
        "You are HyveGrid Offline, an offline apiculture field assistant.\n\n"
        "# Required answer format\n"
        "1. Possible concern\n"
        "2. Check first\n"
        "3. Avoid doing immediately\n"
        "4. Suggested next step\n"
        "5. When to escalate\n\n"
        "1. Possible concern: Low activity and ants may indicate a weak colony.\n"
        "2. Check first: Confirm by physical inspection of the entrance and brood.\n"
        "3. Avoid doing immediately: Avoid harvesting from a stressed colony.\n"
        "4. Suggested next step: Determine if ants are scavenging or harming bees.\n"
        "5. When to escalate: Consult an experienced beekeeper if it declines.\n"
        "\n[ Prompt: 17.4 t/s | Generation: 2.2 t/s ]\n\n"
        "Exiting...\n"
    )

    EXPECTED_ANSWER = (
        "1. Possible concern: Low activity and ants may indicate a weak colony.\n"
        "2. Check first: Confirm by physical inspection of the entrance and brood.\n"
        "3. Avoid doing immediately: Avoid harvesting from a stressed colony.\n"
        "4. Suggested next step: Determine if ants are scavenging or harming bees.\n"
        "5. When to escalate: Consult an experienced beekeeper if it declines."
    )

    def test_strips_chrome_and_echo_keeps_answer(self):
        out = rt.clean_llama_output(self.CHROME_STDOUT)
        self.assertEqual(out, self.EXPECTED_ANSWER)
        # Chrome is gone.
        for bad in [
            "Loading model",
            "available commands",
            "/regen",
            "build      :",
            "modalities :",
            "# System",
            "# Required answer format",
            "[ Prompt:",
            "Generation:",
            "Exiting...",
        ]:
            self.assertNotIn(bad, out, f"chrome leaked: {bad!r}")
        # Legitimate section headings are kept.
        self.assertIn("Check first", out)
        self.assertIn("Avoid doing immediately", out)

    def test_picks_last_answer_start_not_echoed_format_list(self):
        # The echoed prompt also contains "1. Possible concern" as a bare heading;
        # the cleaner must anchor on the real answer (the LAST match), so the
        # echoed format-only list is dropped.
        out = rt.clean_llama_output(self.CHROME_STDOUT)
        self.assertTrue(out.startswith("1. Possible concern: Low activity"))
        # The bare echoed heading (followed only by a newline then "2. Check first")
        # is NOT the start; the answer's colon content is what wins.
        self.assertIn("Confirm by physical inspection", out)

    def test_strips_timing_footer_minimal(self):
        stdout = (
            "> prompt echo line\n\n"
            "1. Possible concern: something\n2. Check first: steps\n"
            "\n[ Prompt: 1.0 t/s | Generation: 2.0 t/s ]\nExiting...\n"
        )
        out = rt.clean_llama_output(stdout)
        self.assertNotIn("[ Prompt:", out)
        self.assertNotIn("Exiting", out)
        self.assertIn("2. Check first: steps", out)

    def test_empty_and_blank(self):
        self.assertEqual(rt.clean_llama_output(""), "")
        self.assertEqual(rt.clean_llama_output("   \n\n  "), "")

    def test_fallback_when_no_format_anchor(self):
        # If the model did not start with "1. Possible concern", the cleaner
        # still drops recognized chrome lines and keeps the content.
        stdout = (
            "Loading model...\nbuild      : x\navailable commands:\n  /exit stop\n\n"
            "This is a free-form answer with no numbered format.\n"
            "\n[ Prompt: 1 t/s | Generation: 2 t/s ]\nExiting...\n"
        )
        out = rt.clean_llama_output(stdout)
        self.assertIn("free-form answer", out)
        self.assertNotIn("Loading model", out)
        self.assertNotIn("available commands", out)
        self.assertNotIn("[ Prompt:", out)


class NoCloudApiTests(unittest.TestCase):
    """Guard against introducing any cloud/network dependency."""

    def test_module_source_has_no_network_imports(self):
        source = Path(rt.__file__).read_text(encoding="utf-8")
        match = NETWORK_IMPORT_RE.search(source)
        self.assertIsNone(
            match,
            f"Found a networking import in llama_runtime.py: {match.group(0) if match else None}",
        )

    def test_defaults_are_local_paths(self):
        self.assertTrue(rt.DEFAULT_LLAMA_BIN.startswith("/"))
        self.assertTrue(rt.DEFAULT_MODEL_PATH.endswith(".gguf"))

    def test_resolves_default_model_from_repo_root(self):
        resolved = rt.resolve_runtime_path(rt.DEFAULT_MODEL_PATH)
        self.assertTrue(resolved.endswith("/model.gguf"))
        self.assertTrue(Path(resolved).is_absolute())

    def test_llama_bin_candidates_include_mac_and_vm_paths(self):
        candidates = rt.llama_bin_candidates()
        self.assertIn("/home/amaete/llama.cpp/build/bin/llama-cli", candidates)
        self.assertIn(str(Path.home() / "llama.cpp/build/bin/llama-cli"), candidates)
        self.assertIn(str(rt.REPO_ROOT / "llama.cpp/build/bin/llama-cli"), candidates)
        self.assertIn("/opt/homebrew/bin/llama-cli", candidates)
        self.assertIn("/usr/local/bin/llama-cli", candidates)

    def test_resolve_llama_bin_uses_first_executable_candidate(self):
        def isfile(path):
            return path == "/opt/homebrew/bin/llama-cli"

        def access(path, mode):
            return path == "/opt/homebrew/bin/llama-cli" and mode == os.X_OK

        with mock.patch.dict("os.environ", {}, clear=True), mock.patch(
            "app.llama_runtime.os.path.isfile", side_effect=isfile
        ), mock.patch("app.llama_runtime.os.access", side_effect=access):
            resolved = rt.resolve_llama_bin()
        self.assertTrue(resolved["found"])
        self.assertEqual(resolved["llama_bin"], "/opt/homebrew/bin/llama-cli")

    def test_missing_llama_bin_message_lists_fixes(self):
        message = rt.llama_bin_not_found_message(["/missing/llama-cli"])
        self.assertIn("/missing/llama-cli", message)
        self.assertIn('export LLAMA_BIN="$HOME/llama.cpp/build/bin/llama-cli"', message)
        self.assertIn(
            'export LLAMA_BIN="/home/amaete/llama.cpp/build/bin/llama-cli"',
            message,
        )

    def test_runtime_diagnostics_reports_configured_paths(self):
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch(
            "app.llama_runtime.os.path.isfile", return_value=False
        ), mock.patch("app.llama_runtime.os.access", return_value=False):
            diagnostics = rt.runtime_diagnostics(
                model_path="model.gguf",
                llama_bin="/home/amaete/llama.cpp/build/bin/llama-cli",
            )
        self.assertIn("hyvegrid-offline", diagnostics["repo_root"])
        self.assertTrue(diagnostics["model_path"].endswith("/model.gguf"))
        self.assertEqual(
            diagnostics["llama_bin"],
            "/home/amaete/llama.cpp/build/bin/llama-cli",
        )
        for key in [
            "model_exists",
            "llama_exists",
            "llama_executable",
            "llama_checked_paths",
            "llama_found",
        ]:
            self.assertIn(key, diagnostics)


if __name__ == "__main__":
    unittest.main()
