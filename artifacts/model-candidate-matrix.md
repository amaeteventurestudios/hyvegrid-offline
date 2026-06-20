# HyveGrid Offline Model Candidate Matrix

Purpose: compare small GGUF model candidates for ADTC 2026 using the same scoring-aware process.

This file exists because HyveGrid Offline has two layers:

1. **Scored model path:** the `.gguf` model, quantization, RAM, throughput, accuracy, crash behavior, and metadata prompts.
2. **Demo/product path:** CLI, SQLite retrieval, public apiculture notes, Yoruba mode, and local web UI.

The scored model path is the priority until the model is locked.

---

## Decision rule

Choose the smallest model that gives the best total tradeoff across:

- Agriculture and apiculture accuracy
- Tokens per second
- Peak RAM
- License safety
- Profiler stability
- No OOM or crash risk
- No thermal flag

Do not choose the smallest model just because it is small. Accuracy is weighted more heavily than efficiency, so a larger model can win if the accuracy gain is large enough and it still runs safely on the 8 GB profile.

---

## Temporary candidate shortlist

These are starting candidates only. Do not lock any candidate until current GGUF availability, license, accuracy, RAM, and throughput have been verified.

| # | Candidate model | Model family | Params | Why consider | Main risk | Initial decision |
|---|---|---|---:|---|---|---|
| 1 | Qwen2.5-1.5B-Instruct | Qwen | 1.5B | Strong reasoning per parameter, widely available GGUF variants | Verify license and current GGUF source | Test |
| 2 | Llama-3.2-1B-Instruct | Llama | 1B | Yes | hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF:Q4_K_M | Llama 3.2 Community License | Conditional | Q4_K_M | TBD | 2048 | TBD | 4.0 to 7.6 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 3.5 | 1.0 | Medium | Best Prompt 1 so far, but missed ants and water stress | Failed site-readiness reasoning | Yes / maybe | Prompt 1 was strongest so far. Prompt 2 misunderstood the site-readiness question and focused on human water-borne disease, soil, and crop water use instead of pesticide risk, forage, seasonal water, hive density, and site safety. See run log. | Do not lock. Compare next model |
| 3 | Llama-3.2-3B-Instruct | Llama | 3B | Better reasoning and knowledge potential | May exceed the 2.5 GB target, must profile | Test only if smaller models are weak |
| 4 | Gemma-2-2B-it | Gemma | 2B | Yes | bartowski/gemma-2-2b-it-GGUF:Q4_K_M | Gemma license | Conditional | Q4_K_M | 1.6 GB | 2048 prompt tests / 8192 profiler report | 1.95 | 2.03 profiler smoke / 1.5 to 3.5 local prompt tests | 16,258.61 ms | No | No | Smoke passed, accuracy skipped | TBD | 3.5 | 3.0 | Medium-good | Stronger ants and brood reasoning, but too broad on avoiding hive opening | Better site-readiness answer, but missed crop-specific forage and 20-hive density | Maybe / yes | Best first-bracket accuracy so far. Profiler smoke passed with safe memory under 2 GB peak RSS, but generation TPS and first-token latency are weak. Compare Granite profiler before locking. | Keep as accuracy candidate. Compare Granite profiler before lock |
| 5 | SmolLM2-1.7B-Instruct | SmolLM | 1.7B | Yes | bartowski/SmolLM2-1.7B-Instruct-GGUF:Q4_K_M | Apache 2.0 | Tentative yes | Q4_K_M | TBD | 2048 | TBD | 3.3 to 3.4 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 2.0 | 2.5 | Medium | Generic and incomplete | Useful but shallow | Maybe | Prompt 1 missed key hive-health checks. Prompt 2 mentioned chemicals, forage, and water, but missed crop-specific pesticide timing, seasonal water reliability, 20-hive density, and site-safety specifics. See run log. | Compare next model |

---

## Full comparison matrix

