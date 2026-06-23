#!/usr/bin/env python3
"""CLI to build the local SQLite FTS5 retrieval database.

Thin wrapper around app.retrieval.build_database. The build logic lives in
app/retrieval.py so the retrieval layer has a single source of truth.

Standard library only. No network, no cloud calls.
"""

import argparse
import sys
from pathlib import Path

# Allow running as a plain script (python3 scripts/build_knowledge_db.py)
# by making the repo root importable.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from app.retrieval import DEFAULT_DB_PATH, DEFAULT_KNOWLEDGE_DIR, build_database  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the local SQLite FTS5 knowledge database."
    )
    parser.add_argument(
        "--knowledge-dir",
        default=DEFAULT_KNOWLEDGE_DIR,
        help=f"Directory of Markdown notes (default: {DEFAULT_KNOWLEDGE_DIR})",
    )
    parser.add_argument(
        "--db-path",
        default=DEFAULT_DB_PATH,
        help=f"Output SQLite path (default: {DEFAULT_DB_PATH})",
    )
    args = parser.parse_args(argv)

    knowledge_dir = Path(args.knowledge_dir)
    db_path = Path(args.db_path)

    try:
        count = build_database(knowledge_dir, db_path)
    except (RuntimeError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Built {db_path} with {count} chunks from {knowledge_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
