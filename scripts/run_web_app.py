#!/usr/bin/env python3
"""Run the HyveGrid Offline local web app on 127.0.0.1:8000.

Local only. No cloud access. Loads no GGUF model at startup.

Usage:
    python3 scripts/run_web_app.py
Then open http://127.0.0.1:8000
"""

import argparse
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import uvicorn  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the HyveGrid Offline local web app."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    uvicorn.run("app.web_app:app", host=args.host, port=args.port, log_level="info")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
