# Granite QLoRA Colab/Kaggle Runbook

## Purpose

This runbook explains how to use the local upload bundle for the first HyveGrid Offline Granite QLoRA experiment.

This is a development-only training run.

The judged ADTC runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

## Local upload bundle

Bundle path:

artifacts/step7/granite-qlora-upload-bundle.zip

This ZIP is ignored by git and should not be committed.

## Files inside the bundle

The bundle includes:

- notebooks/granite_qlora_colab_runtime.py
- data/finetune/splits/apiculture_train_split_chat.jsonl
- data/finetune/splits/apiculture_eval_split_chat.jsonl
- data/finetune/apiculture_qa_seed.jsonl
- artifacts/step7/granite-qlora-colab-ticket.md
- artifacts/step7/granite-lora-notebook-plan.md
- artifacts/step7/tuned-model-import-export-checklist.md
- artifacts/step7/dataset-coverage-report.md

## Colab/Kaggle steps

1. Open a GPU notebook environment.
2. Upload `granite-qlora-upload-bundle.zip`.
3. Unzip it inside the notebook.
4. Open or paste the contents of:

   notebooks/granite_qlora_colab_runtime.py

5. Install dependencies in the notebook.
6. Confirm the dataset counts:

   - train: 52
   - eval: 8

7. Run the training script.
8. Save the output folder:

   hyvegrid-granite-lora

9. Save the quick eval file:

   hyvegrid-granite-lora-quick-eval.jsonl

## Required quick eval checks

After training, review whether the model improves on:

- official_hive_ants
- official_site_20_hives
- short_heat_variant

A useful answer should include:

- cautious language
- what to check first
- what to avoid immediately
- physical inspection when needed
- no unsafe pesticide, harvest, disease, or hive-moving advice

## Files to download after notebook run

Download:

- hyvegrid-granite-lora/
- hyvegrid-granite-lora-quick-eval.jsonl
- any training log
- any notebook output summary

## Local storage after download

Place downloaded outputs under:

artifacts/local-training-outputs/

Do not commit:

- model weights
- adapter files
- checkpoints
- GGUF files
- ZIP bundles

Commit only small text summaries, benchmark reports, and decision notes.

## Local follow-up after download

After the notebook run:

1. Save quick eval output locally.
2. Review quick eval quality.
3. Decide whether the adapter is worth converting.
4. If worth converting, merge adapter if needed.
5. Convert merged model to GGUF.
6. Quantize to Q4_K_M.
7. Run llama.cpp local tests.
8. Run ADTC profiler smoke test.
9. Rerun official prompt benchmark.
10. Compare against base Granite and Gemma.

## Stop condition

Stop and reject the experiment if the tuned model:

- gives unsafe advice
- fails the two official prompts
- loses cautious language
- cannot be converted to GGUF
- requires cloud inference
- becomes too slow or too large
