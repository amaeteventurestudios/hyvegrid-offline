# Step 7 Training Route Decision

## Decision

Do not fine-tune locally on the current iMac.

Use the iMac for repository work, dataset preparation, llama.cpp testing, benchmark harnesses, and offline GGUF runtime checks.

Use a development-only GPU environment for the first fine-tune experiment, then bring the tuned output back into this repo for GGUF conversion, quantization, profiling, and offline testing.

## Machine check

Current machine:

- Architecture: x86_64
- Operating system: macOS 12.7.6
- Python: 3.9.6
- CPU: Intel Core i7-6700K CPU @ 4.00GHz
- RAM: 34 GB
- Free disk: about 68 GB

## Why local training is not the right route

The machine has enough RAM for project work, but it is an Intel Mac without an NVIDIA GPU and without Apple Silicon.

This makes it suitable for:

- Python scripts
- dataset validation
- llama.cpp local inference
- profiler smoke checks
- repo management

It is not suitable for efficient LoRA or QLoRA fine-tuning.

## First training route

Preferred route:

- Development-only GPU notebook or rented GPU environment.
- Train a small Granite adapter or tuned checkpoint.
- Export the adapter/checkpoint.
- Bring the result back into the repo.
- Convert to GGUF.
- Quantize to Q4_K_M first.
- Run local offline llama.cpp tests.

## Base candidate

Primary fine-tune candidate:

- Granite-3.3-2B-Instruct

Reason:

- Current efficiency baseline.
- Lower peak RAM than Gemma in profiler smoke test.
- Faster than Gemma in profiler smoke test.
- Suitable first candidate for public HyveGrid apiculture specialization.

## Hard boundary

The final judged runtime must not depend on the training environment.

Training may happen outside the judged runtime, but the submitted runtime must remain:

- local
- offline
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency
- no private data
- no proprietary hardware or sensor IP

## Success criteria

The tuned candidate must beat the base model on:

- two official HyveGrid prompts
- Step 7 eval split
- safety and caution language
- profiler RAM
- throughput
- GGUF conversion compatibility

## Current next step

Create a development-only fine-tune notebook plan for Granite.

Do not start app, RAG, Yoruba, or UI work yet.
