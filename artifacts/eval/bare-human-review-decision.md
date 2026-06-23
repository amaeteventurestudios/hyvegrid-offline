# HyveGrid Offline Bare Human Review Decision

## Source artifacts

* `artifacts/eval/bare-human-review.md`
* `artifacts/eval/comparison.md`
* `artifacts/eval/scoring_sheet.csv`

## Automated first-pass result

* Granite keyword score: 84.8%
* Qwen keyword score: 81.8%
* Granite projected score: 75.92
* Qwen projected score: 86.11

The keyword score made Qwen look stronger because Qwen has better telemetry, but keyword scoring is only a first pass.

## Human-review finding

Human review finds that Granite gives safer, more relevant apiculture field guidance overall.

Key findings:

1. Qwen's site-readiness answer is over-credited by keyword scoring because it includes irrelevant hazards such as earthquakes, tsunamis, poaching, illegal mining, and generic infrastructure risks instead of focused apiary placement reasoning.
2. Qwen's harvest-quality answer is a serious false positive because it says to harvest uncapped nectar frames and brood frames, which conflicts with honey quality and colony welfare.
3. Qwen's pest-pressure answer suggests insecticides or baits as immediate management, which conflicts with the non-destructive and cautious-action framing.
4. Granite is not perfect, but it more consistently gives inspection-first, colony-welfare-first, and field-practical guidance.

## Human score estimate

| Prompt                | Granite human score | Qwen human score | Notes                                                 |
| --------------------- | ------------------: | ---------------: | ----------------------------------------------------- |
| hive-triage-01        |             2.5 / 3 |          1.5 / 3 | Granite safer and more practical                      |
| site-readiness-01     |               4 / 5 |            2 / 5 | Qwen keyword score inflated by irrelevant hazard list |
| hive-health-02        |             2.5 / 3 |            2 / 3 | Granite slightly stronger                             |
| pest-pressure-02      |             2.5 / 3 |            1 / 3 | Qwen recommends risky chemical action                 |
| heat-stress-01        |             2.5 / 3 |            2 / 3 | Granite slightly stronger                             |
| harvest-quality-01    |               3 / 3 |            1 / 3 | Qwen fails on brood/uncapped nectar guidance          |
| forage-pollination-01 |               3 / 3 |            2 / 3 | Granite stronger on pesticide and forage risk         |
| site-readiness-02     |               3 / 3 |          2.5 / 3 | Both acceptable, Granite cleaner                      |
| pesticide-risk-01     |               3 / 3 |            2 / 3 | Granite stronger                                      |
| water-site-01         |             2.5 / 4 |            3 / 4 | Qwen slightly better here                             |

Totals:

* Granite: 28.5 / 33 = 86.4%
* Qwen: 19 / 33 = 57.6%

Projected human-adjusted score:

* Granite: 0.5 × 86.4 + 33.5 = 76.7
* Qwen: 0.5 × 57.6 + 45.2 = 74.0

## Decision

Do not lock Qwen as the scoring model based only on telemetry.

Granite remains the current accuracy-first candidate after human review.

## Next action

Evaluate challenger models before final model lock:

1. Phi-4-mini-instruct GGUF Q4_K_M
2. NVIDIA Nemotron 3 Nano 4B GGUF Q4_K_M, only if RAM and TPS are acceptable

Then compare all challengers against Granite using the same harness and human-review process.
