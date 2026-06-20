# Step 7 Dataset Coverage Report

## Summary

- Source examples: 60
- Train examples: 52
- Eval examples: 8

## Category coverage

| Category | Count |
|---|---:|
| agriculture_mcq | 4 |
| forage_pollination | 5 |
| general_agriculture | 6 |
| harvest_quality | 6 |
| hive_health | 9 |
| hive_management | 2 |
| hive_signal_check | 4 |
| pest_pressure | 3 |
| pesticide_risk | 3 |
| post_harvest | 2 |
| short_answer | 4 |
| site_readiness | 12 |

## Answer-style checks

| Check | Count |
|---|---:|
| Uses cautious language, such as possible concern | 60 |
| Includes avoid / do not guidance | 57 |
| Mentions inspection or physical inspection | 32 |
| Mentions experienced beekeeper or extension officer | 4 |

## Current read

The dataset now covers hive health, site readiness, pest pressure, pesticide risk, harvest quality, forage and pollination, hive signal checks, and hive management.

Before fine-tuning, review whether the dataset needs more examples for:

- General agriculture prompts beyond bees.
- More multiple-choice style agriculture reasoning.
- More site-readiness variations.
- More official-prompt variants.
- More short-answer responses, because the model benchmark may limit tokens.

## Next recommendation

Do not train yet. First decide whether to expand from 40 to 60 examples or create a small first fine-tune experiment plan.
