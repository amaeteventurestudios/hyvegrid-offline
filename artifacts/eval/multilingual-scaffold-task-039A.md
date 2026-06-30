# Task 039A Multilingual Scaffold Audit

## Files Changed

- `app/web_app.py`
- `app/templates/base.html`
- `app/templates/advisor_form.html`
- `app/templates/index.html`
- `tests/test_web_app.py`
- `artifacts/eval/multilingual-scaffold-task-039A.md`

## Existing Language Behavior Found

The app already had an English default path and a Yorùbá UI layer. Yorùbá used
controlled labels, a glossary, review-note copy, and English model-answer
fallback. The prompt builder still supports English prompts only, so the app
does not ask the local model to freestyle non-English answers.

## English Behavior Preserved

English remains the default language. Existing advisor submission and local
runtime behavior are unchanged.

## Yorùbá Support Preserved

Yorùbá remains the primary supported African language layer for the public
challenge edition. Existing Yorùbá labels, controlled response templates,
glossary entries, and the Yorùbá review note were preserved.

## Hausa Preview Scaffold Added

Hausa now appears in the shared language selector as:

```text
Hausa Preview
```

The Hausa preview route renders controlled English-safe labels around the
English local model answer. It includes this limitation note:

```text
Hausa preview. Key field guidance is structured, but full Hausa language review is still needed.
```

## Swahili Preview Scaffold Added

Swahili now appears in the shared language selector as:

```text
Swahili Preview
```

The Swahili preview route renders controlled English-safe labels around the
English local model answer. It includes this limitation note:

```text
Swahili preview. Key field guidance is structured, but full Swahili language review is still needed.
```

## Glossary And Template Entries Added

Preview placeholder glossary entries were added for Hausa and Swahili. These are
explicitly placeholders with controlled preview labels, not reviewed full
translations.

Preview controlled labels include:

- `Reported observation`
- `Possible concern`
- `Check first`
- `Avoid doing immediately`
- `Suggested next step`
- `When to consult`

## Limitations

- Hausa is preview only.
- Swahili is preview only.
- Neither preview mode claims completed translation quality, human review, or
  full field-support coverage.
- The local model answer remains English in preview modes.
- Prompt-builder language support remains English-only.

## Confirmations

- Hausa and Swahili are marked as preview only.
- No full-support claim was added for Hausa.
- No full-support claim was added for Swahili.
- No GGUF model files were changed.
- Model selection was not changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- No scoring files were changed.
- llama.cpp runtime behavior was not changed.
- Local inference path was not changed.
- No cloud API, external service, remote runtime dependency, CDN, Phaser, WebGL,
  canvas, Remotion, internet dependency, generated art, animation, or remote
  asset was added.

## Tests Run

Prompt builder tests:

```text
python3 -m unittest tests.test_prompt_builder
Ran 17 tests in 0.039s
OK
```

Focused web suite in the project preview venv:

```text
/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app
Ran 43 tests in 0.478s
OK
```

Bare system Python web command:

```text
python3 -m unittest tests.test_web_app
```

Result: expected local environment failure before tests ran because the system
Python environment does not have `fastapi` installed.

## Local Server Smoke Check

Started the app locally on port `8019` with the existing preview venv and fetched
these routes with Python standard library HTTP:

- `/`
- `/?lang=yo`
- `/?lang=ha`
- `/?lang=sw`
- `/advisor/hive-health?lang=ha`
- `/advisor/hive-health?lang=sw`

Confirmed:

- English option is visible.
- Yorùbá option is visible.
- Hausa appears as Preview.
- Swahili appears as Preview.
- Preview language routes render without crashing.
- Advisor pages still render the local guidance waiting state.

The full live model submission was not repeated in this task to avoid an
unnecessary inference run; Task 038D already recorded local browser answer
generation success.

## Final Status

MULTILINGUAL_SCAFFOLD_READY
