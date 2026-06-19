# HyveGrid Offline — ADTC 2026 Build Plan (v2)

Offline apiculture intelligence for African beekeepers and extension workers, built to win the Africa Deep Tech Challenge 2026 Laptop LLM track.

This version replaces the original plan. The original was a good product plan but the wrong competition plan. ADTC's automated scoring is model-centric: the app, RAG layer, and Yoruba mode support the demo, documentation, African use-case bonus, and live evaluation, but the GGUF model's own performance must be treated as the core scoring asset. The challenge still asks for a working end-to-end on-device app, so the app is built, but only after the model is proven. This version puts the model first and reframes the app as the demo and field-product layer around it.

---

## 0. What changed from v1 and why

| Change | Reason |
|---|---|
| Model work moved to the front | The profiler runs your bare GGUF through `llama-bench`. Your app, RAG, and Yoruba do not execute in the scored telemetry path. Confirm the accuracy path against the profiler source (see section 17). |
| RAG reclassified as demo layer | Retrieval almost certainly cannot ground the scored answers. Knowledge must live in the model weights to affect accuracy, pending profiler-source confirmation. |
| RAM target tightened to under 2.5 GB | Efficiency scores linearly: `Seff = (7 − peakRAM) / 7 × 100`. Lower RAM keeps earning points with no floor. |
| Throughput target kept at 15 TPS | The profiler normalises against a provisional `TPS_REFERENCE = 15.0`. Reaching 15 maxes speed. |
| Agriculture validation set added near top | Accuracy includes a multiple-choice benchmark on a provided domain validation set, not just your prompts. |
| Yoruba reframed as use-case story | English is the evaluation language. The African Use Case Bonus is up to 10 points for African applicability, not language specifically. |
| Operating deadline set to Aug 26, 2026 | Devpost shows a single deadline of Aug 26, 2026, 11:45pm PDT. Verify the schedule page for any gates. |

---

## 1. Two theses, kept separate

**Product thesis (what HyveGrid Offline is):**
A local AI field assistant for African beekeeping that runs offline on a low-cost laptop, grounded in public apiculture notes, with meaningful Yoruba field support.

**Competition thesis (what we submit and how it scores):**
A small GGUF model that answers English agriculture and apiculture prompts well on its own, packaged to the official template, profiled under 2.5 GB peak RAM at 15 or more tokens per second, with the HyveGrid app, RAG, and Yoruba mode demonstrating the real African field product around that model.

Both are true. The competition thesis decides where the engineering effort goes first.

---

## 2. What the scoring actually measures

```
S_total = 0.50 × S_acc + 0.30 × S_perf + 0.20 × S_eff − P_thermal
```

| Component | Weight | Formula | Touched by the app? |
|---|---|---|---|
| Accuracy | 50% | MCQ benchmark on domain validation set + 4 prompts, judge-scored 0–100 | No. Bare model only. |
| Throughput | 30% | `min(TPS / 15.0, 1.0) × 100`, 15.0 provisional | No. Bare model only. |
| Efficiency | 20% | `(7 − peakRAM_GB) / 7 × 100` | No. Bare model only. |
| Thermal | −10 | −10 if throttle or core temp > 85°C | No. |
| African Use Case Bonus | up to +10 pts | Applicability to a real African use case | Yes. App, Yoruba, REPORT, demo. |
| OOM or crash | disqualify | `S_total = 0` | Hard gate. |

The model carries 100% of the automated telemetry. The app earns only the up-to-10-point bonus plus the qualitative half of accuracy through documentation and live defense.

---

## 3. The RAM target: can we cook under 2.5 GB?

Yes, with a 1B to 1.5B model at Q4_K_M and a modest context window. But 2.5 GB is a target tier, not a vow. Accuracy is worth more than efficiency, so the agriculture benchmark gets veto power.

**Why under 2.5 GB is worth chasing:**

| Peak RAM | Seff (raw) | Seff weighted (20%) |
|---|---|---|
| 2.5 GB | 64.3 | 12.9 pts |
| 4.0 GB | 42.9 | 8.6 pts |
| 5.5 GB | 21.4 | 4.3 pts |

Going from 5.5 GB to 2.5 GB is worth about 8.6 extra total points. Real, but not decisive on its own.

**Why accuracy can still override it:**
Accuracy is weighted 50%. If a larger model that fits under, say, 4 GB scores 15 points higher on the accuracy benchmark, that is 7.5 weighted points, which nearly cancels the efficiency gain and likely wins overall because accuracy quality also drives the judge panel and the bonus.

