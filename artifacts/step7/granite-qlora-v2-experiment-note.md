# Granite QLoRA V2 Experiment Note

## Status

Granite QLoRA V2 trained successfully in Google Colab on a Tesla T4 GPU.

This experiment is saved as local evidence but is not locked as the final scoring model.

## Runtime boundary

This was a development-only training experiment.

The judged ADTC runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

## Base model

- `ibm-granite/granite-3.3-2b-instruct`

## Training setup

- GPU: Tesla T4
- Train examples: 52
- Eval examples: 8
- Epochs: 3
- LoRA rank: 8
- LoRA alpha: 16
- Trainable parameters: 4,259,840
- Trainable percentage: 0.1679%

## Training outcome

The training run completed successfully.

Reported final metrics:

- train runtime: 135.2 seconds
- train loss: 2.048
- final eval loss: 1.448
- final eval mean token accuracy: 0.7162

## Quick eval review

### official_hive_ants

Output:

> Check if the hive is strong, inspect the entrance, and avoid removing frames or feeding without confirmation of strength. Confirm by physical inspection before taking action.

Review:

- Stable answer.
- No prompt repetition.
- Too shallow for final scoring.
- Missing ants trail checks, brood pattern, queen signs, food stores, water, spraying, moving, and harvesting cautions.

### official_site_20_hives

Output:

> First check: proximity to food sources (flowers, grasses), water availability, pesticide use, farming practices, shade, wind exposure, access, safety, and local regulations. Avoid placing hives in areas with high pesticide use, contaminated water, or unsafe access. Confirm by physical inspection before placement.

Review:

- Stable answer.
- No repeated tokens.
- Useful general structure.
- Too generic for final scoring.
- Missing crop-specific reasoning for cassava, mango, pepper, vegetables, seasonal water, dry-season reliability, and forage seasonality.

### short_heat_variant

Output:

> Check if there's enough food and water, ventilation, and shade. Avoid immediate roof repairs or sealing off the hive. Confirm by physical inspection before taking action.

Review:

- Usable field answer.
- Better than V1.
- Needs more precise heat-stress language.

## Decision

Do not lock Granite QLoRA V2 as the final model.

Save the adapter locally as a useful experiment artifact.

Do not convert to GGUF yet.

## Reason

V2 fixed the V1 repetition failure, but the answers are still too shallow for the official prompts.

The next model step should improve answer specificity before spending time on GGUF conversion and profiler testing.

## Local artifact location

The adapter and quick eval output are stored locally under:

`artifacts/local-training-outputs/granite-qlora-v2/`

This folder is ignored by git and must not be committed.

## Next recommendation

Prepare a V3 experiment with stronger apiculture-specific training examples and stricter answer formats for the two official prompt families.
