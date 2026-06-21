# Step 7B Qwen3-1.7B Q4_K_M Verification

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Status: source verified, not downloaded yet

---

## Selected candidate

| Field | Value |
|---|---|
| Repo | unsloth/Qwen3-1.7B-GGUF |
| File | Qwen3-1.7B-Q4_K_M.gguf |
| License | apache-2.0 |
| Gated | False |
| HEAD status | 200 |
| Download decision | Candidate download allowed for local testing |

---

## Rejected or deferred Qwen sources

| Source | Reason |
|---|---|
| Qwen/Qwen3-1.7B | base model, no GGUF files |
| Qwen/Qwen3-1.7B-GGUF | Apache 2.0 and ungated, but only Q8_0 GGUF shown |
| enacimie/Qwen3-1.7B-Q4_K_M-GGUF | Apache 2.0 and ungated, but includes split files. Keep as fallback |

---

## Why Qwen3-1.7B is next

Gemma 3 4B Q4_K_M was rejected because it was slower than Granite and failed the official hive-health prompt by jumping to Varroa instead of following the ants and hive-stand evidence.

Qwen3-1.7B Q4_K_M is the speed-lane candidate. It should use less memory than Gemma 3 4B and may still give better structured answers than Granite 2B.

---

## Guardrails

- Do not modify metadata.json yet.
- Do not modify download_model.sh yet.
- Keep GGUF files out of git.
- Use this candidate only for Step 7B answer quality and llama.cpp benchmark testing.
- If Qwen3-1.7B fails content quality, do not tune wrappers endlessly. Move to the next candidate.
