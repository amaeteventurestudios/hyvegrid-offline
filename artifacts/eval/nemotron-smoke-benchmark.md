# NVIDIA Nemotron 3 Nano 4B Smoke Benchmark

## Candidate

* Model ID: `nvidia-nemotron-3-nano-4b-q4-k-m`
* GGUF filename: `NVIDIA-Nemotron-3-Nano-4B-Q4_K_M.gguf`
* Source repo: `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`
* Quantization: Q4_K_M
* File size: 2,837,072,864 bytes; 2.7 GiB as reported by `ls -lh` and 2.63 GiB as reported by `llama-bench`

## Environment

* OS: Ubuntu 22.04, Linux kernel 6.8.0-124-generic, x86_64
* CPU cores visible: 4
* RAM visible: 6.7 GiB, with 2.0 GiB swap configured
* llama.cpp benchmark path: `/home/amaete/llama.cpp/build/bin/llama-bench`
* llama.cpp CLI path: `/home/amaete/llama.cpp/build/bin/llama-cli`
* Branch: `phase-1-eval-harness`
* Commit tested: `f3ce0c7b873650e8c6baafef6c19b495c10ec3cc`

## Benchmark result

Command used:

```text
/usr/bin/time -v /home/amaete/llama.cpp/build/bin/llama-bench -m model/nvidia-nemotron-3-nano-4b-q4_k_m.gguf -p 512 -n 128 -t 4
```

* Prompt processing: 8.32 ± 1.83 tokens/second (`pp512`)
* Generation: 3.06 ± 0.58 tokens/second (`tg128`)
* Peak RSS: 3,527,700 KB, approximately 3.36 GiB
* Runtime: 10 minutes 13.64 seconds
* Timeout, crash, or OOM: none
* Process swaps: 0

The model fits within the visible VM memory, but generation throughput is materially below the 5 tokens/second skepticism threshold and below the measured Phi smoke result.

## Two-prompt smoke result

Prompts run:

* `hive-triage-01`
* `site-readiness-01`

Results:

* Both raw outputs were captured successfully.
* `hive-triage-01`: return code 0; 2,644 stdout characters; 3,313-byte raw capture.
* `site-readiness-01`: return code 0; 3,349 stdout characters; 4,071-byte raw capture.
* Timeouts or harness failures: none.
* Approximate combined harness runtime: 5 minutes 20 seconds.

First-read quality notes:

* Both outputs expose internal `[Start thinking]` and `[End thinking]` text. That is unsuitable for the current scored answer path and consumes part of the fixed generation budget.
* The hive-triage answer focuses narrowly on ant “sabotage,” ant damage, and queen presence. It advises against feeding because it may attract ants, but it misses a broader inspection of colony strength, food and water stress, brood condition, ant access points, and cautious confirmation before attributing a cause. It is clearly weaker than Granite's human-reviewed inspection-first guidance.
* The site-readiness answer begins a structured and relevant checklist covering pesticide drift, water contamination, and water reliability. However, visible reasoning consumes output space and the answer truncates early, before it can address the full placement problem. It does not demonstrate sufficient coverage of forage seasonality, 20-hive carrying capacity, human or livestock safety, shade, wind, drainage, access, and spray coordination within the captured response.

## Preliminary decision

**Not viable because answer quality is too weak.**

Nemotron completed the benchmark and both prompts without an OOM or timeout, and its approximately 3.36 GiB peak RSS is acceptable. However, its 3.06 tokens/second generation rate is below the stated threshold, both answers expose internal reasoning, and the two captured answers are clearly weaker than Granite's reviewed field guidance. A full 10-prompt bare evaluation is not justified for the current model and llama.cpp configuration.