| # | Candidate model | Model family | Params | Instruct tuned? | GGUF source URL | License | License cleared? | Quantization tested | File size | Context used | Peak RAM GB | TPS | First-token latency | OOM/crash? | Thermal flag? | ADTC profiler passed? | Agriculture validation score | Prompt 1 score | Prompt 2 score | Caution language quality | Apiculture reasoning quality | Site-readiness reasoning quality | Fine-tune needed? | Notes | Decision |
|---|---|---|---:|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | Qwen2.5-1.5B-Instruct | Qwen | 1.5B | Yes | Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M | Apache 2.0 | Tentative yes | Q4_K_M | TBD | 2048 | TBD | 4.1 to 4.9 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 2.5 | 1.5 | Medium | Basic but incomplete | Weak and generic | Maybe | Prompt 1 was incomplete. Prompt 2 missed pesticide risk, water reliability, forage calendar, hive density, and site-safety specifics. See run log. | Retest / compare next model |
| 2 | Llama-3.2-1B-Instruct | Llama | 1B | Yes | hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF:Q4_K_M | Llama 3.2 Community License | Conditional | Q4_K_M | TBD | 2048 | TBD | 4.0 to 7.6 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 3.5 | 1.0 | Medium | Best Prompt 1 so far, but missed ants and water stress | Failed site-readiness reasoning | Yes / maybe | Prompt 1 was strongest so far. Prompt 2 misunderstood the site-readiness question and focused on human water-borne disease, soil, and crop water use instead of pesticide risk, forage, seasonal water, hive density, and site safety. See run log. | Do not lock. Compare next model |
| 3 | Llama-3.2-3B-Instruct | Llama | 3B | Yes | hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF:Q4_K_M | Llama 3.2 Community License | Conditional | Q4_K_M | TBD | 2048 | TBD | 1.9 to 2.1 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 2.5 | 2.5 | Medium | Over-focused on humidity/ventilation, missed colony strength and food/water stress | Partly relevant but incomplete | Maybe / yes | Prompt 1 was slower and not better than Llama 1B. Prompt 2 mentioned pesticide, herbicide, flood risk, forage, and climate, but missed spray timing, seasonal water reliability, 20-hive density, safety, access, and crop-specific forage detail. See run log. | Do not lock. Compare next model |
| 4 | Gemma-2-2B-it | Gemma | 2B | Yes | bartowski/gemma-2-2b-it-GGUF:Q4_K_M | Gemma license | Conditional | Q4_K_M | 1.6 GB | 2048 prompt tests / 8192 profiler report | 1.95 | 2.03 profiler smoke / 1.5 to 3.5 local prompt tests | 16,258.61 ms | No | No | Smoke passed, accuracy skipped | TBD | 3.5 | 3.0 | Medium-good | Stronger ants and brood reasoning, but too broad on avoiding hive opening | Better site-readiness answer, but missed crop-specific forage and 20-hive density | Maybe / yes | Best first-bracket accuracy so far. Profiler smoke passed with safe memory under 2 GB peak RSS, but generation TPS and first-token latency are weak. Compare Granite profiler before locking. | Keep as accuracy candidate. Compare Granite profiler before lock |
| 5 | SmolLM2-1.7B-Instruct | SmolLM | 1.7B | Yes | bartowski/SmolLM2-1.7B-Instruct-GGUF:Q4_K_M | Apache 2.0 | Tentative yes | Q4_K_M | TBD | 2048 | TBD | 3.3 to 3.4 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 2.0 | 2.5 | Medium | Generic and incomplete | Useful but shallow | Maybe | Prompt 1 missed key hive-health checks. Prompt 2 mentioned chemicals, forage, and water, but missed crop-specific pesticide timing, seasonal water reliability, 20-hive density, and site-safety specifics. See run log. | Compare next model |
| 6 | DeepSeek-R1-Distill-Qwen-1.5B | DeepSeek/Qwen | 1.5B | Yes | bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF:Q4_K_M | DeepSeek model license, verify before lock | Tentative | Q4_K_M | TBD | 2048 | TBD | 5.1 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 0.5 | TBD | Low | Failed Prompt 1 with visible reasoning and hallucinated beekeeping guidance | TBD | No | Output showed reasoning text, hallucinated sperm/oocysts and air filtering, missed core hive-health checks and immediate avoid guidance. See run log. | Do not continue unless doing one controlled no-reasoning recovery test |
| 7 | Qwen3-1.7B | Qwen | 1.7B | Yes | enacimie/Qwen3-1.7B-Q4_K_M-GGUF:Q4_K_M | Apache 2.0, verify source model license before lock | Tentative | Q4_K_M | TBD | 2048 | TBD | 3.7 to 6.2 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 1.0 | TBD | Low | Raw prompt triggered visible thinking. Controlled prompt gave a short but weak answer | TBD | No | Raw prompt entered visible thinking mode. Controlled /no_think prompt avoided reasoning but gave poor advice focused on hive board damage and hive mud. Missed ants, colony strength, brood, food, water, queen-right signs, harvest caution, and chemical caution. See run log. | Reject for now |
| 8 | Granite-3.3-2B-Instruct | Granite | 2B | Yes | ibm-granite/granite-3.3-2b-instruct-GGUF:Q4_K_M | Apache 2.0, verify before lock | Tentative | Q4_K_M | TBD | 2048 | TBD | 2.7 to 3.1 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 3.0 | 3.0 | Medium | Clean but incomplete hive-health answer | Relevant site-readiness answer, but missed density and spray coordination | Maybe / yes | Prompt 1 covered queen health and disturbance caution but missed ant entry, colony strength, food/water stress, brood detail, and harvest/chemical caution. Prompt 2 covered pesticide risk, safe distance, forage availability, water, terrain, shade, and predators, but missed spray timing, dry-season water backup, 20-hive density, crop-specific forage limits, human/livestock safety, access, and staged placement. See run log. | Keep as balanced backup. Compare against Gemma after profiler |
| 9 | Phi-4-mini-instruct | Phi | 3.84B | Yes | bartowski/microsoft_Phi-4-mini-instruct-GGUF:Q4_K_M | Microsoft license, verify before lock | Conditional | Q4_K_M | TBD | 2048 | TBD | 2.0 gen t/s local iMac | TBD | No | TBD | Not yet | TBD | 3.0 | 3.0 | Medium | Relevant but incomplete hive-health answer, did not beat Gemma | Relevant site-readiness answer, but missed density, spray coordination, and safety specifics | Maybe / yes | Prompt 1 covered ants, queen health, brood disease, pests, ventilation, and hive space but missed key avoid guidance. Prompt 2 covered pesticides, forage, blooming periods, water, habitat, land use, pollen/nectar quality, and pest pressure, but missed spray timing, dry-season water plan, 20-hive density, crop-specific forage limits, human/livestock safety, access, and staged placement. Slow for its size. See run log. | Do not lock. Keep as record only |
---

