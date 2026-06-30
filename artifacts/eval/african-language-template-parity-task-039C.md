# Task 039C African Language Template Parity

## Current commit reviewed

`121091ce7963fef8df514fadf57bea3e9c48bbee`

## Task summary

Task 039C moves Hausa and Swahili from preview scaffold labeling into structured field-template mode while keeping English as the default and preserving the existing Yorùbá language layer. Hausa and Swahili now use controlled labels and fixed local UI/template phrases instead of asking the local model to freestyle full Hausa or Swahili translation.

## Files changed

- `app/web_app.py`
- `app/templates/advisor_form.html`
- `app/templates/index.html`
- `tests/test_web_app.py`
- `artifacts/eval/african-language-template-parity-task-039C.md`

## Existing language behavior found

- English was already the default language.
- Yorùbá already used controlled field labels, glossary entries, and a review-needed note.
- Hausa and Swahili were previously exposed as preview scaffolds with preview badges and limited framing.
- The advisor form already supported language-specific rendering and local answer display without changing model selection or runtime behavior.

## Changes made

- Main language selector labels are now `English`, `Yorùbá`, `Hausa`, and `Swahili`.
- Hausa and Swahili no longer appear as `Preview` in the main selector or advisor language controls.
- Hausa and Swahili now show the visible note: `Structured field mode. Human language review recommended before field deployment.`
- Hausa and Swahili structured field phrase packs were added for cautious field sections, waiting-state labels, local source labels, and local completion wording.
- Hausa and Swahili structured answer framing continues to wrap the English model answer with controlled labels and review guidance.
- Advisor waiting-state text now uses structured phrase packs for Hausa and Swahili where available.

## English behavior preserved

English remains the default. The default advisor answer flow, local runtime call, source rendering, and submit behavior are unchanged.

## Yorùbá behavior preserved

Yorùbá remains the primary supported African language layer. Existing Yorùbá labels, glossary entries, controlled template behavior, and review-needed note were preserved.

## Hausa structured field-template mode

Hausa now includes controlled phrase entries for:

- `possible_concern`
- `check_first`
- `avoid_immediately`
- `confirm_physical_inspection`
- `consult`
- `preparing_local_guidance`
- `working_locally`
- `no_cloud_access`
- `manual_observations`
- `sample_edge_signal_inputs`
- `local_apiculture_notes`
- `local_gguf_model`
- `offline_mode`
- `completed_locally`

All Hausa phrase-pack entries are marked `review_needed: true`.

## Swahili structured field-template mode

Swahili now includes controlled phrase entries for:

- `possible_concern`
- `check_first`
- `avoid_immediately`
- `confirm_physical_inspection`
- `consult`
- `preparing_local_guidance`
- `working_locally`
- `no_cloud_access`
- `manual_observations`
- `sample_edge_signal_inputs`
- `local_apiculture_notes`
- `local_gguf_model`
- `offline_mode`
- `completed_locally`

All Swahili phrase-pack entries are marked `review_needed: true`.

## Limitations

Hausa and Swahili are structured field-template modes only. They are not represented as human-reviewed, native-quality, or fully supported language modes. Full human language review is recommended before field deployment.

## Static and safety confirmations

- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- Runtime path behavior was not changed.
- Retrieval logic was not changed.
- Prompt-builder logic was not changed.
- No cloud API, CDN, Phaser, WebGL, canvas, Remotion, remote image, or external runtime dependency was added.
- The app remains offline and local.

## Test results

- `python3 -m py_compile app/web_app.py`: passed.
- `python3 -m unittest tests.test_prompt_builder`: passed, `Ran 17 tests in 0.038s OK`.
- `/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app`: passed, `Ran 44 tests in 0.942s OK`.
- `python3 -m unittest tests.test_web_app`: failed on bare system Python because `fastapi` is not installed in that Python environment. The focused web suite passed in the existing project test virtual environment.

## Rendered smoke check

A fresh local server was started on `127.0.0.1:8032` with the existing project test virtual environment. These routes rendered successfully:

- `/`
- `/?lang=ha`
- `/?lang=sw`
- `/advisor/hive-health?lang=ha`
- `/advisor/hive-health?lang=sw`

The rendered pages included the structured review note, controlled Hausa and Swahili labels, and no `Hausa Preview` or `Swahili Preview` labels.

## Final status

`AFRICAN_LANGUAGE_TEMPLATE_PARITY_READY`
