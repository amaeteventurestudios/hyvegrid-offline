"""Local SQLite FTS5 retrieval for the public apiculture knowledge notes.

This module is the canonical retrieval layer. It can build the knowledge
database from Markdown notes and run full-text searches against it.

Standard library only. No network, no cloud calls, no external services.

HyveGrid is not a certified disease diagnosis tool. The retrieval layer returns
field-triage notes for reasoning support only; it does not replace physical
inspection or expert guidance.
"""

import re
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = "data/knowledge/knowledge.db"
DEFAULT_KNOWLEDGE_DIR = "data/knowledge"

CREATE_CHUNKS_SQL = """
CREATE TABLE knowledge_chunks (
    id INTEGER PRIMARY KEY,
    source_file TEXT NOT NULL,
    title TEXT NOT NULL,
    heading TEXT NOT NULL,
    body TEXT NOT NULL
)
"""

CREATE_FTS_SQL = """
CREATE VIRTUAL TABLE knowledge_chunks_fts USING fts5(
    title,
    heading,
    body,
    content='knowledge_chunks',
    content_rowid='id'
)
"""


def fts5_available() -> bool:
    """Return True if the linked SQLite supports FTS5."""
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE VIRTUAL TABLE _probe USING fts5(a)")
    except sqlite3.OperationalError:
        return False
    finally:
        con.close()
    return True


def _clean_line(line: str) -> str:
    """Strip markdown emphasis and list bullets so bodies index as plain text."""
    line = line.replace("**", "")
    line = re.sub(r"^[-*+]\s+", "", line)
    return line.rstrip()


def split_markdown(text: str):
    """Split Markdown into (title, heading, body) sections by headings.

    The H1 line is treated as the document title. Each H2 starts a new section;
    deeper headings (H3+) are kept as part of the current section's body. Lines
    before the first H2 are ignored (they are usually just the title).
    """
    title = ""
    heading = ""
    body_lines = []

    def flush():
        if not heading:
            return None
        body = "\n".join(body_lines).strip()
        return title, heading, body

    sections = []
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("# ") and not stripped.startswith("## "):
            done = flush()
            if done:
                sections.append(done)
            heading = ""
            body_lines = []
            title = stripped[2:].strip()
            continue
        if stripped.startswith("## ") and not stripped.startswith("### "):
            done = flush()
            if done:
                sections.append(done)
            heading = stripped[3:].strip()
            body_lines = []
            continue
        body_lines.append(_clean_line(raw))

    done = flush()
    if done:
        sections.append(done)
    return sections


def _iter_markdown_files(knowledge_dir: Path):
    """Yield .md files in the knowledge dir, excluding the DB and sidecars."""
    for path in sorted(knowledge_dir.glob("*.md")):
        name = path.name
        if name.endswith(".db") or ".db-" in name:
            continue
        yield path


def _db_has_tables(con: sqlite3.Connection) -> bool:
    """Return True if both required tables exist in the database."""
    cur = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name IN ('knowledge_chunks', 'knowledge_chunks_fts')"
    )
    existing = {row[0] for row in cur.fetchall()}
    return existing == {"knowledge_chunks", "knowledge_chunks_fts"}


def build_database(knowledge_dir: Path, db_path: Path) -> int:
    """Build the SQLite + FTS5 database. Returns the number of chunks stored."""
    if not fts5_available():
        raise RuntimeError(
            "FTS5 is not available in this Python sqlite3 build; "
            "cannot build the knowledge database."
        )

    markdown_files = list(_iter_markdown_files(knowledge_dir))
    if not markdown_files:
        raise FileNotFoundError(f"No .md files found in {knowledge_dir}")

    # Idempotent: start from a clean file so reruns never accumulate stale rows.
    if db_path.exists():
        db_path.unlink()
    for sidecar in db_path.parent.glob(db_path.name + "*"):
        if sidecar != db_path:
            sidecar.unlink(missing_ok=True)

    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()
        cur.execute(CREATE_CHUNKS_SQL)
        cur.execute(CREATE_FTS_SQL)

        count = 0
        for md_path in markdown_files:
            text = md_path.read_text(encoding="utf-8")
            source_file = md_path.name
            for title, heading, body in split_markdown(text):
                if not body:
                    continue
                cur.execute(
                    "INSERT INTO knowledge_chunks "
                    "(source_file, title, heading, body) VALUES (?, ?, ?, ?)",
                    (source_file, title, heading, body),
                )
                count += 1

        # Populate the FTS index from the linked content table.
        cur.execute(
            "INSERT INTO knowledge_chunks_fts(knowledge_chunks_fts) "
            "VALUES('rebuild')"
        )
        con.commit()
    finally:
        con.close()

    return count


