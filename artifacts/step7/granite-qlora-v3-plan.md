# Granite QLoRA V3 Plan

## Purpose

V3 strengthens the training set around the official prompt families before another Colab training run.

## Why V3 is needed

Granite QLoRA V2 trained successfully and fixed V1 repetition, but the quick eval answers were too shallow for the official hive-health and site-readiness prompts.

## V3 dataset change

A supplement file was added:

`data/finetune/v3/official_prompt_family_supplement_chat.jsonl`

It adds focused examples for:

- low hive activity with ants near the hive stand
- partially capped brood and normal smell
- what to check first
- what to avoid doing immediately
- site readiness near cassava, mango, pepper, vegetable farms, and seasonal water
- pesticide risk
- dry-season water reliability
- forage seasonality
- heat stress and water limitation

## V3 generated files

- `data/finetune/v3/apiculture_v3_train_chat.jsonl`
- `data/finetune/v3/apiculture_v3_eval_chat.jsonl`

## Acceptance target

V3 should produce answers that are more specific than V2 while avoiding prompt repetition.

Minimum expected answer content:

### Hive ants prompt

- possible concern
- ants entering hive vs near stand only
- ant trails and stand contact points
- colony strength
- brood pattern
- eggs or young larvae
- queen-right signs
- food stores
- water, shade, heat, recent disturbance
- avoid spraying chemicals
- avoid harvesting immediately
- avoid moving hive immediately unless safety requires
- confirm by physical inspection

### Site 20 hives prompt

- pesticide and herbicide risk
- pepper and vegetable farm spray timing
- water reliability in dry season
- backup clean water
- forage seasonality
- mango is seasonal
- cassava is not enough by itself
- shade, wind, heat, drainage, flooding
- human, livestock, road, path, and access safety
- stage placement if uncertain

## Decision rule

Do not convert V3 to GGUF unless quick eval beats V2 clearly.
