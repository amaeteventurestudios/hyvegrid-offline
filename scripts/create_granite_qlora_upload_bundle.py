#!/usr/bin/env python3
import zipfile
from pathlib import Path

FILES = [
    "notebooks/granite_qlora_colab_runtime.py",
    "notebooks/granite_qlora_colab_runtime_v2.py",
    "notebooks/granite_qlora_colab_runtime_v3.py",
    "data/finetune/splits/apiculture_train_split_chat.jsonl",
    "data/finetune/splits/apiculture_eval_split_chat.jsonl",
    "data/finetune/apiculture_qa_seed.jsonl",
    "data/finetune/v3/official_prompt_family_supplement_chat.jsonl",
    "data/finetune/v3/apiculture_v3_train_chat.jsonl",
    "data/finetune/v3/apiculture_v3_eval_chat.jsonl",
    "artifacts/step7/granite-qlora-colab-ticket.md",
    "artifacts/step7/granite-lora-notebook-plan.md",
    "artifacts/step7/tuned-model-import-export-checklist.md",
    "artifacts/step7/dataset-coverage-report.md",
    "artifacts/step7/granite-qlora-colab-runbook.md",
    "artifacts/step7/granite-qlora-v2-experiment-note.md",
    "artifacts/step7/granite-qlora-v3-plan.md",
]

OUT = Path("artifacts/step7/granite-qlora-upload-bundle.zip")

def main():
    missing = [p for p in FILES if not Path(p).exists()]
    if missing:
        raise SystemExit(f"Missing files: {missing}")

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for file_path in FILES:
            z.write(file_path, arcname=file_path)

    print(f"Wrote {OUT}")
    print("Included files:")
    for file_path in FILES:
        print(f"- {file_path}")

if __name__ == "__main__":
    main()
