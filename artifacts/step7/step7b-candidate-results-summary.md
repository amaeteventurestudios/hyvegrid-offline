# Step 7B Candidate Results Summary

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Status: Step 7B candidate branch complete

---

## Candidates tested

| Candidate | Size | Speed signal | Quality signal | Decision |
|---|---:|---:|---|---|
| Gemma 3 4B IT Q4_K_M | 2.3 GB | 2.62 t/s | Jumped to Varroa, missed ants/stand/brood details | Reject |
| Qwen3-1.7B Q4_K_M | 1.0 GB | 6.0 t/s | Too generic, missed almost all required apiculture details | Reject |
| Granite 3.3 8B Q3_K_M | 3.7 GB | 0.8 t/s | Jumped to Varroa/AFB, missed ants/stand/brood details | Reject |

---

## Main finding

None of the Step 7B candidates beat the practical scoring tradeoff.

- Gemma 3 4B was larger and slower but still wrong on the official hive-health prompt.
- Qwen3-1.7B was faster but too shallow.
- Granite 8B was far too slow and still wrong on the official hive-health prompt.

---

## Decision

Stop Step 7B candidate testing.

Do not lock Gemma 3 4B, Qwen3-1.7B, or Granite 8B.

Do not keep looping on wrappers.

Return to the scoring strategy with evidence:

1. Keep Granite 2B and Gemma 2B as known baselines.
2. Consider whether a small targeted fine-tune should be tried on a better base or whether the public challenge should lock the least-bad efficient base.
3. Do not start UI, RAG, Yoruba, or app work until the scoring model path is decided.