**The decision rule:**
```
Target peak RAM < 2.5 GB.
Accept a larger model only if it raises benchmark accuracy by more than
the efficiency points it costs, measured on the real agriculture set.
Never exceed the safe ceiling that risks OOM on the 8 GB profile.
```

**What makes up peak RSS (so we can control it):**
- Quantized weights resident in memory (the bulk).
- KV cache, which grows with context length. Keep context as small as the prompts need.
- llama.cpp runtime overhead.

**Levers to stay under 2.5 GB:**
- Pick a 1B to 1.5B model, Q4_K_M.
- Use the smallest context window that handles the prompts. The test prompts are short.
- Consider quantized KV cache if the profiler's bench settings allow it.
- Match the profiler's `llama-bench` context defaults so your self-check matches the audit.

---

## 4. Hard compliance constraints

Pulled directly from the official template and profiler. These are pass or fail.

- [ ] Repository is public on GitHub at evaluation time.
- [ ] `metadata.json` fully filled, no placeholder values, exactly 2 test prompts in your domain.
- [ ] `download_model.sh` downloads a valid `.gguf` to `model/`, is idempotent, needs no credentials, and the path matches `_runtime.model_path`.
- [ ] `*.gguf` and `model/` are in `.gitignore`. No weights in git.
- [ ] `REPORT.md` filled with the technical writeup.
- [ ] Runs 100% offline during evaluation, zero network calls after the download step.
- [ ] llama.cpp only, GGUF only.
- [ ] Runs within the 8 GB profile (4 vCPU, integrated GPU). No OOM.
- [ ] `budget_laptop_claim` set to true.
- [ ] `cross_disciplinary_pairing` filled with `load_bearing: true` and a real description.
- [ ] Submitted on Devpost before Aug 26, 2026, 11:45pm PDT.

---

## 5. IP boundary

Public challenge edition only. Absent from the repo and the public site:

| Excluded | Reason |
|---|---|
| Proprietary hardware and firmware | Patent and IP risk |
| Sensor IP and logic | IP risk |
| Private datasets and field records | Data and IP risk |
| Commercial roadmap and Honey Flow internal strategy | Strategy risk |
| Partner, pilot, and investor materials | Confidentiality |
| API keys and credentials | Security |

Allowed: public apiculture notes, public sources, open-source model components, challenge-safe code, basic local retrieval, manual or sample edge-signal inputs, public Yoruba templates.

Use the framing "manual observations or sample edge-signal inputs." Bluetooth hive sensors are described only as an optional future architecture, never required for judging, never disclosed in design detail.

---

## 6. Repository structure

One public repo. Template files at root for compliance. App and data live in extra folders that the profiler ignores but judges and the demo video can show.

```
hyvegrid-offline-adtc-2026/
  metadata.json          # required, scored path
  download_model.sh      # required, downloads the .gguf
  REPORT.md              # required, technical story
  SCORING.md             # what affects the score and what does not
  README.md
  .gitignore             # must exclude *.gguf and model/
  LICENSE                # match challenge requirements
  model/                 # populated by download_model.sh, never committed

  app/                   # demo layer, ignored by profiler
  data/                  # public apiculture notes, ignored by profiler
  scripts/               # dataset build, profiler helpers
  tests/                 # prompt tests, benchmark harness
  artifacts/             # profiler outputs, benchmark evidence

  specs/
    001-hyvegrid-offline/
      spec.md plan.md tasks.md research.md data-model.md quickstart.md
```

The extra folders do not affect telemetry. The profiler reads only `_runtime.model_path`.

---

## 7. Build order

Compliance is a gate. Model is the contest. App is the demo. Do not start app work until the model is locked.

| # | Workstream | Acceptance test |
|---|---|---|
| 1 | Fork official template, set up repo skeleton | Repo matches template, profiler can read metadata |
| 2 | Model candidate shortlist | 3 to 5 small GGUF candidates chosen with license cleared |
| 3 | Agriculture validation set | The ADTC set obtained, or a faithful proxy built |
| 4 | First download + profiler run on smallest candidate | Real peak RAM and TPS on an 8 GB profile |
| 5 | Benchmark candidates on validation set + 2 prompts | Accuracy, RAM, TPS table for every candidate |
| 6 | Decide base model vs fine-tune | Documented decision with evidence |
| 7 | If fine-tuning: build public ag/apiculture QA dataset, train | Tuned model beats base on the validation set |
| 8 | Quantize variants (Q4_K_M, Q5_K_M), benchmark each | Best accuracy within the RAM target |
| 9 | Lock the scoring model | Model frozen, metadata model fields final |
| 10 | CLI engine (demo layer) | Asks a hive question, returns a grounded answer |
| 11 | SQLite + FTS5 RAG (demo layer) | Retrieval returns relevant notes for 80% of 20 test prompts |
| 12 | Yoruba controlled field mode | A real hive-health task completes end to end in Yoruba |
| 13 | Local web UI + Offline System Status screen | App opens at localhost offline, shows compliance |
| 14 | REPORT.md with constrained benchmark numbers | Numbers come from an 8 GB profile, within audit tolerance |
| 15 | Demo video, 2 minutes | Viewer understands the product and sees it run |
| 16 | Clean clone + profiler audit | Fresh clone runs, no missing files, no cloud calls |
| 17 | Submit on Devpost | Locked commit, before Aug 26 |

