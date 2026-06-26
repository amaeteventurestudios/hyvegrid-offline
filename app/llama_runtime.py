"""Local llama.cpp runtime wrapper for HyveGrid Offline.

Sends a built HyveGrid prompt to the local Granite GGUF model through the
llama.cpp `llama-cli` binary via subprocess. This connects the prompt builder to
llama.cpp while staying simple and testable.

This module runs a local process only. It never calls the network and never
calls cloud APIs. It does not edit model weights or scoring.

Contract:
- Missing llama binary or model file raises RuntimeError (configuration error).
- A subprocess timeout or non-zero exit does NOT raise; it returns a result
  dict carrying the failure details (timed_out / returncode / stderr) so the
  caller can decide what to do.
"""

import logging
import os
import re
import subprocess
from pathlib import Path

from app.prompt_builder import build_prompt_with_retrieval

LOGGER = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LLAMA_BIN = "/home/amaete/llama.cpp/build/bin/llama-cli"
DEFAULT_MODEL_PATH = "model.gguf"


def _to_text(value) -> str:
    """Coerce subprocess output (bytes/str/None) to str."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value


def resolve_runtime_path(path: str) -> str:
    """Resolve a runtime path deterministically from the repo root.

    Absolute paths are preserved. Relative paths are anchored at the HyveGrid
    repo root so uvicorn can be launched from any working directory.
    """
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    return os.path.abspath(candidate)


def runtime_diagnostics(
    model_path: str = DEFAULT_MODEL_PATH,
    llama_bin: str = DEFAULT_LLAMA_BIN,
) -> dict:
    """Return path diagnostics for server logs and focused tests."""
    resolved_model_path = resolve_runtime_path(model_path)
    resolved_llama_bin = resolve_runtime_path(llama_bin)
    return {
        "repo_root": str(REPO_ROOT),
        "model_path": resolved_model_path,
        "model_exists": os.path.isfile(resolved_model_path),
        "llama_bin": resolved_llama_bin,
        "llama_exists": os.path.isfile(resolved_llama_bin),
        "llama_executable": os.access(resolved_llama_bin, os.X_OK),
    }


def log_runtime_diagnostics(
    model_path: str = DEFAULT_MODEL_PATH,
    llama_bin: str = DEFAULT_LLAMA_BIN,
    *,
    level: int = logging.INFO,
) -> dict:
    """Log local model/runtime paths without exposing prompts or stdout."""
    diagnostics = runtime_diagnostics(model_path=model_path, llama_bin=llama_bin)
    LOGGER.log(
        level,
        "HyveGrid runtime diagnostics: repo_root=%s model_path=%s "
        "model_exists=%s llama_bin=%s llama_exists=%s llama_executable=%s",
        diagnostics["repo_root"],
        diagnostics["model_path"],
        diagnostics["model_exists"],
        diagnostics["llama_bin"],
        diagnostics["llama_exists"],
        diagnostics["llama_executable"],
    )
    return diagnostics


# --- Output cleaning -----------------------------------------------------
# llama-cli runs in conversation mode (the only mode this binary supports;
# --no-conversation is rejected) so it can apply Granite's chat template. That
# mode prints a TUI to stdout: a banner/logo, build/model lines, an
# "available commands" help block, an echoed copy of the prompt, the answer,
# then a timing line and "Exiting...". clean_llama_output() keeps only the
# answer.

# The timing footer that marks the end of the answer, e.g. "[ Prompt: .. t/s | Generation: .. t/s ]".
_TIMING_LINE_RE = re.compile(
    r"^\s*\[\s*Prompt\s*:.*?Generation\s*:.*?\]\s*$", re.IGNORECASE
)
# The model answer reliably begins with the first required section. The echoed
# prompt also lists "1. Possible concern" in the format instructions, so the
# cleaner takes the LAST match (the real answer), not the first.
_ANSWER_START_RE = re.compile(
    r"^\s*1[\.\)]\s*[*_`]?\s*Possible Concern\b", re.IGNORECASE
)
# Fallback chrome lines (banner art, build/model/modalities, command help, the
# ">" chat marker, "Exiting..."). Block-drawing chars cover the ASCII logo.
_CHROME_LINE_RE = re.compile(
    r"^("
    r"Loading model|"
    r"\s*>|"
    r"build\s*:|model\s*:|modalities\s*:|"
    r"available commands:|"
    r"\s*/(exit|regen|clear|read|glob)\b|"
    r"Exiting\.\.\."
    r")",
    re.IGNORECASE,
)
_BLOCK_ART_RE = re.compile(r"[▄▀█]")


def clean_llama_output(text: str) -> str:
    """Strip llama.cpp conversation-mode chrome and the echoed prompt.

    Returns only the model's answer. Removes the banner/ASCII logo, "Loading
    model...", build/model/modalities lines, the "available commands" help, the
    echoed prompt, the timing line, and "Exiting...". Legitimate answer content
    such as the section headings "Check first" and "Avoid doing immediately" is
    preserved.
    """
    if not text:
        return ""
    lines = text.splitlines()

    # 1. Drop the timing footer and everything after it.
    for i, line in enumerate(lines):
        if _TIMING_LINE_RE.match(line):
            lines = lines[:i]
            break

    # 2. Prefer the structured anchor: the answer starts with "1. Possible
    #    concern". Take the LAST such line because the echoed prompt also lists
    #    it in the format instructions.
    start_idx = None
    for i in range(len(lines) - 1, -1, -1):
        if _ANSWER_START_RE.match(lines[i]):
            start_idx = i
            break

    if start_idx is not None:
        answer_lines = lines[start_idx:]
    else:
        # Fallback for answers that do not follow the format: drop recognized
        # chrome lines (banner, command help, chat markers, Exiting) and keep
        # the rest.
        answer_lines = [
            ln
            for ln in lines
            if not (_CHROME_LINE_RE.match(ln) or _BLOCK_ART_RE.search(ln))
        ]

    # 3. Defensively strip any leading chat marker and trim blanks.
    cleaned = [re.sub(r"^\s*>\s?", "", ln) for ln in answer_lines]
    answer = "\n".join(cleaned).strip()

    # 4. Best-effort fallback if nothing survived.
    return answer if answer else text.strip()


def _build_command(
    llama_bin: str,
    model_path: str,
    prompt: str,
    max_tokens: int,
    temperature: float,
    threads: int,
) -> list:
    """Build the llama-cli argv list.

    Flags used (all verified against this local llama.cpp build):
      -m   model file
      -p   prompt text
      -n   number of tokens to predict
      -t   CPU threads
      --temp                sampling temperature
      --single-turn         answer once, then exit (avoids an empty-turn loop)
      --no-display-prompt   best-effort prompt-echo suppression
      --simple-io           basic IO for clean subprocess capture
      --no-warmup           skip the throwaway warmup pass (speed)
    """
    return [
        llama_bin,
        "-m", model_path,
        "-p", prompt,
        "-n", str(max_tokens),
        "-t", str(threads),
        "--temp", str(temperature),
        "--single-turn",
        "--no-display-prompt",
        "--simple-io",
        "--no-warmup",
    ]


def run_llama_prompt(
    prompt: str,
    model_path: str = DEFAULT_MODEL_PATH,
    llama_bin: str = DEFAULT_LLAMA_BIN,
    max_tokens: int = 384,
    temperature: float = 0.2,
    threads: int = 4,
    # The target hardware is a low-cost 8 GB laptop where the ~6 GB Q4 Granite
    # model pages against swap, so a single 384-token answer can exceed 3 minutes
    # of wall time. 600 s gives headroom without being unbounded.
    timeout_seconds: int = 600,
) -> dict:
    """Run a prompt through the local llama-cli and return a result dict.

    Returns:
      {
        "answer": "...",      # stripped stdout when returncode == 0
        "stdout": "...",
        "stderr": "...",
        "returncode": 0,      # None on timeout
        "model_path": "...",
        "llama_bin": "...",
        "timed_out": False,
      }

    Raises RuntimeError if the llama binary or model file is missing.
    """
    resolved_llama_bin = resolve_runtime_path(llama_bin)
    resolved_model_path = resolve_runtime_path(model_path)
    log_runtime_diagnostics(
        model_path=resolved_model_path,
        llama_bin=resolved_llama_bin,
        level=logging.INFO,
    )

    if not os.path.isfile(resolved_llama_bin):
        raise RuntimeError(
            f"llama.cpp binary not found at {resolved_llama_bin!r}. "
            "Build llama.cpp and check the path."
        )
    if not os.path.isfile(resolved_model_path):
        raise RuntimeError(
            f"Model file not found at {resolved_model_path!r}. "
            "Download or link the GGUF model and check the path."
        )

    command = _build_command(
        resolved_llama_bin, resolved_model_path, prompt, max_tokens, temperature, threads
    )

    result = {
        "answer": "",
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "model_path": resolved_model_path,
        "llama_bin": resolved_llama_bin,
        "timed_out": False,
    }

    try:
        proc = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        # Return useful timeout info instead of raising.
        result["timed_out"] = True
        result["stdout"] = _to_text(exc.stdout)
        result["stderr"] = _to_text(exc.stderr)
        result["answer"] = clean_llama_output(result["stdout"])
        return result

    result["stdout"] = _to_text(proc.stdout)
    result["stderr"] = _to_text(proc.stderr)
    result["returncode"] = proc.returncode
    if proc.returncode == 0:
        result["answer"] = clean_llama_output(result["stdout"])

    return result


def answer_question(
    question: str,
    model_path: str = DEFAULT_MODEL_PATH,
    llama_bin: str = DEFAULT_LLAMA_BIN,
    limit: int = 5,
    max_context_chars: int = 1800,
    max_tokens: int = 512,
) -> dict:
    """Answer a field question end-to-end, locally and offline.

    Builds the prompt via the retrieval-backed prompt builder, then runs it
    through llama.cpp. Returns a dict combining the prompt bundle and the
    runtime result.
    """
    bundle = build_prompt_with_retrieval(
        question, limit=limit, max_context_chars=max_context_chars
    )
    runtime = run_llama_prompt(
        bundle["prompt"],
        model_path=model_path,
        llama_bin=llama_bin,
        max_tokens=max_tokens,
    )
    return {
        "question": question,
        "prompt": bundle["prompt"],
        "context": bundle["context"],
        "results": bundle["results"],
        "answer": runtime["answer"],
        "runtime": runtime,
    }
