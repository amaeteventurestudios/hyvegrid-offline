# Step 7B Gemma 3 4B IT Q4_K_M Verification

Date: 2026-06-20
Project: HyveGrid Offline ADTC 2026
Status: source verified, not downloaded yet

## Selected candidate

| Field | Value |
|---|---|
| Repo | ggml-org/gemma-3-4b-it-GGUF |
| File | gemma-3-4b-it-Q4_K_M.gguf |
| License tag | gemma |
| Gated | False |
| HEAD status | 200 |
| Download decision | Candidate download allowed for local testing |

## Rejected or deferred sources

| Source | Reason |
|---|---|
| google/gemma-3-4b-it | gated manual, no GGUF file |
| google/gemma-3-4b-it-qat-q4_0-gguf | gated manual, target file returned 401 |
| bartowski/google_gemma-3-4b-it-GGUF | ungated, but license field was None |
| bartowski/google_gemma-3-4b-it-qat-GGUF | fallback only, not first candidate |
| Aldaris/gemma-3-4b-it-Q4_K_M-GGUF | tested target filename returned 404 |

## Guardrails

- Do not modify metadata.json yet.
- Do not modify download_model.sh yet.
- Keep GGUF files out of git.
- Use this candidate only for Step 7B answer quality and llama.cpp benchmark testing.
- License compatibility must remain documented before any final lock.