---

## 8. Model strategy (the heart of the submission)

**Candidate shortlist (verify current availability, GGUF, and license at build time):**

| Candidate | Size | Why consider | Risk |
|---|---|---|---|
| Qwen2.5-1.5B-Instruct | 1.5B | Strong reasoning per parameter, GGUF widely available | Verify license tier |
| Llama-3.2-1B-Instruct | 1B | Very low RAM, fast | Weaker on knowledge benchmarks |
| Llama-3.2-3B-Instruct | 3B | Better accuracy | Likely breaks 2.5 GB, test for ceiling |
| Gemma-2-2B-it | 2B | Good quality for size | Borderline on 2.5 GB target |
| SmolLM2-1.7B-Instruct | 1.7B | Small, capable | Verify agriculture performance |

The small-model landscape moves fast. Before locking step 2, check for the newest small instruct models (current Qwen, Gemma, and Llama small variants) and prefer the strongest one that fits the RAM tier with a license that allows challenge use. Treat this shortlist as temporary. Do not lock Qwen2.5, Llama 3.2, Gemma 2, or SmolLM2 yet. Lock only the evaluation process: the same accuracy harness, RAM measurement, and profiler run applied to whatever candidates are current at build time.

**Base model vs fine-tune (step 6):**
- If a base model already scores well on the agriculture validation set, ship it. Simpler, lower risk.
- If base accuracy is weak, fine-tune a small base on a public agriculture and apiculture QA dataset so the knowledge lives in the weights. This is the only way to lift the scored accuracy, because RAG is not in the scored path.

**Quantization (step 8):**
- Start at Q4_K_M for the RAM target.
- Test Q5_K_M for an accuracy bump if it still fits under 2.5 GB.
- Record peak RAM, TPS, and accuracy for each variant before deciding.

**Lock criteria (step 9):**
- Peak RAM under 2.5 GB, or justified by an accuracy gain that beats the efficiency cost.
- TPS at or above 15 on the 8 GB profile.
- No OOM, no thermal flag.
- Best agriculture benchmark accuracy among the candidates that meet the above.

---

## 9. Accuracy strategy

Accuracy is half the score and the part the original plan ignored.

- **Get the validation set first.** Check the Devpost Resources tab for the agriculture validation set, or ask the organizers. Its format and difficulty drive model choice.
- **Build a local accuracy harness.** Fix the expected key points for your 2 test prompts and run the validation set on each candidate model. This catches regressions when you quantize or fine-tune.
- **Design for hidden prompts.** Organizers add 2 hidden prompts in agriculture. Do not overfit to your 2. Train and test on a spread of agriculture and apiculture topics.
- **Two required test prompts:**
  1. A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
  2. An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?

**Caution language the model and templates should use:** possible concern, check first, avoid doing immediately, confirm by physical inspection, consult an experienced beekeeper or extension officer when needed. HyveGrid Offline is field triage, not certified diagnosis.

---

## 10. The demo layer (app, RAG, Yoruba)

Scoped as the field product and the bonus story, built only after the model is locked.

- **CLI engine:** question, retrieve local notes, build prompt, run local GGUF, return field-friendly answer.
- **Public knowledge base:** hive health, weak colony, ants and pests, wax moth, absconding, heat stress, apiary siting, water access, shade and wind, pesticide risk, human and livestock safety, harvest timing, moisture risk, smoke contamination, filtering and storage, traceability basics, forage and pollination, Nigeria-relevant examples, sensor-style patterns, Yoruba glossary and templates, sources.
- **RAG:** SQLite FTS5, no cloud vector database. Demonstrates grounding and reliability in the video and live defense.
- **Yoruba mode:** English and Yoruba toggle, Yoruba labels, glossary, structured field flow, controlled response templates, a real Yoruba demo task. Use controlled templates so the small model does not freestyle Yoruba. Get a native Yoruba speaker to review before submission.
- **Screens:** Mission Control, Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, Hive Signal Check, Offline System Status.