## Fields to record

| Field | Why it matters |
|---|---|
| Candidate model | Exact model name being tested |
| Model family | Qwen, Llama, Gemma, SmolLM, or another family |
| Params | Main RAM and speed driver |
| Instruct tuned? | HyveGrid needs instruction-following behavior |
| GGUF source URL | Needed later for `download_model.sh` |
| License | Must allow challenge-safe use |
| License cleared? | No unclear license gets locked |
| Quantization tested | Start with Q4_K_M, then test Q5_K_M if promising |
| File size | Rough proxy for RAM pressure |
| Context used | Smaller context helps RAM and speed |
| Peak RAM GB | Drives efficiency score |
| TPS | Drives performance score |
| First-token latency | Helps responsiveness and audit notes |
| OOM/crash? | Hard rejection if yes |
| Thermal flag? | Avoid thermal penalty |
| ADTC profiler passed? | Must pass before model lock |
| Agriculture validation score | Main accuracy proxy |
| Prompt 1 score | Hive-health prompt quality |
| Prompt 2 score | Site-readiness prompt quality |
| Caution language quality | Checks whether the model avoids unsafe overclaiming |
| Apiculture reasoning quality | Checks beekeeping competence |
| Site-readiness reasoning quality | Checks farm placement and pesticide-risk reasoning |
| Fine-tune needed? | Decides whether we move into public QA dataset and training |
| Notes | Weird outputs, license concerns, profiling issues |
| Decision | Keep, reject, or retest |

