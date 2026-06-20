# HyveGrid Offline - Granite QLoRA Runtime Script
#
# Development-only GPU training script.
#
# Do not use this during judged ADTC runtime.
# Judged runtime must remain offline, local, GGUF, and llama.cpp.
#
# Expected uploaded files in notebook:
# - data/finetune/splits/apiculture_train_split_chat.jsonl
# - data/finetune/splits/apiculture_eval_split_chat.jsonl
#
# Colab/Kaggle install cell:
# !pip install -U transformers datasets accelerate peft trl bitsandbytes sentencepiece

import json
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer

BASE_MODEL = "ibm-granite/granite-3.3-2b-instruct"

TRAIN_FILE = "data/finetune/splits/apiculture_train_split_chat.jsonl"
EVAL_FILE = "data/finetune/splits/apiculture_eval_split_chat.jsonl"

OUTPUT_DIR = "hyvegrid-granite-lora"
QUICK_EVAL_OUT = "hyvegrid-granite-lora-quick-eval.jsonl"

MAX_SEQ_LENGTH = 1024

def count_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())

print("GPU available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))

print("Train examples:", count_jsonl(TRAIN_FILE))
print("Eval examples:", count_jsonl(EVAL_FILE))

assert count_jsonl(TRAIN_FILE) == 52, "Expected 52 train examples"
assert count_jsonl(EVAL_FILE) == 8, "Expected 8 eval examples"

def format_chat_example(example):
    messages = example["messages"]
    system = messages[0]["content"]
    user = messages[1]["content"]
    assistant = messages[2]["content"]

    return (
        f"<|system|>\n{system}\n"
        f"<|user|>\n{user}\n"
        f"<|assistant|>\n{assistant}"
    )

dataset = load_dataset(
    "json",
    data_files={
        "train": TRAIN_FILE,
        "eval": EVAL_FILE,
    },
)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_4bit=True,
    device_map="auto",
    trust_remote_code=True,
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=5,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    fp16=True,
    report_to="none",
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset["train"],
    eval_dataset=dataset["eval"],
    formatting_func=format_chat_example,
    args=training_args,
    max_seq_length=MAX_SEQ_LENGTH,
)

trainer.train()

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

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

Path(QUICK_EVAL_OUT).parent.mkdir(parents=True, exist_ok=True)

model.eval()

with open(QUICK_EVAL_OUT, "w", encoding="utf-8") as f:
    for item in QUICK_EVAL_PROMPTS:
        prompt = item["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=220,
                temperature=0.2,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        f.write(json.dumps({
            "id": item["id"],
            "prompt": prompt,
            "output": text,
        }, ensure_ascii=False) + "\n")

print(f"Saved adapter/model output to: {OUTPUT_DIR}")
print(f"Saved quick eval outputs to: {QUICK_EVAL_OUT}")

print("")
print("Next local steps after downloading outputs:")
print("1. Place output under artifacts/local-training-outputs/ or model/, ignored by git.")
print("2. Merge adapter if needed.")
print("3. Convert to GGUF.")
print("4. Quantize to Q4_K_M.")
print("5. Run llama.cpp local test.")
print("6. Run ADTC profiler.")
print("7. Rerun official prompt benchmark.")
