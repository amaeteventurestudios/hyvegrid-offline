# Granite LoRA Notebook Plan

## Purpose

This plan defines the first development-only fine-tune experiment for HyveGrid Offline.

The goal is to test whether the public 60-example HyveGrid apiculture dataset can improve Granite's field reasoning without breaking the ADTC runtime path.

This is not a model lock.

## Runtime boundary

Training may happen in a development-only GPU notebook.

The judged runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

## Base model

Primary base model:

- ibm-granite/granite-3.3-2b-instruct

Reason:

- Current HyveGrid efficiency baseline.
- Lower RAM than Gemma in profiler smoke testing.
- Faster than Gemma in profiler smoke testing.
- Small enough for a controlled LoRA or QLoRA experiment.

## Training method

Preferred first method:

- QLoRA

Reason:

- Lower VRAM requirement than full fine-tuning.
- Suitable for a small experiment on a 2B model.
- Good first test before investing in larger data or longer training.

## Development environment

Acceptable development-only options:

- Google Colab with NVIDIA GPU
- Kaggle notebook with NVIDIA GPU
- rented NVIDIA GPU instance

Do not use any cloud service during judged runtime.

## Data files to upload to notebook

Upload:

- data/finetune/splits/apiculture_train_split_chat.jsonl
- data/finetune/splits/apiculture_eval_split_chat.jsonl

Optional for reference:

- data/finetune/apiculture_qa_seed.jsonl
- artifacts/step7/dataset-coverage-report.md
- artifacts/step7/first-finetune-experiment-ticket.md

## Notebook steps

1. Install training dependencies.
2. Load Granite-3.3-2B-Instruct.
3. Load train split.
4. Load eval split.
5. Apply LoRA or QLoRA adapter.
6. Train for a small number of steps.
7. Save adapter or merged checkpoint.
8. Run quick eval prompts inside notebook.
9. Export tuned model files.
10. Bring output back to local repo.
11. Convert to GGUF.
12. Quantize to Q4_K_M.
13. Run llama.cpp local test.
14. Run ADTC profiler smoke test.
15. Run Step 5 official prompt benchmark.
16. Run Step 7 eval split benchmark.
17. Compare against baseline Granite and Gemma.

## Starting hyperparameters

Use conservative starting values:

- max sequence length: 1024
- LoRA rank: 8
- LoRA alpha: 16
- LoRA dropout: 0.05
- learning rate: 2e-4
- epochs: 3
- batch size: small, based on GPU memory
- gradient accumulation: use if batch size is small

These are starting values only. Do not lock them until the first run is evaluated.

## Success criteria

The tuned model must improve over base Granite on:

- Official prompt 1, hive activity and ants.
- Official prompt 2, 20 hives near farms.
- Held-out Step 7 eval split.
- Safety language.
- Avoid-action guidance.
- Field triage usefulness.

The tuned model must also remain:

- convertible to GGUF
- quantizable to Q4_K_M
- usable with llama.cpp
- safe under RAM constraints
- fully offline at judged runtime

## Reject criteria

Reject the tuned candidate if it:

- Memorizes examples but fails variants.
- Gives unsafe pesticide, harvest, disease, or hive-moving advice.
- Stops giving cautious language.
- Loses broader agriculture usefulness.
- Cannot convert to GGUF.
- Is slower or larger without a clear accuracy gain.
- Requires cloud runtime for inference.

## Files expected after successful training

Expected development outputs:

- adapter directory, if using adapter-only save
- merged model directory, if merging adapter into base
- training log
- quick eval output

Expected local repo outputs later:

- tuned GGUF model file, ignored by git
- profiler JSON artifact
- official prompt benchmark artifact
- eval split benchmark artifact
- model decision note

## Next action after this plan

Create the notebook skeleton.

Do not start app, RAG, Yoruba, or UI work yet.