---

## Official HyveGrid Offline test prompts

### Prompt 1: Hive Health Advisor

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

### Prompt 2: Site Readiness Advisor

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

---

## Manual scoring rubric: Prompt 1

Use a 0 to 5 score.

| Score | Meaning |
|---:|---|
| 5 | Mentions ants entering the hive, colony strength, brood pattern, food or water stress, avoids immediate harvest or chemical overreaction, and recommends physical inspection |
| 4 | Covers most important checks, with only minor missing detail |
| 3 | Generally useful but incomplete |
| 2 | Generic beekeeping advice with weak prioritization |
| 1 | Mostly wrong, unsafe, or misleading |
| 0 | Fails, hallucinates, or gives dangerous advice |

### Required key points for a strong Prompt 1 answer

- Check whether ants are only near the stand or entering the hive.
- Check hive stand protection, nearby ant trails, and ground contact points.
- Check colony strength and whether the colony is too weak to defend itself.
- Check brood pattern, capped brood, larvae condition, and queen-right signs.
- Check food stores, water stress, heat stress, and recent disturbance.
- Avoid harvesting immediately.
- Avoid spraying chemicals into or near the hive.
- Avoid moving the hive immediately unless there is a clear safety reason.
- Confirm by physical inspection.
- Use cautious language: possible concern, check first, not certified diagnosis.

---

## Manual scoring rubric: Prompt 2

Use a 0 to 5 score.

| Score | Meaning |
|---:|---|
| 5 | Covers pesticide risk, water reliability, forage seasonality, shade and wind, human and livestock safety, hive density, access, and farm spraying coordination |
| 4 | Covers most important factors, with only minor missing detail |
| 3 | Useful but shallow |
| 2 | Generic siting advice with weak local reasoning |
| 1 | Mostly wrong, unsafe, or misleading |
| 0 | Fails, hallucinates, or gives dangerous advice |

### Required key points for a strong Prompt 2 answer

- Evaluate pesticide and herbicide risk from pepper and vegetable farms.
- Coordinate with farmers on spray timing and chemical use.
- Check whether the seasonal water source is reliable through dry periods.
- Provide or plan clean water if the natural source dries up.
- Evaluate forage diversity and flowering seasonality across mango, vegetables, cassava, and surrounding plants.
- Avoid assuming cassava is enough forage by itself.
- Check shade, wind protection, drainage, flooding risk, and heat exposure.
- Check human, livestock, and footpath safety.
- Confirm access for hive inspection and harvest.
- Consider hive spacing, stand height, and colony density for 20 hives.
- Use cautious site-readiness language rather than promising success.

---

## Candidate run log

Use this section after each candidate test.

### Candidate run: Qwen2.5-1.5B-Instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-18 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | Qwen/Qwen2.5-1.5B-Instruct-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf Qwen/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 32.3 t/s. Generation: 4.9 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 2.5 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 |

Notes:

- The model gave a structured answer and noticed ants, smell, and partially capped brood.
- It missed colony strength, food stores, water stress, harvest caution, chemical caution, and careful physical inspection.
- It incorrectly suggested avoiding opening the hive, using a smoker, or using a hive tool.
- Better guidance would be to inspect carefully and avoid disturbing the colony aggressively.
- Current result is usable but not strong enough to lock.

### Candidate run: SmolLM2-1.7B-Instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-18 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | bartowski/SmolLM2-1.7B-Instruct-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf bartowski/SmolLM2-1.7B-Instruct-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 20.5 t/s. Generation: 3.4 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 2.0 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 |

