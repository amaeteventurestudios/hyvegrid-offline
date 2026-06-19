# HyveGrid Offline Tasks

## Phase 1: Compliance and planning

- [x] Create repo skeleton
- [x] Add SCORING.md
- [x] Add v2 build plan to `specs/001-hyvegrid-offline/plan.md`
- [x] Add model candidate matrix
- [x] Add starter `metadata.json`
- [x] Add starter `download_model.sh`
- [x] Add starter `README.md`
- [x] Add starter `REPORT.md`
- [ ] Validate metadata JSON
- [ ] Make first Git commit

## Phase 2: Scored model path

- [ ] Find 3 to 5 current small GGUF candidate models
- [ ] Verify each model license
- [ ] Add each candidate to `artifacts/model-candidate-matrix.md`
- [ ] Obtain official agriculture validation set or build a faithful proxy
- [ ] Build local prompt scoring harness
- [ ] Download smallest candidate
- [ ] Run first profiler test
- [ ] Record peak RAM, TPS, first-token latency, crash/OOM status
- [ ] Run Prompt 1 and Prompt 2 against candidate
- [ ] Score Prompt 1 and Prompt 2 manually
- [ ] Repeat for each model candidate
- [ ] Decide whether base model is enough or fine-tuning is needed
- [ ] Lock scoring model
- [ ] Update `metadata.json` with final model fields
- [ ] Update `download_model.sh` with final GGUF URL

## Phase 3: Demo field product layer

Do not start until the scoring model is locked.

- [ ] Build CLI engine
- [ ] Add public apiculture notes
- [ ] Add SQLite FTS5 retrieval
- [ ] Add structured hive inspection flow
- [ ] Add site readiness flow
- [ ] Add harvest quality flow
- [ ] Add forage and pollination flow
- [ ] Add sample edge-signal input flow
- [ ] Add Yoruba controlled templates
- [ ] Add local web UI
- [ ] Add Offline System Status screen

## Phase 4: Final packaging

- [ ] Run profiler on constrained profile
- [ ] Record benchmark numbers in `REPORT.md`
- [ ] Record model decision in `artifacts/model-candidate-matrix.md`
- [ ] Run clean clone audit
- [ ] Run offline test
- [ ] Scan repo and Git history for private material
- [ ] Record demo video
- [ ] Submit locked commit