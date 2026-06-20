# Granite QLoRA V3 Experiment Note

## Status

Granite QLoRA V3 trained successfully in Google Colab on a Tesla T4 GPU.

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
- Train examples: 61
- Eval examples: 11
- Epochs: 3
- LoRA rank: 8
- LoRA alpha: 16
- Trainable parameters: 4,259,840
- Trainable percentage: 0.1679%

## Training outcome

The training run completed successfully.

Reported final metrics:

- train runtime: 153.4 seconds
- train loss: 1.948
- final eval loss: 1.454
- final eval mean token accuracy: 0.6979

## Quick eval review

### official_hive_ants

Output:

> Check first: whether the colony is strong or weak, whether the queen is present, and whether there's enough food and water. Avoid immediately removing the hive stand or spraying pesticides. Confirm by physical inspection before taking action.

Review:

- Stable answer.
- No prompt repetition.
- Better than V1.
- Still too shallow for final scoring.
- Missing ants entering vs near stand, ant trails, stand contact points, brood pattern, eggs or young larvae, harvesting caution, and movement caution.

### official_site_20_hives

Output:

> First check: proximity to food sources (flowers, grasses), water, shade, pesticide risk, farming practices, and potential competition from other beekeepers. Avoid placing hives near contaminated water or pesticides. Check for flowering times and forage availability. Confirm by physical inspection before placement.

Review:

- Stable answer.
- No repeated tokens.
- Still too generic.
- Missing cassava, mango, pepper, vegetables, seasonal water, dry-season reliability, backup water, spray timing, and staged placement.

### short_heat_variant

Output:

> Check whether the colony has enough food, water, ventilation, brood, pollen, and adult bees. Avoid removing brood or feeding too early. Confirm by physical inspection before taking action.

Review:

- Stable but not enough heat-stress specificity.
- Missing bearding, shade, direct sun, airflow, entrance blockage, and avoid sealing/spraying/harvesting.

## Decision

Do not lock Granite QLoRA V3 as the final model.

Save the adapter locally as a useful experiment artifact.

Do not convert to GGUF yet.

## Reason

V3 trained successfully and used stronger official-family examples, but the quick eval did not clearly beat V2.

The model still compresses answers into generic safety summaries instead of preserving enough apiculture-specific detail.

## Local artifact location

The adapter and quick eval output are stored locally under:

`artifacts/local-training-outputs/granite-qlora-v3/`

This folder is ignored by git and must not be committed.

## Next recommendation

Stop repeating the same Granite QLoRA strategy for now.

Next model step should test either:

1. a stronger prompt/evaluation wrapper on the existing base Granite model, or
2. a different small base model with better instruction-following before more fine-tuning.

The model remains unlocked.