Notes:

- The model gave a generic answer focused on disease, queen presence, and temperature/humidity.
- It did not specifically address ants entering the hive or ant pressure.
- It missed colony strength, food stores, water stress, brood pattern detail, harvest caution, chemical caution, and careful physical inspection.
- It gave weak avoidance guidance by saying not to add more bees or honey.
- Current result is weaker than Qwen2.5 on Prompt 1.

Prompt 2 notes:

- The model gave a general apiary site answer.
- It mentioned agricultural chemicals, nectar and pollen availability, plant diversity, water, pests, and human activity.
- It did not focus enough on the exact crop setting: cassava, mango, pepper, and vegetable farms.
- It missed spray timing coordination with pepper and vegetable farmers.
- It did not address that the water source is seasonal and may fail in the dry season.
- It did not evaluate whether the site can support 20 hives.
- It missed shade, wind, heat, drainage, livestock, roads, footpaths, and harvest access.
- It incorrectly mentioned natural nesting sites, which is not the core issue for managed hive placement.
- Current result is useful but too shallow to lock.

### Candidate run: Llama-3.2-1B-Instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf hugging-quants/Llama-3.2-1B-Instruct-Q4_K_M-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 42.6 t/s. Generation: 7.6 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 3.5 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 |

Notes:

- This is the best Prompt 1 answer so far.
- The model covered ventilation, honey stores, brood/queen condition, pollen and nectar stores, and chemical-treatment caution.
- It missed the ant-pressure detail and did not clearly say to check whether ants are entering the hive.
- It missed colony strength, adult bee population, water stress, and immediate harvest caution.
- It gave somewhat awkward wording about not opening or inspecting too quickly. Better guidance would be careful physical inspection without aggressive disturbance.
- Current result is promising enough to continue to Prompt 2.

Prompt 2 notes:

- The model misunderstood the prompt.
- It focused on water-borne human diseases such as malaria, typhoid, and schistosomiasis.
- It discussed crop water requirements and soil quality instead of apiary siting.
- It missed pesticide and spray timing risk from pepper and vegetable farms.
- It missed seasonal water reliability for bees.
- It missed forage diversity, flowering calendar, and whether the site can support 20 hives.
- It missed shade, wind, heat, drainage, livestock, roads, footpaths, and inspection/harvest access.
- Current result is not strong enough to lock.

### Candidate run: Gemma-2-2B-it Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install, ADTC profiler smoke test |
| Model | bartowski/gemma-2-2b-it-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf bartowski/gemma-2-2b-it-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | Profiler smoke: 1,949 MB peak RSS |
| TPS | Profiler smoke: 2.03 gen t/s; local prompt tests: 1.5 to 3.5 gen t/s |
| First-token latency | 16,258.61 ms profiler smoke |
| Profiler output path | artifacts/gemma-participant-smoke.json |
| Prompt 1 score | 3.5 / 5 |
| Prompt 2 score | 3.0 / 5 |
| Agriculture validation score | TBD |
| Decision | Keep as accuracy candidate. Compare Granite profiler before lock |

Notes:

- The model gave one of the better Prompt 1 answers so far.
- It correctly prioritized ants near the hive as a serious concern.
- It connected partially capped brood to brood-development concerns, nutrition, disease, and stress.
- It correctly warned against treating the hive without a diagnosis.
- It missed colony strength, adult bee population, food stores, water stress, queen-right signs, and immediate harvest caution.
- It said to avoid opening the hive, which is too broad. Better guidance would be careful physical inspection without aggressive disturbance.
- Generation speed was very slow on the local iMac test.

Prompt 2 notes:

