#!/usr/bin/env python3
"""Local CLI to ask HyveGrid Offline an apiculture question.

Builds a retrieval-backed prompt, runs it through the local llama.cpp Granite
model, and prints the retrieved sources and the answer. Local-only: no web UI,
no cloud APIs, no network.

Example:
    python3 scripts/ask_hyvegrid_cli.py "A beekeeper reports low hive activity, \
ants near the hive stand, normal smell, and partially capped brood. What should \
they check first?"
"""

import argparse
import sys
from pathlib import Path

# Allow running as a plain script by making the repo root importable.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app.llama_runtime import (  # noqa: E402
    DEFAULT_LLAMA_BIN,
    DEFAULT_MODEL_PATH,
    answer_question,
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Ask HyveGrid Offline a local apiculture question (no cloud)."
    )
    parser.add_argument("question", help="Field question to ask the assistant")
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, help="GGUF model path")
    parser.add_argument("--llama-bin", default=DEFAULT_LLAMA_BIN, help="llama-cli binary path")
    parser.add_argument("--limit", type=int, default=5, help="Number of notes to retrieve")
    parser.add_argument("--max-context-chars", type=int, default=3000)
    parser.add_argument("--max-tokens", type=int, default=384, help="Max tokens to generate")
    args = parser.parse_args(argv)

    bundle = answer_question(
        args.question,
        model_path=args.model,
        llama_bin=args.llama_bin,
        limit=args.limit,
        max_context_chars=args.max_context_chars,
        max_tokens=args.max_tokens,
    )

    print("Retrieved sources:")
    for r in bundle["results"]:
        print(f"- {r['source_file']} | {r['heading']}")
    print()

    runtime = bundle["runtime"]
    if runtime.get("timed_out"):
        print("TIMEOUT: inference exceeded the time limit. No answer produced.")
        return 1
    if runtime.get("returncode") != 0:
        print(f"ERROR: llama-cli exited with code {runtime.get('returncode')}.")
        if runtime.get("stderr"):
            print(runtime["stderr"][:800])
        return 1

    print("Answer:")
    print(bundle["answer"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
