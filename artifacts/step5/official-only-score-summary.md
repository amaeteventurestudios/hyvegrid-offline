# HyveGrid Offline Step 5 Official Prompt Score Summary

Date: 2026-06-20

## Scope

This benchmark compared Gemma-2-2B-it Q4_K_M and Granite-3.3-2B-Instruct Q4_K_M on the two official HyveGrid Offline ADTC test prompts.

This was an official-prompt accuracy smoke comparison, not a full model lock.

## Scores

| Prompt ID | Gemma /5 | Granite /5 | Winner | Notes |
|---|---:|---:|---|---|
| official_hive_ants | 1.5 | 2.0 | Granite | Gemma focused on ants but missed core avoid actions. Granite mentioned disease, food, queen issues, and parasites, but still missed the required immediate avoid guidance. |
| official_site_20_hives | 2.0 | 1.5 | Gemma | Gemma correctly led with pesticide/herbicide risk. Granite used a questionable fixed-distance crop claim and missed core site-readiness factors. |
| **Total** | **3.5 / 10** | **3.5 / 10** | Tie | Neither model is accurate enough to lock. |

## Interpretation

Granite remains the telemetry leader because it is faster and lighter.

Gemma showed slightly better site-readiness direction because it identified pesticide and herbicide risk, but it is still incomplete.

Both base models missed too many required HyveGrid field-reasoning points, including:

- Avoid harvesting immediately.
- Avoid spraying chemicals into or near the hive.
- Confirm by physical inspection.
- Check colony strength, brood pattern, queen-right signs, food stores, water stress, heat stress, and recent disturbance.
- Check water reliability through dry periods.
- Evaluate forage seasonality, mango seasonality, and cassava limitations.
- Check human, livestock, road, school, drainage, shade, wind, access, and staged-placement risks.

## Step 5 decision

Do not lock either base model.

Move Step 6 toward public apiculture specialization and fine-tune preparation.

## Step 6 working direction

Use Granite as the current efficiency baseline because it has better profiler performance.

Use the Step 5 failures to design a public apiculture QA/checklist dataset.

Fine-tuning should happen only if the public dataset can improve official-prompt and proxy-prompt accuracy without breaking RAM and throughput constraints.
