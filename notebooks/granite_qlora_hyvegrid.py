# HyveGrid Offline - Granite QLoRA Notebook Skeleton
#
# Purpose:
# Development-only fine-tune experiment for HyveGrid Offline.
#
# Important:
# This script is for a GPU notebook or training environment only.
# The judged ADTC runtime must remain offline, local, GGUF, and llama.cpp.
#
# Expected input files:
# - data/finetune/splits/apiculture_train_split_chat.jsonl
# - data/finetune/splits/apiculture_eval_split_chat.jsonl
#
# Expected output:
# - A LoRA adapter or merged tuned checkpoint
# - Quick eval outputs
# - Files that can later be converted to GGUF and quantized locally

# ------------------------------------------------------------
# 1. Install dependencies in the notebook environment
# ------------------------------------------------------------
#
# In Colab/Kaggle, run something like:
#
# !pip install -U transformers datasets accelerate peft trl bitsandbytes sentencepiece
#
# If using Unsloth, install according to the current Unsloth documentation.
# Do not assume this script runs unchanged across all GPU notebook providers.

# ------------------------------------------------------------
# 2. Imports
# ------------------------------------------------------------

import json
from pathlib import Path

# These imports are expected in the notebook training environment.
# Uncomment when dependencies are installed.

# import torch
# from datasets import load_dataset
# from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
# from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
# from trl import SFTTrainer

# ------------------------------------------------------------
# 3. Paths
# ------------------------------------------------------------

BASE_MODEL = "ibm-granite/granite-3.3-2b-instruct"

TRAIN_FILE = "data/finetune/splits/apiculture_train_split_chat.jsonl"
EVAL_FILE = "data/finetune/splits/apiculture_eval_split_chat.jsonl"

OUTPUT_DIR = "artifacts/training/granite-hyvegrid-lora"
QUICK_EVAL_OUT = "artifacts/training/granite-hyvegrid-lora-quick-eval.jsonl"

# ------------------------------------------------------------
# 4. Sanity check dataset files
# ------------------------------------------------------------

def count_jsonl(path):
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())

print("Train examples:", count_jsonl(TRAIN_FILE))
print("Eval examples:", count_jsonl(EVAL_FILE))

# ------------------------------------------------------------
# 5. Prompt formatting helper
# ------------------------------------------------------------

def format_chat_example(example):
    """
    Converts one HyveGrid chat JSONL row into a simple instruction text block.

    The source row format is:
    {
      "id": "...",
      "category": "...",
      "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
      ]
    }
    """
    messages = example["messages"]
    system = messages[0]["content"]
    user = messages[1]["content"]
    assistant = messages[2]["content"]

    return (
        f"<|system|>\n{system}\n"
        f"<|user|>\n{user}\n"
        f"<|assistant|>\n{assistant}"
    )

# ------------------------------------------------------------
# 6. Load dataset
# ------------------------------------------------------------
#
# Notebook version:
#
# dataset = load_dataset(
#     "json",
#     data_files={
#         "train": TRAIN_FILE,
#         "eval": EVAL_FILE,
#     },
# )
#
# def formatting_func(example):
#     return format_chat_example(example)
#
# print(dataset)

# ------------------------------------------------------------
# 7. Load tokenizer and model
# ------------------------------------------------------------
#
# tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
#
# if tokenizer.pad_token is None:
#     tokenizer.pad_token = tokenizer.eos_token
#
# model = AutoModelForCausalLM.from_pretrained(
#     BASE_MODEL,
#     load_in_4bit=True,
#     device_map="auto",
#     trust_remote_code=True,
# )
#
# model = prepare_model_for_kbit_training(model)

# ------------------------------------------------------------
# 8. Configure LoRA
# ------------------------------------------------------------
#
# lora_config = LoraConfig(
#     r=8,
#     lora_alpha=16,
#     lora_dropout=0.05,
#     bias="none",
#     task_type="CAUSAL_LM",
#     target_modules=[
#         "q_proj",
#         "k_proj",
#         "v_proj",
#         "o_proj",
#     ],
# )

# model = get_peft_model(model, lora_config)

# ------------------------------------------------------------
# 9. Training arguments
# ------------------------------------------------------------
#
# training_args = TrainingArguments(
#     output_dir=OUTPUT_DIR,
#     num_train_epochs=3,
#     per_device_train_batch_size=1,
#     per_device_eval_batch_size=1,
#     gradient_accumulation_steps=4,
#     learning_rate=2e-4,
#     logging_steps=5,
#     eval_strategy="epoch",
#     save_strategy="epoch",
#     save_total_limit=2,
#     fp16=True,
#     report_to="none",
# )

# ------------------------------------------------------------
# 10. Trainer
# ------------------------------------------------------------
#
# trainer = SFTTrainer(
#     model=model,
#     tokenizer=tokenizer,
#     train_dataset=dataset["train"],
#     eval_dataset=dataset["eval"],
#     formatting_func=formatting_func,
#     args=training_args,
#     max_seq_length=1024,
# )
#
# trainer.train()
# trainer.save_model(OUTPUT_DIR)
# tokenizer.save_pretrained(OUTPUT_DIR)

# ------------------------------------------------------------
# 11. Quick eval prompts
# ------------------------------------------------------------

QUICK_EVAL_PROMPTS = [
    {
        "id": "official_hive_ants",
        "prompt": "A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?",
    },
    {
        "id": "official_site_20_hives",
        "prompt": "An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?",
    },
    {
        "id": "short_heat_variant",
        "prompt": "Give a short field answer: bees cluster outside in hot weather, hive activity is low, and water is limited. What should be checked first?",
    },
]

# Notebook version after training:
#
# Path(QUICK_EVAL_OUT).parent.mkdir(parents=True, exist_ok=True)
#
# with open(QUICK_EVAL_OUT, "w", encoding="utf-8") as f:
#     for item in QUICK_EVAL_PROMPTS:
#         inputs = tokenizer(item["prompt"], return_tensors="pt").to(model.device)
#         outputs = model.generate(
#             **inputs,
#             max_new_tokens=180,
#             temperature=0.2,
#             top_p=0.9,
#             do_sample=True,
#         )
#         text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         f.write(json.dumps({
#             "id": item["id"],
#             "prompt": item["prompt"],
#             "output": text,
#         }, ensure_ascii=False) + "\n")
#
# print(f"Wrote quick eval outputs to {QUICK_EVAL_OUT}")

# ------------------------------------------------------------
# 12. Export notes
# ------------------------------------------------------------
#
# After training:
#
# 1. Download OUTPUT_DIR from the notebook.
# 2. Bring it back into the local repo under an ignored folder.
# 3. Convert or merge as needed.
# 4. Convert to GGUF.
# 5. Quantize to Q4_K_M.
# 6. Run llama.cpp locally.
# 7. Run ADTC profiler.
# 8. Run Step 5 benchmark again.
#
# Do not use this notebook or any cloud runtime during judged ADTC runtime.
