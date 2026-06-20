# HyveGrid Offline Notebooks

## Purpose

This folder contains development-only notebook scripts for HyveGrid Offline.

These files are used for experimentation, training preparation, and model improvement work.

They are not part of the judged ADTC offline runtime.

## Runtime boundary

The final judged runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

A notebook may be used during development to fine-tune or test a model, but the submitted runtime cannot depend on Colab, Kaggle, hosted GPUs, APIs, or cloud services.

## Current notebook scripts

- `granite_qlora_hyvegrid.py`

This script is a development-only skeleton for a Granite QLoRA fine-tune experiment using the public HyveGrid apiculture dataset.

## Data inputs

Expected training files:

- `data/finetune/splits/apiculture_train_split_chat.jsonl`
- `data/finetune/splits/apiculture_eval_split_chat.jsonl`

## Expected development outputs

A successful development experiment may produce:

- LoRA adapter files
- merged model checkpoint
- quick eval outputs
- training logs

These outputs must be reviewed before any model is accepted.

## Final model path

After training, a candidate model must be:

1. brought back into the local repo environment
2. converted to GGUF
3. quantized, likely Q4_K_M first
4. tested with llama.cpp
5. profiled with ADTC profiler
6. benchmarked on official and eval prompts
7. accepted or rejected based on evidence

## Important restriction

Do not start app, RAG, Yoruba, or UI work from this folder.

This folder is only for development-time model experiments.