A judge should grasp in 30 seconds: this is offline, this is beekeeping, this runs locally, this has Yoruba support, this is more than a chatbot.

---

## 11. Profiler discipline

Install:
```
pip install "git+https://github.com/Africa-Deep-Tech-Foundation/adtc-profiler.git"
```

Self-check:
```
bash download_model.sh
adtc-profiler run --submission . --mode participant --output artifacts/submission.json --skip-accuracy
```

**Run it from step 4 onward, on every model and every quantization.**

**Benchmark on a constrained environment, not your iMac.** The audit compares your reported numbers to a constrained run. Tolerances: peak RAM ±15% (fail over 50%), TPS and first-token latency ±25% (fail over 50%). Mismatched numbers get flagged or failed.

Constrained test target:
```
docker run --rm -it --memory=7g --cpus=4 -v "$PWD:/app" -w /app ubuntu:22.04
```
Validate finally on a real 8 GB Ubuntu 22.04 laptop.

Track: peak RAM (target under 2.5 GB), TPS (target 15+), first-token latency, zero OOM, no thermal flag, fully offline.

---

## 12. REPORT.md outline

One to three pages, factual and specific.

- Problem and African context: beekeepers and extension workers need field guidance without reliable connectivity in Nigeria.
- Design decisions: which base model, why that size, why that quantization, what alternatives were tested.
- Constraints: 8 GB RAM, integrated graphics, offline, the 2.5 GB target and how it was met.
- Benchmarks: peak RAM, TPS, latency from the constrained profile, plus accuracy on the validation set.
- Cross-disciplinary pairing: apiculture plus offline retrieval plus site and sensor-style reasoning, load-bearing.
- Limitations: not certified diagnosis, public prototype, no hardware system.
- How to run: clone, download model, run app, run profiler.

Include the boundary line: HyveGrid Offline is a public challenge edition. It does not include proprietary hardware, private field data, sensor IP, or commercial operating strategy.

---

## 13. Demo video script, 2 minutes

| Time | Scene |
|---|---|
| 0:00–0:15 | HyveGrid Offline runs local AI for African beekeeping, no cloud. |
| 0:15–0:30 | Offline proof: disconnect network, app still answers. |
| 0:30–0:55 | Hive Health: the low-activity and ants prompt. |
| 0:55–1:15 | Site Readiness: the 20-hives-near-crops prompt. |
| 1:15–1:30 | Yoruba mode: a real field task end to end in Yoruba. |
| 1:30–1:45 | System status: llama.cpp, GGUF, SQLite, offline, RAM number. |
| 1:45–2:00 | Built for low-cost laptops, public challenge edition. |

---

## 14. Final audit and submit

```
git clone YOUR_REPO_URL
cd hyvegrid-offline-adtc-2026
bash download_model.sh
adtc-profiler run --submission . --mode participant --output artifacts/submission.json --skip-accuracy
```

Offline test: disconnect network after the model download, then confirm the app opens, search works, the model answers, Yoruba mode works, no cloud calls, no crash.

IP audit before pushing public, and scan git history, not just the current tree: no hardware designs, no sensor IP, no private datasets, no roadmap, no internal strategy, no credentials, no API keys.

Submit on Devpost with the locked commit before Aug 26, 2026, 11:45pm PDT.

---

## 15. GLM usage rules

GLM is a coding worker during development, never the runtime model.

- One GLM prompt equals one small engineering ticket.
- Ask for patches, not giant rewrites. Review diffs before accepting.
- No random refactors of unrelated files.
- Keep the repo small and focused.
- Example instruction: "Implement Task 011 only: SQLite FTS5 retrieval. Do not edit metadata.json or model files."
- Do not spend GLM quota on the model science. Model selection, fine-tuning, and profiling are your decisions, made on evidence, not delegated.

---

## 16. Operating principle

```
Compliance first.
Model scoring second.
Profiler third.
Public apiculture demo layer fourth.
Yoruba field support fifth.
UI polish sixth.
Website last.
```

The mistake would be building a polished app first and discovering the model cannot clear the agriculture benchmark or the RAM target. Build the scored model path first, prove it under 2.5 GB at 15 TPS, then wrap HyveGrid Offline around it as a serious local field tool.

---

## 17. Open items to verify before locking the calendar

- Confirm the operating deadline and whether gates exist, via the Devpost schedule page.
- Obtain the agriculture validation set and its format.
- Confirm whether the accuracy evaluation applies any system prompt or chat template to the model, by reading the profiler source or asking the organizers. If it does not, knowledge must live entirely in the weights.
- Confirm the licenses of the final model candidates allow challenge use.
- Line up a native Yoruba speaker for review.
