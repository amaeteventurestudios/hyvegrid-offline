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

import os
import subprocess

from app.prompt_builder import build_prompt_with_retrieval

DEFAULT_LLAMA_BIN = "/home/amaete/llama.cpp/build/bin/llama-cli"
DEFAULT_MODEL_PATH = "model/granite-3.3-2b-instruct-q4_k_m.gguf"


def _to_text(value) -> str:
    """Coerce subprocess output (bytes/str/None) to str."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value


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
      --single-turn         answer once, then exit
      --no-display-prompt   stdout contains only the generated answer
      --simple-io           basic IO for clean subprocess capture
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
    if not os.path.isfile(llama_bin):
        raise RuntimeError(
            f"llama.cpp binary not found at {llama_bin!r}. "
            "Build llama.cpp and check the path."
        )
    if not os.path.isfile(model_path):
        raise RuntimeError(
            f"Model file not found at {model_path!r}. "
            "Download or link the GGUF model and check the path."
        )

    command = _build_command(
        llama_bin, model_path, prompt, max_tokens, temperature, threads
    )

    result = {
        "answer": "",
        "stdout": "",
        "stderr": "",
        "returncode": None,
        "model_path": model_path,
        "llama_bin": llama_bin,
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
        result["answer"] = result["stdout"].strip()
        return result

    result["stdout"] = _to_text(proc.stdout)
    result["stderr"] = _to_text(proc.stderr)
    result["returncode"] = proc.returncode
    if proc.returncode == 0:
        result["answer"] = result["stdout"].strip()

    return result


def answer_question(
    question: str,
    model_path: str = DEFAULT_MODEL_PATH,
    llama_bin: str = DEFAULT_LLAMA_BIN,
    limit: int = 5,
    max_context_chars: int = 3000,
    max_tokens: int = 384,
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
