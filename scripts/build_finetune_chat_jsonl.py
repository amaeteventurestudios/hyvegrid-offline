#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

SYSTEM_PROMPT = (
    "You are HyveGrid Offline, a cautious offline apiculture field assistant "
    "for African beekeepers and extension workers. Give practical field triage, "
    "not certified diagnosis. Start with possible concern when appropriate. "
    "Explain what to check first, what to avoid doing immediately, and when to "
    "confirm by physical inspection or consult an experienced beekeeper or "
    "extension officer."
)

REQUIRED = {"id", "category", "input", "output"}

def main():
    parser = argparse.ArgumentParser(description="Convert HyveGrid QA JSONL to chat fine-tune JSONL.")
    parser.add_argument("--input", default="data/finetune/apiculture_qa_seed.jsonl")
    parser.add_argument("--output", default="data/finetune/apiculture_train_chat.jsonl")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    rows = []
    errors = 0

    with input_path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Line {line_no}: invalid JSON: {e}", file=sys.stderr)
                errors += 1
                continue

            missing = REQUIRED - row.keys()
            if missing:
                print(f"Line {line_no}: missing fields: {sorted(missing)}", file=sys.stderr)
                errors += 1
                continue

            rows.append({
                "id": row["id"],
                "category": row["category"],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": row["input"]},
                    {"role": "assistant", "content": row["output"]},
                ],
            })

    if errors:
        print(f"FAILED: {errors} issue(s) found.", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(rows)} chat examples to {output_path}")

if __name__ == "__main__":
    main()