- The model gave the best Prompt 2 answer from the first bracket so far.
- It covered pesticide and herbicide risk, seasonal water reliability, water quality, water accessibility, farm traffic, machinery disturbance, livestock or animal activity, wind exposure, drainage, and regulatory considerations.
- It did not focus enough on the specific crops: cassava, mango, pepper, and vegetables.
- It missed spray timing coordination with pepper and vegetable farmers.
- It did not evaluate whether the site can support 20 hives.
- It missed forage calendar, flowering gaps, mango as seasonal forage, and cassava as limited forage.
- It missed safe distance from homes, roads, schools, and footpaths.
- It missed inspection and harvest access.
- It did not recommend staged placement if the site is uncertain.
- Generation speed was slow but better than Prompt 1.

### Candidate run: DeepSeek-R1-Distill-Qwen-1.5B Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf bartowski/DeepSeek-R1-Distill-Qwen-1.5B-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 27.0 t/s. Generation: 5.1 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 0.5 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Do not continue unless doing one controlled no-reasoning recovery test |

Notes:

- The model entered visible reasoning mode instead of giving a direct final answer.
- It hallucinated inappropriate beekeeping details such as checking sperm and oocysts.
- It suggested air filtering or dehumidifying around the hive, which is not practical field guidance.
- It missed ant entry checks, colony strength, food stores, water stress, queen-right signs, harvest caution, chemical caution, and careful inspection guidance.
- The speed was good, but the answer quality was not acceptable.
---

### Candidate run: Qwen3-1.7B Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | enacimie/Qwen3-1.7B-Q4_K_M-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf enacimie/Qwen3-1.7B-Q4_K_M-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 25.1 t/s. Generation: 3.7 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 1.0 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Run one no-thinking recovery test before rejecting |

Notes:

- The model entered visible thinking mode instead of giving a direct field answer.
- It noticed low hive activity, ants, partially capped brood, and possible forage/food issues.
- It did not clearly answer what to check first or what to avoid doing immediately.
- It missed ant entry checks, colony strength, food stores, water stress, queen-right signs, harvest caution, chemical caution, and careful inspection guidance.
- Current raw-prompt result is not acceptable.

Controlled recovery test:

- Command/control used: `/no_think` plus English-only direct-answer instruction.
- The model stopped showing visible reasoning.
- The answer was too short and missed the main beekeeping checks.
- It focused on hive board or entrance damage and mentioned hive mud.
- It still missed ants entering the hive, colony strength, food stores, water stress, brood pattern, queen-right signs, harvest caution, chemical caution, and careful inspection.
- Controlled recovery result does not save the model.

### Candidate run: Granite-3.3-2B-Instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | ibm-granite/granite-3.3-2b-instruct-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf ibm-granite/granite-3.3-2b-instruct-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 23.3 t/s. Generation: 2.7 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 3.0 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 |

Notes:

- The model gave a clean but incomplete hive-health answer.
- It prioritized queen presence and queen health.
- It correctly warned against excessive disturbance.
- It warned against adding sugar syrup or introducing new bees without expert guidance.
- It mentioned temperature and humidity.
- It missed checking whether ants are entering the hive.
- It missed colony strength, adult bee population, food stores, water stress, brood pattern detail, immediate harvest caution, blind chemical-treatment caution, and careful inspection wording.
- It weakly connected ants to Varroa or parasitic mites instead of first treating them as ant pressure or a hive-stand protection issue.

Prompt 2 notes:

- The model gave a relevant site-readiness answer.
- It covered pesticide residue risk, safe distance from farms, forage availability, forage diversity, seasonal water, water contamination, terrain, sun exposure, shade, temperature protection, and predators.
- It did not clearly address spray timing coordination with pepper and vegetable farmers.
- It did not explain the dry-season risk of relying on a seasonal water source.
- It did not evaluate whether the site can support 20 hives.
- It missed hive density, overstocking risk, and staged placement.
- It missed crop-specific forage detail: mango as seasonal forage, cassava as limited forage, and pepper/vegetables as higher pesticide-risk crops.
- It missed safe distance from homes, schools, roads, paths, and livestock.
- It missed inspection and harvest access.

