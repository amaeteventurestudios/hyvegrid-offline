#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = {"id", "category", "input", "output"}

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/validate_finetune_jsonl.py data/finetune/apiculture_qa_seed.jsonl")
        sys.exit(1)

    path = Path(sys.argv[1])
    seen_ids = set()
    errors = 0

    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                print(f"Line {i}: empty line")
                errors += 1
                continue

            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {i}: invalid JSON: {e}")
                errors += 1
                continue

            missing = REQUIRED - row.keys()
            if missing:
                print(f"Line {i}: missing fields: {sorted(missing)}")
                errors += 1

            row_id = row.get("id")
            if row_id in seen_ids:
                print(f"Line {i}: duplicate id: {row_id}")
                errors += 1
            seen_ids.add(row_id)

            for field in REQUIRED:
                value = row.get(field, "")
                if not isinstance(value, str) or not value.strip():
                    print(f"Line {i}: field '{field}' must be non-empty text")
                    errors += 1

            output = row.get("output", "")
            banned_fragments = [
                "proprietary hardware",
                "sensor design",
                "firmware strategy",
                "Honey Flow Africa internal",
                "partner strategy",
                "investor",
                "patent",
            ]
            for banned in banned_fragments:
                if banned.lower() in output.lower():
                    print(f"Line {i}: possible IP-risk phrase in output: {banned}")
                    errors += 1

    if errors:
        print(f"FAILED: {errors} issue(s) found.")
        sys.exit(1)

    print(f"OK: {len(seen_ids)} examples validated.")

if __name__ == "__main__":
    main()
