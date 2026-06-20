# HyveGrid Offline - Granite QLoRA Runtime Script V2
#
# Development-only GPU training script.
# Judged runtime must remain offline, local, GGUF, and llama.cpp.

import json
from pathlib import Path

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, prepare_model_for_kbit_training, get_peft_model
from trl import SFTTrainer, SFTConfig

BASE_MODEL = "ibm-granite/granite-3.3-2b-instruct"

TRAIN_FILE = "data/finetune/splits/apiculture_train_split_chat.jsonl"
EVAL_FILE = "data/finetune/splits/apiculture_eval_split_chat.jsonl"

OUTPUT_DIR = "hyvegrid-granite-lora-v2"
QUICK_EVAL_OUT = "hyvegrid-granite-lora-v2-quick-eval.jsonl"

MAX_SEQ_LENGTH = 1024

SYSTEM_PROMPT = (
    "You are HyveGrid Offline, a cautious offline apiculture field assistant. "
    "Give practical field triage for beekeepers and extension workers. "
    "Use short structured answers. Include what to check first, what to avoid doing immediately, "
    "and remind the user to confirm by physical inspection when needed. "
    "Do not give certified disease diagnosis."
)

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

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def render_chat(messages, add_generation_prompt=False):
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=add_generation_prompt,
        )
    except Exception:
        rendered = []
        for message in messages:
            role = message.get("role", "user").upper()
            content = message.get("content", "")
            rendered.append(f"{role}:\n{content}")
        if add_generation_prompt:
            rendered.append("ASSISTANT:\n")
        return "\n\n".join(rendered)

def format_chat_example(example):
    return render_chat(example["messages"], add_generation_prompt=False)

dataset = load_dataset(
    "json",
    data_files={
        "train": TRAIN_FILE,
        "eval": EVAL_FILE,
    },
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.float16,
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

model = get_peft_model(model, lora_config)

for name, param in model.named_parameters():
    if param.requires_grad:
        param.data = param.data.float()

model.print_trainable_parameters()

print("Trainable parameter dtypes:")
_seen_dtypes = set()
for name, param in model.named_parameters():
    if param.requires_grad:
        _seen_dtypes.add(str(param.dtype))
print(sorted(_seen_dtypes))

if hasattr(model, "config"):
    model.config.use_cache = False

training_args = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    optim="paged_adamw_8bit",
    logging_steps=5,
    eval_strategy="epoch",
    save_strategy="epoch",
    save_total_limit=2,
    fp16=False,
    bf16=False,
    report_to="none",
    max_length=MAX_SEQ_LENGTH,
    packing=False,
    max_grad_norm=0.0,
)

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,
    train_dataset=dataset["train"],
    eval_dataset=dataset["eval"],
    formatting_func=format_chat_example,
    args=training_args,
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

model.eval()

def generate_answer(prompt):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    rendered_prompt = render_chat(messages, add_generation_prompt=True)
    inputs = tokenizer(rendered_prompt, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[-1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=220,
            do_sample=False,
            repetition_penalty=1.08,
            no_repeat_ngram_size=6,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    new_tokens = outputs[0][input_len:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

with open(QUICK_EVAL_OUT, "w", encoding="utf-8") as f:
    for item in QUICK_EVAL_PROMPTS:
        answer = generate_answer(item["prompt"])

        f.write(json.dumps({
            "id": item["id"],
            "prompt": item["prompt"],
            "output": answer,
        }, ensure_ascii=False) + "\n")

print(f"Saved adapter/model output to: {OUTPUT_DIR}")
print(f"Saved quick eval outputs to: {QUICK_EVAL_OUT}")
