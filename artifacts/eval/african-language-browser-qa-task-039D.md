# Task 039D African Language Browser QA and Reviewer Export

## Current commit reviewed

`2d57874a269638c52be6e93f16d68bbafaeeb3b5`

## Files changed

- `artifacts/eval/african-language-browser-qa-task-039D.md`
- `artifacts/eval/african-language-review-export-task-039D.md`

No app behavior files were changed for this task.

## Browser or rendered-route method used

Rendered-route QA was performed with the existing project test virtual environment and `fastapi.testclient.TestClient`. GET routes were rendered directly. Advisor POST rendering was checked with the same mocked local answer bundle shape used by the focused web suite, so the QA verified the page response, answer area, source cards, and language templates without running a GGUF inference request.

A screenshot was not created because this task did not require adding a browser or screenshot dependency, and rendered-route QA already covered the text and template acceptance criteria.

## Routes/pages inspected

- `/`
- `/?lang=yo`
- `/?lang=ha`
- `/?lang=sw`
- `/advisor/hive-health`
- `/advisor/hive-health?lang=yo`
- `/advisor/hive-health?lang=ha`
- `/advisor/hive-health?lang=sw`
- POST `/advisor/hive-health`
- POST `/advisor/hive-health?lang=ha`
- POST `/advisor/hive-health?lang=sw`

## Language selector labels observed

The selector rendered:

- `English`
- `Yorùbá`
- `Hausa`
- `Swahili`

The rendered routes did not show:

- `Hausa Preview`
- `Swahili Preview`

## English QA result

`PASS`

- English remains the default.
- Advisor routes render.
- The default English advisor POST rendered a completed local-answer page using the focused test mock.
- Retrieved source cards displayed with source file and heading text.
- No structured review-needed note appeared for English.

## Yorùbá QA result

`PASS`

- Yorùbá remains available in the selector.
- Yorùbá was not downgraded to preview.
- Existing Yorùbá labels, controlled templates, glossary behavior, and review-needed note remain available where implemented.
- The Yorùbá advisor route rendered without crashing.

## Hausa QA result

`PASS`

- Hausa appears without `Preview`.
- Hausa shows `Structured field mode. Human language review recommended before field deployment.`
- Hausa uses controlled labels/templates around the English model answer.
- Hausa does not claim human review.
- Hausa does not claim native-quality translation.
- Hausa does not rely on local-model freestyle translation.

## Swahili QA result

`PASS`

- Swahili appears without `Preview`.
- Swahili shows `Structured field mode. Human language review recommended before field deployment.`
- Swahili uses controlled labels/templates around the English model answer.
- Swahili does not claim human review.
- Swahili does not claim native-quality translation.
- Swahili does not rely on local-model freestyle translation.

## Field-safety wording

Rendered Hausa and Swahili structured templates preserve cautious field-language concepts:

- possible concern
- check first
- avoid doing immediately
- confirm by physical inspection
- consult an experienced beekeeper or extension officer when needed

The QA did not find newly introduced claims for:

- certified diagnosis
- guaranteed diagnosis
- digital twin
- autonomous agents
- live sensor simulation
- real-time sensor readings

## Reviewer export

Created:

`artifacts/eval/african-language-review-export-task-039D.md`

The export includes current controlled field-language phrases for:

- Yorùbá
- Hausa
- Swahili

It is formatted as reviewer-editable markdown tables with columns for key, English source, current phrase, reviewer correction, and notes.

## Checks run

- Rendered-route QA script with `/tmp/hyvegrid-task-034b-test-venv/bin/python`: passed.
- `python3 -m unittest tests.test_prompt_builder`: passed.
- `/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app`: passed.
- `python3 -m unittest tests.test_web_app`: failed on bare system Python because FastAPI is not installed in that Python environment. The focused web suite passed in the existing project test virtual environment.

## Static and safety confirmations

- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- Runtime path files were not changed.
- No cloud API, CDN, Phaser, WebGL, canvas, Remotion, remote asset, external service, or external runtime dependency was added.
- No proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims were added.
- `artifacts/source/` was not committed.

## Visual or text issues found

No blocking visual or text issues were found. Hausa and Swahili intentionally retain some English structural labels such as `Reported observation`, `Suggested next step`, and `English model answer` because this task exports the current controlled phrase layer for human review rather than inventing a larger translation set.

## Final status

`AFRICAN_LANGUAGE_BROWSER_QA_AND_REVIEW_EXPORT_READY`
