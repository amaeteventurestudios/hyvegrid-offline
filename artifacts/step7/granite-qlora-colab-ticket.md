# Granite QLoRA Colab Experiment Ticket

## Purpose

This ticket defines the first development-only GPU fine-tune experiment for HyveGrid Offline.

The goal is to test whether a small Granite QLoRA run improves HyveGrid field reasoning on public apiculture and agriculture examples.

This is not a model lock.

## Boundary

The notebook may use a GPU during development.

The judged ADTC runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

Do not use any notebook, hosted GPU, API, or cloud service during judged runtime.

## Base model

Use:

- ibm-granite/granite-3.3-2b-instruct

Reason:

- Granite is the current efficiency baseline.
- It used less RAM than Gemma in profiler smoke tests.
- It was faster than Gemma in profiler smoke tests.
- It is the first reasonable candidate for HyveGrid specialization.

## Dataset files

Upload these files into the notebook environment:

- data/finetune/splits/apiculture_train_split_chat.jsonl
- data/finetune/splits/apiculture_eval_split_chat.jsonl

Optional reference files:

- data/finetune/apiculture_qa_seed.jsonl
- artifacts/step7/dataset-coverage-report.md
- artifacts/step7/first-finetune-experiment-ticket.md
- artifacts/step7/tuned-model-import-export-checklist.md

## Expected data counts

Current expected counts:

- train: 52
- eval: 8

If counts differ, stop and check the dataset before training.

## Starting training settings

Use conservative values:

- method: QLoRA
- max sequence length: 1024
- LoRA rank: 8
- LoRA alpha: 16
- LoRA dropout: 0.05
- learning rate: 2e-4
- epochs: 3
- batch size: 1 or 2 depending on GPU memory
- gradient accumulation: 4 if batch size is 1
- save strategy: save at end and optionally each epoch
- eval strategy: eval each epoch
- logging: every few steps
- reporting: none

## Required quick eval prompts

Run these after training:

### Official prompt 1

A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?

Expected answer pattern:

- possible concern
- check ants entering hive vs near stand only
- check ant trails and stand contact points
- check colony strength
- check brood pattern, larvae, eggs, queen-right signs
- check food stores, pollen, water, heat stress, recent disturbance
- avoid harvesting immediately
- avoid spraying chemicals into or near hive
- avoid moving hive immediately unless safety requires it
- confirm by physical inspection

### Official prompt 2

An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?

Expected answer pattern:

- possible concern
- pesticide and herbicide risk from pepper and vegetable farms
- spray timing coordination
- dry-season water reliability
- backup clean water
- forage diversity and flowering seasonality
- mango is seasonal
- cassava should not be assumed to be enough forage
- shade, wind, heat, drainage, flooding
- human, livestock, road, path, school, and farm-worker safety
- access for inspection and harvest
- stage placement if uncertain

### Short heat prompt

Give a short field answer: bees cluster outside in hot weather, hive activity is low, and water is limited. What should be checked first?

Expected answer pattern:

- possible heat stress
- check shade, airflow, entrance blockage, water, direct sun, crowding, bearding
- avoid harvesting immediately
- avoid spraying water or chemicals into hive
- confirm by physical inspection

## Required outputs from notebook

Save or download:

- training log
- adapter folder, if adapter-only training
- merged model folder, if adapter was merged
- tokenizer/config files
- quick eval output JSONL
- short notes on GPU type and training settings

## Output storage

When brought back into the local repo, large training outputs must go under ignored local folders such as:

- artifacts/local-training-outputs/
- model/

Do not commit model weights, adapters, checkpoints, or GGUF files.

Commit only small text artifacts such as:

- training notes
- quick eval summaries
- benchmark reports
- model decision notes

## Local follow-up after notebook

After notebook training:

1. Bring adapter or merged model back locally.
2. Confirm files load.
3. Convert or merge if needed.
4. Convert to GGUF.
5. Quantize to Q4_K_M.
6. Run llama.cpp local tests.
7. Run ADTC profiler smoke test.
8. Run Step 5 official benchmark.
9. Run Step 7 eval split benchmark.
10. Compare against base Granite and Gemma.

## Accept or reject

Accept only if tuned model clearly improves field-answer quality and stays within runtime constraints.

Reject if it:

- memorizes examples but fails variants
- gives unsafe advice
- loses cautious language
- cannot convert to GGUF
- becomes too slow
- uses too much RAM
- requires cloud runtime for inference

## Current next action

Create the actual notebook or paste the existing notebook skeleton into a Colab/Kaggle GPU environment.

Do not start app, RAG, Yoruba, or UI work yet.