File size: 1.4 GB
Peak RAM GB: 1.72
TPS: 2.97 profiler smoke / 2.7 to 3.1 local prompt tests
First-token latency: 18,039.5 ms
Thermal flag?: No
ADTC profiler passed?: Smoke passed, accuracy skipped
Decision: Keep as profiler leader. Compare with Gemma on accuracy before lock.

### Candidate run: Phi-4-mini-instruct Q4_K_M

| Item | Value |
|---|---|
| Date tested | 2026-06-19 |
| Machine/profile | Amaete iMac, macOS, local llama.cpp Homebrew install |
| Model | bartowski/microsoft_Phi-4-mini-instruct-GGUF |
| Quantization | Q4_K_M |
| Command used | `llama-cli -hf bartowski/microsoft_Phi-4-mini-instruct-GGUF:Q4_K_M -p "<Prompt 1>" -n 350 -c 2048 --temp 0.2` |
| Peak RAM | TBD |
| TPS | Prompt processing: 8.8 t/s. Generation: 2.0 t/s. Local Mac result only, not final profiler. |
| First-token latency | TBD |
| Profiler output path | TBD |
| Prompt 1 score | 3.0 / 5 |
| Prompt 2 score | TBD |
| Agriculture validation score | TBD |
| Decision | Retest with Prompt 2 only for completeness |

Notes:

- The model gave a relevant but incomplete hive-health answer.
- It correctly treated ants as an important first signal.
- It covered queen presence, queen health, brood disease, dead larvae, deformed brood, pests, ventilation, and hive space.
- It missed colony strength, adult bee population, food stores, pollen stores, water stress, and checking whether ants are entering the hive.
- It did not clearly answer what to avoid doing immediately.
- It did not clearly warn against immediate harvest or blind chemical treatment.
- It began moving toward treatment advice before confirming the problem, which is risky for field guidance.
- The model is heavier and slower than the current leader, so Prompt 1 does not justify locking it.

Prompt 2 notes:

- The model gave a relevant site-readiness answer.
- It covered pesticide use, pesticide frequency, crop diversity, forage availability, blooming periods, water proximity, contamination/runoff risk, wildflowers, shrubs, trees, land-use practices, pollen/nectar quality, and pest/disease pressure.
- It did not clearly address spray timing coordination with pepper and vegetable farmers.
- It did not explain the dry-season risk of relying on a seasonal water source.
- It did not evaluate whether the site can support 20 hives.
- It missed hive density, overstocking risk, and staged placement.
- It missed crop-specific forage detail: mango as seasonal forage, cassava as limited forage, and pepper/vegetables as higher pesticide-risk crops.
- It missed safe distance from homes, schools, roads, paths, and livestock.
- It missed inspection and harvest access.
- The answer was decent, but not strong enough to justify the heavier model.

## Finalist profiler decision

After first-bracket and second-bracket testing, the strongest candidates are:

| Rank | Model | Role | Reason |
|---:|---|---|---|
| 1 | Gemma-2-2B-it Q4_K_M | Accuracy candidate | Best content quality across the two ADTC prompts so far |
| 2 | Granite-3.3-2B-Instruct Q4_K_M | Balanced backup | More consistent than most models, likely better license/compliance posture |
| 3 | Llama-3.2-1B-Instruct Q4_K_M | Speed baseline | Fastest usable candidate but weak on site-readiness |

Next decision depends on ADTC profiler results, not local Mac speed alone.

## Local model path smoke test

| Item | Result |
|---|---|
| Date tested | 2026-06-19 |
| Selected test model | Gemma-2-2B-it Q4_K_M |
| Local model path | `model/hyvegrid-offline.gguf` |
| File size | 1.6 GB |
| Git tracking check | Passed. `git status` showed clean working tree. |
| Prompt 1 local path run | Passed |
| Prompt 2 local path run | Passed |
| Prompt 1 local path score | 3.0 / 5 |
| Prompt 2 local path score | 3.0 / 5 |
| Decision | Local model slot validated. Ready for profiler testing. |

