# Local Evaluation Outputs

This folder stores local evaluation outputs from the Granite versus Qwen harness. Raw model outputs are not committed by default.

The harness compares only Granite 3.3 2B Instruct Q4_K_M and Qwen2.5 1.5B Instruct Q4_K_M under two conditions:

- `bare`: the user prompt without the HyveGrid system prompt. This is closest to the ADTC scored path.
- `hyvegrid`: the user prompt with the HyveGrid Offline system prompt.

Keyword scoring is only a first pass. Human review is required before model lock.
