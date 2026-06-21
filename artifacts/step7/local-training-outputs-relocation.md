# Local Training Outputs Relocation

Date: 2026-06-21
Project: HyveGrid Offline ADTC 2026

Local fine-tune artifacts from Granite QLoRA V2/V3 were moved out of artifacts/ and into the ignored model/ directory.

Reason:

- adapter_model.safetensors, optimizer.pt, scheduler.pt, and training_args.bin are model/training artifacts.
- They should not be committed to the public challenge repo.
- The public repo should keep notes, decisions, benchmark evidence, and reproducible scripts, not local weight artifacts.

Local-only destination:

model/local-training-outputs/
