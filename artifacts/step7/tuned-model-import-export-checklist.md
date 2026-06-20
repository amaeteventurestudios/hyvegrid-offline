# Tuned Model Import and Export Checklist

## Purpose

This checklist defines what happens after a development-only fine-tune experiment produces a tuned HyveGrid model candidate.

The goal is to bring the tuned model back into the local repo, convert it to GGUF, quantize it, test it offline, and compare it against the Gemma and Granite baselines.

This checklist is not a model lock.

## Runtime boundary

Training may happen in a development-only GPU environment.

The judged ADTC runtime must remain:

- offline
- local
- GGUF
- llama.cpp
- no cloud dependency
- no external API dependency

## Expected development outputs

After the notebook experiment, collect:

- LoRA adapter directory, if adapter-only training was used
- merged model directory, if adapter was merged into base
- tokenizer files
- config files
- training logs
- quick eval outputs
- notes on training settings

## Local ignored folder

Place downloaded training outputs under an ignored local folder such as:

artifacts/local-training-outputs/

These files may be large and should not be committed unless they are small text reports.

Model weights, adapters, checkpoints, and GGUF files must stay out of git.

## Import checklist

Before conversion:

- [ ] Confirm the tuned output came from the public HyveGrid dataset only.
- [ ] Confirm no private field records were included.
- [ ] Confirm no proprietary hardware, sensor IP, firmware, partner strategy, or commercial roadmap entered the training data.
- [ ] Confirm model license is acceptable for challenge use.
- [ ] Confirm files include tokenizer/config material needed for conversion.
- [ ] Save training settings in a small text report.
- [ ] Save quick eval outputs in a small text report.

## Merge checklist

If the output is adapter-only:

- [ ] Load base Granite model.
- [ ] Load LoRA adapter.
- [ ] Merge adapter into base model if required.
- [ ] Save merged Hugging Face model directory.
- [ ] Test the merged model with a small prompt before GGUF conversion.

If the output is already a merged model:

- [ ] Verify it loads locally or in a notebook.
- [ ] Verify tokenizer loads correctly.
- [ ] Run one quick official prompt test.

## GGUF conversion checklist

After a merged model exists:

- [ ] Clone or use local llama.cpp tools.
- [ ] Convert merged Hugging Face model to GGUF.
- [ ] Save unquantized GGUF under model/ or another ignored model folder.
- [ ] Quantize to Q4_K_M first.
- [ ] Optionally test Q5_K_M only if RAM allows.
- [ ] Do not commit GGUF files.

## Local test checklist

After quantization:

- [ ] Run llama.cpp with the tuned GGUF.
- [ ] Test official prompt 1.
- [ ] Test official prompt 2.
- [ ] Check for unsafe advice.
- [ ] Check that answer style includes possible concern, check first, avoid doing immediately, and physical inspection where needed.
- [ ] Check that the model does not expose hidden reasoning or ramble.

## Profiler checklist

Run ADTC profiler smoke test:

adtc-profiler run --submission . --mode participant --output artifacts/tuned-candidate-profiler.json --skip-accuracy

Record:

- peak RSS
- steady RSS
- tokens per second
- first-token latency
- CPU p99
- thermal status
- crash or OOM status

## Benchmark checklist

Run the same benchmark process used for base models:

- Step 5 official prompt benchmark
- Step 7 held-out eval split benchmark
- proxy validation prompt set, if available

Compare tuned model against:

- Granite base
- Gemma base

## Acceptance rule

Accept the tuned candidate only if it clearly improves accuracy and safety enough to justify any speed or RAM cost.

Reject the tuned candidate if it:

- gives unsafe beekeeping advice
- fails official prompt variants
- overfits the training examples
- loses general agriculture usefulness
- cannot convert cleanly to GGUF
- becomes too slow
- uses too much RAM
- requires cloud runtime

## Final output if candidate passes

If the tuned model passes:

- update model candidate matrix
- create tuned model decision note
- update metadata model fields only after model lock
- update download_model.sh only after model lock
- run final profiler smoke check
- continue to Step 8 quantization comparison

## Current status

No tuned model is locked yet.

The next action is to prepare the first Granite QLoRA experiment and collect training outputs for this checklist.
