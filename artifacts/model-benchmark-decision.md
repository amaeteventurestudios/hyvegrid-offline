# HyveGrid Offline Model Benchmark Decision

Benchmark environment:
- VMware Fusion on Intel iMac
- Ubuntu 22.04.5 LTS x86-64
- 4 CPU cores
- 6.7 GB RAM visible
- llama.cpp CPU runtime
- ADTC profiler participant mode, skip accuracy

Current baseline:
- Granite 3.3 2B Instruct Q4_K_M
- Generation TPS: 10.67
- First-token latency: 11938.55 ms
- Peak RSS: 2736.61 MB
- Steady RSS: 2627.84 MB
- Thermal throttled: false

Comparison summary:
- Qwen2.5 1.5B Q4_K_M was fastest at 16.64 TPS and 1694.62 MB peak RSS, but gave weaker HyveGrid apiculture/site-readiness answers.
- Qwen2.5 1.5B Q5_K_M was near target speed at 14.95 TPS and low RAM, but did not improve answer quality.
- Gemma 2 2B Q4_K_M was slower than Granite.
- Gemma 3 4B Q4_K_M was too slow and too memory-heavy for the scored model path.

Decision:
Keep Granite 3.3 2B Instruct Q4_K_M as the baseline model for now. Stop model hopping unless a clearly stronger agriculture/apiculture candidate is identified.
