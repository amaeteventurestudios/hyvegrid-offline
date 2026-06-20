#!/usr/bin/env python3
import json
from pathlib import Path

BASE_TRAIN = Path("data/finetune/splits/apiculture_train_split_chat.jsonl")
BASE_EVAL = Path("data/finetune/splits/apiculture_eval_split_chat.jsonl")
SUPPLEMENT = Path("data/finetune/v3/official_prompt_family_supplement_chat.jsonl")

OUT_TRAIN = Path("data/finetune/v3/apiculture_v3_train_chat.jsonl")
OUT_EVAL = Path("data/finetune/v3/apiculture_v3_eval_chat.jsonl")

def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def main():
    base_train = read_jsonl(BASE_TRAIN)
    base_eval = read_jsonl(BASE_EVAL)
    supplement = read_jsonl(SUPPLEMENT)

    # Keep most official-family examples in train, hold a few variants out for eval.
    supplement_train = supplement[:9]
    supplement_eval = supplement[9:]

    train = base_train + supplement_train
    eval_rows = base_eval + supplement_eval

    write_jsonl(OUT_TRAIN, train)
    write_jsonl(OUT_EVAL, eval_rows)

    print(f"Base train: {len(base_train)}")
    print(f"Base eval: {len(base_eval)}")
    print(f"Supplement: {len(supplement)}")
    print(f"V3 train: {len(train)} -> {OUT_TRAIN}")
    print(f"V3 eval: {len(eval_rows)} -> {OUT_EVAL}")

    for path in [OUT_TRAIN, OUT_EVAL]:
        for row in read_jsonl(path):
            assert "messages" in row
            assert len(row["messages"]) == 3
            assert row["messages"][0]["role"] == "system"
            assert row["messages"][1]["role"] == "user"
            assert row["messages"][2]["role"] == "assistant"

if __name__ == "__main__":
    main()
