# Phi-4 Mini Instruct Smoke Benchmark

## Candidate

* Model ID: `phi-4-mini-instruct-q4-k-m`
* GGUF filename: `Phi-4-mini-instruct-Q4_K_M.gguf`
* Source repo: `unsloth/Phi-4-mini-instruct-GGUF`
* Quantization: Q4_K_M
* File size: 2.4 GiB as reported by `ls -lh` (2.31 GiB reported by `llama-bench`)

## Environment

* OS: Ubuntu 22.04, Linux kernel 6.8.0-124-generic, x86_64
* CPU cores visible: 4
* RAM visible: 6.7 GiB, with 2.0 GiB swap configured
* llama.cpp binary path: `/home/amaete/llama.cpp/build/bin/llama-bench`
* llama.cpp CLI path: `/home/amaete/llama.cpp/build/bin/llama-cli`
* Branch: `phase-1-eval-harness`
* Commit tested: `989215c5cd49c4bac85a8083e752bdcbdd8ffae4`

## Benchmark result

Command used:

```text
/home/amaete/llama.cpp/build/bin/llama-bench -m model/phi-4-mini-instruct-q4_k_m.gguf -p 512 -n 128 -t 4
```

GNU `time -v` wrapped the command to record process memory and elapsed time.

* Prompt processing: 14.12 ± 2.86 tokens/second (`pp512`)
* Generation: 5.77 ± 1.30 tokens/second (`tg128`)
* Peak RSS: 3,822,004 KB, approximately 3.65 GiB
* Approximate runtime: 5 minutes 50 seconds
* Timeout, crash, or OOM: none
* Process swaps: 0
* Notes: The benchmark completed with exit status 0. Phi is slower and heavier than the existing Granite and Qwen candidates, but it completed within the visible VM resources.

## Two-prompt smoke result

Prompts run:

* `hive-triage-01`
* `site-readiness-01`

Results:

* Both raw outputs were captured successfully.
* `hive-triage-01`: return code 0; 1,667 stdout characters; 2,316-byte raw capture.
* `site-readiness-01`: return code 0; 3,768 stdout characters; 4,446-byte raw capture.
* Timeouts or harness failures: none.
* Approximate combined harness runtime: 2 minutes 20 seconds.

First-read quality notes:

* The hive-triage answer advises against immediate strong chemical treatment, but it over-focuses on Varroa mites, associates the ant observation with Varroa without adequate support, and suggests acid treatments before giving a sufficiently broad physical inspection checklist. It misses several important checks, including colony strength, food stores, and fuller brood-pattern assessment.
* The site-readiness answer is more relevant. It covers pesticide exposure, forage seasonality, water access, neighboring farms, weather, pests, and farm practices. It does not clearly address a dry-season water backup, coordination on spray timing, safety around people or livestock, drainage, access, or whether 20 hives exceed local forage capacity.
* These two outputs are insufficient to conclude that Phi is more accurate than Granite.

## Preliminary decision

**Viable for full bare evaluation.**

Phi completed the benchmark and both prompt runs without a timeout, crash, or OOM. Its measured peak RSS and generation speed are technically workable on this VM, although materially less efficient than the current candidates. The mixed first-read answer quality means viability should not be interpreted as an accuracy win. A full bare evaluation and the same human-review process are required before any model-lock decision.