def build_or_open_db(db_path: str = DEFAULT_DB_PATH):
    """Open the knowledge DB, building it from notes if it is missing or empty.

    Returns the db_path. Uses the sibling knowledge directory (the parent of the
    db file by default) as the source of Markdown notes when a build is needed.
    """
    db_path = Path(db_path)
    needs_build = True
    if db_path.exists():
        con = sqlite3.connect(db_path)
        try:
            needs_build = not _db_has_tables(con)
        finally:
            con.close()

    if needs_build:
        knowledge_dir = db_path.parent if db_path.parent.name else Path(DEFAULT_KNOWLEDGE_DIR)
        build_database(knowledge_dir, db_path)
    return str(db_path)


def _row_to_result(row) -> dict:
    source_file, title, heading, body, score = row
    return {
        "source_file": source_file,
        "title": title,
        "heading": heading,
        "body": body,
        "score": score,
    }


def _to_fts_query(query: str) -> str:
    """Sanitize a free-text query into an FTS5 OR query.

    FTS5 implicit-combines whitespace-separated tokens with AND, which returns
    nothing when a multi-term question does not share every token with one chunk.
    For a retrieval layer over small notes we want high recall with bm25 ranking,
    so alphanumeric tokens are deduplicated and OR-joined. Stripping non-alphanumerics
    also avoids FTS5 syntax surprises (-, *, :, quotes, parentheses).
    """
    tokens = re.findall(r"[A-Za-z0-9]+", query)
    tokens = list(dict.fromkeys(tokens))  # dedupe, preserve order
    return " OR ".join(tokens)


def _fts_search(con: sqlite3.Connection, query: str, limit: int):
    """Run an FTS5 MATCH query with bm25 ranking. Returns result rows."""
    fts_query = _to_fts_query(query)
    if not fts_query:
        return []
    # bm25() is negative; more negative means a better match. Negate so that a
    # higher score means a better match, and order best-first.
    sql = (
        "SELECT k.source_file, k.title, k.heading, k.body, "
        "-bm25(knowledge_chunks_fts) AS score "
        "FROM knowledge_chunks_fts "
        "JOIN knowledge_chunks k ON k.id = knowledge_chunks_fts.rowid "
        "WHERE knowledge_chunks_fts MATCH ? "
        "ORDER BY score DESC "
        "LIMIT ?"
    )
    cur = con.execute(sql, (fts_query, limit))
    return cur.fetchall()


def _like_search(con: sqlite3.Connection, query: str, limit: int):
    """Fallback search using LIKE across the normal table (no FTS5)."""
    terms = [t for t in re.split(r"\s+", query.strip()) if t]
    if not terms:
        return []
    where = " OR ".join(
        ["body LIKE ? OR heading LIKE ? OR title LIKE ?" for _ in terms]
    )
    params = []
    for term in terms:
        params.extend([f"%{term}%", f"%{term}%", f"%{term}%"])
    sql = (
        "SELECT source_file, title, heading, body, 0.0 AS score "
        "FROM knowledge_chunks WHERE " + where + " LIMIT ?"
    )
    params.append(limit)
    cur = con.execute(sql, params)
    return cur.fetchall()


def search_knowledge(query: str, db_path: str = DEFAULT_DB_PATH, limit: int = 5):
    """Search the knowledge DB and return a list of result dicts.

    Each dict has: source_file, title, heading, body, score. Uses FTS5 with bm25
    ranking when available, falling back clearly to a LIKE search otherwise.
    """
    build_or_open_db(db_path)
    con = sqlite3.connect(db_path)
    try:
        has_fts = _db_has_tables(con)
        if has_fts:
            try:
                rows = _fts_search(con, query, limit)
            except sqlite3.OperationalError:
                # FTS5 missing at query time: fall back to LIKE.
                rows = _like_search(con, query, limit)
        else:
            rows = _like_search(con, query, limit)
    finally:
        con.close()
    return [_row_to_result(row) for row in rows]


def format_retrieval_context(results, max_chars: int = 3000) -> str:
    """Format search results into a compact context string.

    Each result is labelled with its source file and heading. Output is kept
    under max_chars by trimming the final block, preserving the cautious field
    language of the notes. Returns an empty string if there are no results.
    """
    if not results:
        return ""

    blocks = []
    for r in results:
        body = (r.get("body") or "").strip()
        block = "[{source} > {heading}]\n{body}".format(
            source=r.get("source_file", "?"),
            heading=r.get("heading", "?"),
            body=body,
        )
        blocks.append(block)

    sep = "\n\n"
    out_parts = []
    used = 0
    suffix = " …"
    for block in blocks:
        # Account for the separator that precedes every block after the first.
        extra = len(sep) if out_parts else 0
        if used + extra + len(block) <= max_chars:
            out_parts.append(block)
            used += extra + len(block)
            continue
        # Truncate the overflowing block, reserving room for the ellipsis so the
        # final joined string never exceeds max_chars.
        remaining = max_chars - used - extra
        if remaining > len(suffix):
            out_parts.append(block[: remaining - len(suffix)].rstrip() + suffix)
        break

    return sep.join(out_parts)
