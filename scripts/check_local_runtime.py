#!/usr/bin/env python3
"""Fast local llama.cpp runtime setup diagnostics for HyveGrid Offline."""

import os
import platform
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.llama_runtime import (  # noqa: E402
    DEFAULT_LLAMA_BIN,
    LLAMA_BIN_ENV,
    llama_bin_not_found_message,
    resolve_llama_bin,
)


def _exists_line(path: Path) -> str:
    return f"{path}: exists={path.is_file()}"


def main() -> int:
    configured = os.environ.get(LLAMA_BIN_ENV, DEFAULT_LLAMA_BIN)
    resolved = resolve_llama_bin(configured)
    llama_bin = resolved["llama_bin"]

    print("HyveGrid local runtime diagnostics")
    print(f"platform: {platform.platform()}")
    print(f"python: {sys.executable}")
    print(f"repo_root: {REPO_ROOT}")
    print(f"LLAMA_BIN set: {LLAMA_BIN_ENV in os.environ}")
    if os.environ.get(LLAMA_BIN_ENV):
        print(f"LLAMA_BIN value: {os.environ[LLAMA_BIN_ENV]}")

    print("checked llama-cli paths:")
    for path in resolved["checked_paths"]:
        print(f"- {path}")

    print(f"resolved llama-cli: {llama_bin or 'not found'}")
    if llama_bin:
        llama_path = Path(llama_bin)
        print(f"llama-cli exists: {llama_path.is_file()}")
        print(f"llama-cli executable: {os.access(llama_path, os.X_OK)}")
    else:
        print("llama-cli exists: False")
        print("llama-cli executable: False")
        print(llama_bin_not_found_message(resolved["checked_paths"]))

    print("model file checks:")
    for model_path in [
        REPO_ROOT / "model" / "hyvegrid-offline.gguf",
        REPO_ROOT / "model" / "granite-3.3-2b-instruct-Q4_K_M.gguf",
        REPO_ROOT / "model.gguf",
    ]:
        print(f"- {_exists_line(model_path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
