#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

EVAL_IDS = {
    "brood_smell_001",
    "flooding_site_001",
    "storage_filtering_001",
    "edge_signal_low_activity_001",
    "mcq_pesticide_001",
    "short_site_001",
    "soil_moisture_001",
    "extension_triage_001",
}

SYSTEM_PROMPT = (
    "You are HyveGrid Offline, a cautious offline apiculture field assistant "
    "for African beekeepers and extension workers. Give practical field triage, "
    "not certified diagnosis. Start with possible concern when appropriate. "
    "Explain what to check first, what to avoid doing immediately, and when to "
    "confirm by physical inspection or consult an experienced beekeeper or "
    "extension officer."
)

def to_chat(row):
    return {
        "id": row["id"],
        "category": row["category"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": row["input"]},
            {"role": "assistant", "content": row["output"]},
        ],
    }

def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Split HyveGrid fine-tune seed dataset into train and eval chat JSONL.")
    parser.add_argument("--input", default="data/finetune/apiculture_qa_seed.jsonl")
    parser.add_argument("--train-output", default="data/finetune/splits/apiculture_train_split_chat.jsonl")
    parser.add_argument("--eval-output", default="data/finetune/splits/apiculture_eval_split_chat.jsonl")
    args = parser.parse_args()

    source_path = Path(args.input)
    train_path = Path(args.train_output)
    eval_path = Path(args.eval_output)

    train_rows = []
    eval_rows = []

    with source_path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            row = json.loads(line)
            chat_row = to_chat(row)

            if row["id"] in EVAL_IDS:
                eval_rows.append(chat_row)
            else:
                train_rows.append(chat_row)

    write_jsonl(train_path, train_rows)
    write_jsonl(eval_path, eval_rows)

    print(f"Wrote {len(train_rows)} train examples to {train_path}")
    print(f"Wrote {len(eval_rows)} eval examples to {eval_path}")

    if len(eval_rows) != len(EVAL_IDS):
        found = {row["id"] for row in eval_rows}
        missing = sorted(EVAL_IDS - found)
        raise SystemExit(f"Missing eval IDs: {missing}")

if __name__ == "__main__":
    main()
