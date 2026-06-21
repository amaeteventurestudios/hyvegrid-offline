# Qwen3-1.7B Q4_K_M Raw Completion Failure

Date: 2026-06-20  
Candidate: `unsloth/Qwen3-1.7B-GGUF / Qwen3-1.7B-Q4_K_M.gguf`

## What happened

The model loaded successfully in `llama-completion`, but raw completion mode produced an unrelated repeated phrase:

> What is the correct term for the process of removing the queen from the hive?

## Interpretation

This is not a Mac performance problem. It is an inference-mode problem.

Qwen3-1.7B is an instruct/chat model and likely needs the chat template. Raw completion mode is not a fair quality test for this candidate.

## Next action

Retest with `llama-cli` using chat mode plus `--single-turn`, so the model uses its chat template and exits after one answer.
