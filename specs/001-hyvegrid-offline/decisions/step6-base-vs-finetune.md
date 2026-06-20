# Step 6 Decision: Base Model vs Fine-Tune

## Decision

Do not lock the current base models.

Move toward public apiculture specialization and fine-tune preparation.

## Evidence

Gemma-2-2B-it Q4_K_M and Granite-3.3-2B-Instruct Q4_K_M were compared on the two official HyveGrid Offline ADTC prompts.

Both models scored 3.5 / 10 on the official-prompt smoke benchmark.

## Why base models are not enough

The models gave generic beekeeping answers but missed important HyveGrid field-reasoning details:

- Avoid harvesting immediately.
- Avoid spraying chemicals into or near the hive.
- Confirm by physical inspection.
- Check whether ants are only near the stand or entering the hive.
- Check colony strength, adult bee population, brood pattern, larvae, eggs, and queen-right signs.
- Check food stores, pollen, water stress, heat stress, and recent disturbance.
- Check pesticide and herbicide risk from nearby farms.
- Check seasonal water reliability and backup water.
- Evaluate forage diversity and flowering gaps.
- Avoid assuming cassava is enough forage.
- Check human, livestock, road, school, drainage, shade, wind, and access risks.
- Consider staged placement for 20 hives.

## Baseline model

Granite-3.3-2B-Instruct Q4_K_M remains the efficiency baseline because it has better profiler performance than Gemma.

## Fine-tune direction

Build a public, challenge-safe apiculture QA/checklist dataset.

Allowed content:

- Public apiculture notes.
- Public extension-style guidance.
- Cleaned field scenarios.
- Cautious next-step answers.
- Manual observations and sample edge-signal inputs.

Excluded content:

- Proprietary hardware plans.
- Sensor IP.
- Firmware strategy.
- Private field data.
- Partner strategy.
- Honey Flow Africa internal strategy.
- Commercial roadmap.
- Investor materials.
- Patent-sensitive claims.

## Acceptance criteria before fine-tuning

A tuned candidate must beat the baseline models on:

- The two official prompts.
- The proxy validation prompt set.
- Safety and caution language.
- Profiler RAM and throughput constraints.

## Step 6 outcome

Proceed to public apiculture dataset preparation.

Do not start app, RAG, Yoruba, or UI implementation until the scoring model path has a stronger candidate.
