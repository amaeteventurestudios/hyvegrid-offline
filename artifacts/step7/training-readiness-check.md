# Step 7 Training Readiness Check

## Purpose

This file records what must be true before running the first fine-tune experiment.

The goal is not to train blindly. The goal is to test whether a small public HyveGrid apiculture dataset can improve the model's own field reasoning.

## Current dataset

- Source examples: 60
- Train examples: 52
- Eval examples: 8

## Current baseline

Primary efficiency baseline:

- Granite-3.3-2B-Instruct Q4_K_M

Quality reference:

- Gemma-2-2B-it Q4_K_M

## First training target

Train a small adapter or tuned checkpoint against Granite first, if license and tooling are workable.

Granite is chosen first because it is the current efficiency baseline.

## Readiness checklist

Before training:

- [ ] Confirm machine architecture.
- [ ] Confirm Python version.
- [ ] Confirm available disk space.
- [ ] Confirm whether local fine-tuning is realistic.
- [ ] Confirm Granite license allows this use.
- [ ] Confirm training route: local, Colab, Kaggle, or other development-only environment.
- [ ] Confirm output can be converted to GGUF.
- [ ] Confirm runtime remains llama.cpp and offline.
- [ ] Confirm no private data or proprietary IP enters the dataset.

## Machine check command

Run:

uname -m
sw_vers
python3 --version
sysctl -n machdep.cpu.brand_string 2>/dev/null || true
sysctl -n hw.memsize 2>/dev/null || true
df -h .

## Decision rule

If local training is not realistic, use a development-only training environment, then bring the tuned model back, convert it to GGUF, quantize it, and run locally offline.

The final judged runtime must still be local, offline, GGUF, and llama.cpp.

## Do not proceed if

- Training requires cloud runtime during judging.
- The model cannot be converted to GGUF.
- The tuned model is larger or slower without a clear accuracy gain.
- The tuned model gives unsafe hive, pesticide, harvest, or disease guidance.
- The dataset includes private field records, hardware IP, partner strategy, or Honey Flow Africa internal material.
