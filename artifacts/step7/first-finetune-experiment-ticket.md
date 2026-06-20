# Step 7 First Fine-Tune Experiment Ticket

## Goal

Run a small, controlled fine-tune experiment to test whether the public HyveGrid apiculture dataset improves the model's own field reasoning.

This experiment is not a model lock.

## Why this experiment exists

Step 5 showed that Gemma and Granite both scored 3.5 / 10 on the two official HyveGrid prompts.

Step 6 decided not to lock either base model.

Step 7 created a 60-example public, challenge-safe dataset with:

- 52 train examples
- 8 held-out eval examples

## Base candidate

Primary candidate:

- Granite-3.3-2B-Instruct

Reason:

- Better profiler efficiency than Gemma
- Lower peak RAM
- Faster than Gemma
- Good candidate for a small specialization experiment

Quality reference:

- Gemma-2-2B-it Q4_K_M

Reason:

- Sometimes stronger field direction
- Slower and larger than Granite

## Training data

Train file:

- data/finetune/splits/apiculture_train_split_chat.jsonl

Eval file:

- data/finetune/splits/apiculture_eval_split_chat.jsonl

Full generated chat file:

- data/finetune/apiculture_train_chat.jsonl

Source QA file:

- data/finetune/apiculture_qa_seed.jsonl

## Success criteria

The tuned candidate must beat the baseline model on:

1. The two official HyveGrid prompts.
2. The Step 7 held-out eval split.
3. The proxy validation prompt set.
4. Safety and caution language.
5. No unsafe beekeeping guidance.
6. RAM and throughput after GGUF conversion and quantization.

## Failure criteria

Reject the tuned candidate if it:

- Memorizes training examples but fails variants.
- Gives unsafe pesticide, harvest, disease, or hive-moving advice.
- Loses general agriculture usefulness.
- Becomes too slow.
- Uses too much RAM.
- Cannot be converted cleanly to GGUF.
- Requires cloud access at runtime.

## Runtime requirements after tuning

The final model must still be:

- GGUF
- llama.cpp compatible
- Offline
- Quantized, likely Q4_K_M first
- Compatible with ADTC Standard Laptop constraints

## Experiment sequence

1. Confirm base model license and local training feasibility.
2. Choose training method.
3. Train a small adapter or tuned checkpoint.
4. Merge if needed.
5. Convert to GGUF.
6. Quantize to Q4_K_M.
7. Run profiler smoke test.
8. Run Step 5 official prompt benchmark.
9. Run Step 7 eval split benchmark.
10. Compare against Gemma and Granite baselines.
11. Decide whether to continue, expand data, or reject.

## Current decision

Do not start UI, RAG, Yoruba, or web app work until the tuned model path is tested.

The current task is still the model brain.