Notes:

- The model successfully ran from `model/hyvegrid-offline.gguf`.
- This confirms the repo can point to one selected offline GGUF model.
- The model file is ignored by Git and was not committed.
- Local Mac results are smoke-test results only, not final ADTC profiler results.

## ADTC profiler smoke test: Gemma

| Item | Result |
|---|---|
| Date tested | 2026-06-19 |
| Profiler version | adtc-profiler 0.1.0 |
| Mode | participant |
| Accuracy skipped? | Yes |
| Model path | `model.gguf` |
| Model source | `model/hyvegrid-offline.gguf` symlinked to root `model.gguf` |
| Model architecture | gemma2 |
| Claimed params | 2B |
| Context length reported | 8192 |
| Generation TPS | 2.03 |
| First-token latency | 16,258.61 ms |
| Prompt tokens | 512 |
| Generated tokens | 128 |
| Peak RSS | 1,949 MB |
| Steady-state RSS | 1,675.48 MB |
| Peak VMS | 71,197.46 MB |
| CPU p99 | 88% |
| Thermal throttled | false |
| Accuracy | Skipped |
| Output file | `artifacts/gemma-participant-smoke.json` |
| Decision | Memory looks safe. Speed and first-token latency are weak. Compare Granite before locking. |

Notes:

- This was measured on Amaete's iMac, not the ADTC Standard Laptop.
- The profiler completed successfully and produced a schema-valid participant JSON.
- Gemma stayed under 2 GB peak RSS in this smoke run.
- Generation speed was only 2.03 tokens/sec.
- First-token latency was high at 16.26 seconds.
- Do not lock Gemma until Granite is profiled for comparison.

## ADTC profiler smoke test: Granite

| Item | Result |
|---|---|
| Date tested | 2026-06-19 |
| Profiler version | adtc-profiler 0.1.0 |
| Mode | participant |
| Accuracy skipped? | Yes |
| Model path | `model.gguf` |
| Model source | `model/granite-3.3-2b-instruct-Q4_K_M.gguf` symlinked to root `model.gguf` |
| Model architecture | granite |
| Claimed params | 2B |
| Context length reported | 131072 |
| Generation TPS | 2.97 |
| First-token latency | 18,039.5 ms |
| Prompt tokens | 512 |
| Generated tokens | 128 |
| Peak RSS | 1,723.32 MB |
| Steady-state RSS | 1,647.27 MB |
| Peak VMS | 70,622.48 MB |
| CPU p99 | 91% |
| Thermal throttled | false |
| Accuracy | Skipped |
| Output file | `artifacts/granite-participant-smoke.json` |
| Decision | Faster and lighter than Gemma, but manual prompt quality was weaker. Keep as profiler leader and compare with accuracy-bearing tests before locking. |

Notes:

- This was measured on Amaete's iMac, not the ADTC Standard Laptop.
- The profiler completed successfully and produced a schema-valid participant JSON.
- Granite stayed under 1.8 GB peak RSS in this smoke run.
- Generation speed was 2.97 tokens/sec, faster than Gemma's 2.03 tokens/sec.
- First-token latency was high at 18.04 seconds.
- Do not lock Granite until accuracy-bearing tests confirm it can compete with Gemma on agriculture and apiculture.

## Lock criteria

Do not lock the scoring model until all of these are true:

- License is cleared.
- `download_model.sh` can download the exact GGUF without credentials.
- The path matches `metadata.json`.
- ADTC profiler passes on a constrained 8 GB-style profile.
- No OOM or crash.
- No thermal flag.
- Peak RAM target is under 2.5 GB, unless a larger model is justified by measured accuracy gain.
- TPS is at or near 15.
- Prompt 1 and Prompt 2 scores are strong enough to defend publicly.
- Agriculture validation score is competitive among tested candidates.

---

## One rule

```text
If a task does not change the .gguf, its quantization, or the 2 metadata test prompts,
it does not change the automated score. Build it only after the model is locked.
```
