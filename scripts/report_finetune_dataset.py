#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

SOURCE = Path("data/finetune/apiculture_qa_seed.jsonl")
TRAIN = Path("data/finetune/splits/apiculture_train_split_chat.jsonl")
EVAL = Path("data/finetune/splits/apiculture_eval_split_chat.jsonl")
OUT = Path("artifacts/step7/dataset-coverage-report.md")

def read_jsonl(path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows

def main():
    source_rows = read_jsonl(SOURCE)
    train_rows = read_jsonl(TRAIN)
    eval_rows = read_jsonl(EVAL)

    categories = Counter(row["category"] for row in source_rows)

    caution_hits = 0
    avoid_hits = 0
    inspection_hits = 0
    extension_hits = 0

    for row in source_rows:
        output = row["output"].lower()
        if "possible concern" in output:
            caution_hits += 1
        if "avoid" in output or "do not" in output:
            avoid_hits += 1
        if "physical inspection" in output or "inspect" in output:
            inspection_hits += 1
        if "extension officer" in output or "experienced beekeeper" in output:
            extension_hits += 1

    lines = []
    lines.append("# Step 7 Dataset Coverage Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Source examples: {len(source_rows)}")
    lines.append(f"- Train examples: {len(train_rows)}")
    lines.append(f"- Eval examples: {len(eval_rows)}")
    lines.append("")
    lines.append("## Category coverage")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    for category, count in sorted(categories.items()):
        lines.append(f"| {category} | {count} |")

    lines.append("")
    lines.append("## Answer-style checks")
    lines.append("")
    lines.append("| Check | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Uses cautious language, such as possible concern | {caution_hits} |")
    lines.append(f"| Includes avoid / do not guidance | {avoid_hits} |")
    lines.append(f"| Mentions inspection or physical inspection | {inspection_hits} |")
    lines.append(f"| Mentions experienced beekeeper or extension officer | {extension_hits} |")

    lines.append("")
    lines.append("## Current read")
    lines.append("")
    lines.append("The dataset now covers hive health, site readiness, pest pressure, pesticide risk, harvest quality, forage and pollination, hive signal checks, and hive management.")
    lines.append("")
    lines.append("Before fine-tuning, review whether the dataset needs more examples for:")
    lines.append("")
    lines.append("- More general agriculture prompts beyond bees, if hidden agriculture accuracy remains weak.")
    lines.append("- More multiple-choice style agriculture reasoning.")
    lines.append("- More site-readiness variations.")
    lines.append("- More official-prompt variants.")
    lines.append("- More short-answer responses, because the model benchmark may limit tokens.")
    lines.append("")
    lines.append("## Next recommendation")
    lines.append("")
    lines.append("The dataset has reached the 60-example checkpoint. Next, create a small first fine-tune experiment ticket. Do not lock a tuned model unless it beats the baseline models on official prompts, eval split, safety, RAM, and throughput.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT}")
    print(f"Source examples: {len(source_rows)}")
    print(f"Train examples: {len(train_rows)}")
    print(f"Eval examples: {len(eval_rows)}")

if __name__ == "__main__":
    main()
