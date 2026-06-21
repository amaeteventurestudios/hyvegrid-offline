# Step 12 Profiler Smoke Summary

Date: 2026-06-21
Project: HyveGrid Offline ADTC 2026

## Result

The ADTC profiler smoke run completed successfully in participant mode with accuracy skipped.

Profiler command:

adtc-profiler run --submission . --mode participant --output artifacts/step12/submission-smoke-skip-accuracy.json --seed 42 --skip-accuracy

## Key metrics

- Model path: model.gguf
- Model: Granite 3.3 2B Instruct Q4_K_M
- Generation throughput: 3.09 tokens/second
- First token latency: 15423.77 ms
- Peak RSS: 1722.2 MB
- Steady RSS: 1638.4 MB
- CPU p99: 93.3%
- Thermal throttled: false
- Accuracy: skipped for smoke run

## Path correction

The profiler expects the model at root path model.gguf. download_model.sh was updated to create model.gguf directly and verify SHA256.

## Next step

Run the full participant profiler with accuracy enabled after confirming the accuracy task dependencies are available.
