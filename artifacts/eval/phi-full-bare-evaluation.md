# Phi-4 Mini Instruct Full Bare Evaluation

## Candidate

* Model ID: `phi-4-mini-instruct-q4-k-m`
* GGUF filename: `Phi-4-mini-instruct-Q4_K_M.gguf`
* Source repo: `unsloth/Phi-4-mini-instruct-GGUF`
* Quantization: Q4_K_M

## Run status

* Branch: `phase-1-eval-harness`
* Commit tested: `0a59614fb3cad138e31734f87fdbe6d66f3e41a7`
* Phi raw outputs: 10
* Missing outputs: 0
* Failures or timeouts: none
* All 10 bare prompts completed: yes

The two smoke-test outputs were retained. The remaining eight prompts were completed in four resumable chunks of no more than two runs each. Granite and Qwen were not rerun.

## Automated keyword result

* Phi bare keyword score: 81.8%
* Projected score: pending, because Phi telemetry formula is not yet locked into scoring

Keyword scoring is only a first pass. The 81.8% result does not resolve correctness, safety, relevance, or false keyword hits.

## First-read quality notes

These notes are a preliminary comparison with the Granite human-review decision, not a completed human score.

* **Hive triage caution:** Phi appropriately cautions against immediate strong chemical treatment, but it prematurely centers Varroa, makes an unsupported connection between ants and Varroa, and then suggests oxalic or formic acid before giving a sufficiently broad inspection checklist. It misses colony strength, food stores, and a fuller brood assessment. Granite appears more inspection-first and field-practical on this prompt.
* **Site readiness relevance:** Phi identifies pesticide exposure, crop and forage seasonality, water access, neighboring farms, weather, and farm practices. It is relevant overall, but it does not clearly address dry-season water backup, spray coordination, people or livestock safety, access, drainage, or whether local forage can support 20 colonies.
* **Pest pressure safety:** This is Phi's weakest area on first read. It incorrectly suggests that small beetles could be Varroa mites and moves quickly to acaricides rather than prioritizing identification, colony-strength assessment, sanitation, and non-destructive physical barriers. This is less cautious than Granite's overall inspection-first pattern.
* **Harvest quality and colony welfare:** Phi correctly says brood should not be harvested, but it also advises harvesting uncapped nectar frames, temporary storage, filtering, and pasteurization. That guidance risks unripe honey quality and conflicts with the safer approach of leaving uncapped nectar for further ripening. The automated 100% prompt score therefore appears over-generous.
* **Pesticide coordination:** Phi gives useful coordination guidance on application timing, product toxicity, drift distance, monitoring, and communication. It does not explicitly emphasize following the product label or consulting local extension guidance, so the answer remains incomplete.
* **Forage seasonality:** Phi clearly recommends diverse forage, flowering calendars, identifying forage gaps, pollination needs, and competition with other pollinators. It is useful but does not foreground nearby pesticide coordination.
* **Water, wind, shade, and drainage:** Phi recommends afternoon shade, windbreaks, raised stands, drainage, and a maintained alternative water supply. Some supporting claims are questionable or impractical, including associating standing water with Varroa or foulbrood and suggesting dehumidifiers, fans, or moving a hive as routine low-risk heat actions. The core siting checklist is present, but the field guidance needs human review.

## Preliminary decision

**Technically viable but likely weaker than Granite.**

Phi completed all 10 prompts without operational failure and matched Qwen's 81.8% keyword score, but first-read inspection found important false positives and unsafe or misleading details in pest pressure, harvest quality, and heat management. Several site and forage answers are useful, so this is not a formal rejection. A structured human review could quantify the gap, but the current evidence does not justify replacing Granite as the accuracy-first candidate.
