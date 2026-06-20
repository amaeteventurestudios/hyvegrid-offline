# Step 7 Fine-Tune Experiment Plan

## Purpose

Step 5 showed that the tested base models were not accurate enough on the official HyveGrid Offline field prompts.

Step 6 decided not to lock a base model yet.

Step 7 prepares a public, challenge-safe apiculture dataset for a small fine-tune experiment.

## Current baseline

Granite-3.3-2B-Instruct Q4_K_M remains the efficiency baseline because it performed better than Gemma on profiler telemetry.

Gemma remains a quality reference, but it is slower.

## Current dataset

Source dataset:

- data/finetune/apiculture_qa_seed.jsonl

Current count:

- 20 public apiculture QA examples

Generated chat dataset:

- data/finetune/apiculture_train_chat.jsonl

## Experiment rule

Do not train blindly.

Before fine-tuning, split the dataset into train and eval files.

The train file is used for model learning.

The eval file is used to check whether the tuned model learned useful field reasoning without only memorizing the examples.

## Success criteria

A tuned candidate must beat the current base models on:

- The two official HyveGrid prompts.
- The held-out Step 7 eval split.
- The proxy validation prompt set.
- Safety and caution language.
- Profiler RAM and throughput constraints.

## Safety and IP boundary

The dataset must stay public and challenge-safe.

Allowed:

- Public apiculture guidance.
- Public extension-style reasoning.
- Manual observation scenarios.
- Sample edge-signal style inputs.
- Cautious field triage answers.

Excluded:

- Proprietary hardware plans.
- Sensor IP.
- Firmware strategy.
- Private field records.
- Honey Flow Africa internal strategy.
- Partner strategy.
- Commercial roadmap.
- Investor materials.
- Patent-sensitive claims.

## Step 7 immediate next step

Create a deterministic train/eval split from the 20-example seed dataset.

Then expand the dataset beyond 20 examples before a serious fine-tune run.
