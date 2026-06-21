# Step 7B Granite 3.3 8B Q3_K_M Verification

Date: 2026-06-20  
Project: HyveGrid Offline ADTC 2026  
Status: source verified, not downloaded yet

---

## Selected candidate

| Field | Value |
|---|---|
| Repo | ibm-granite/granite-3.3-8b-instruct-GGUF |
| File | granite-3.3-8b-instruct-Q3_K_M.gguf |
| License | apache-2.0 |
| Gated | False |
| HEAD status | 200 |
| Download decision | Candidate download allowed for local testing |

---

## Why this candidate

Gemma 3 4B Q4_K_M was rejected because it was slow and jumped to Varroa instead of following the ants and hive-stand evidence.

Qwen3-1.7B Q4_K_M was rejected because it was faster but too shallow.

Granite 3.3 8B Q3_K_M is now tested only as an accuracy-ceiling fallback.

---

## Guardrails

- Do not modify metadata.json yet.
- Do not modify download_model.sh yet.
- Keep GGUF files out of git.
- Use the official IBM Granite GGUF repo first.
- Avoid abliterated, LogDetective, or unclear community variants.
- If answer quality is still shallow, reject quickly.
- Do not run repeated speed tests unless the answer quality justifies it.
