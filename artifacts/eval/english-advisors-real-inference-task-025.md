# Task 025: English advisor real browser inference evidence

Date: 2026-06-25

Starting branch: `phase-1-eval-harness`

Starting HEAD: `08e53da66c72236c84877edfc0e50401aaf05889`

Working tree at start: clean

Runtime path: local web app started with `python3 -m app.web_app`; routes were exercised with browser-style form POSTs using `question=<prompt>`.

## Harvest Quality Coach

Route tested: `POST /advisor/harvest-quality`

Prompt used:

```text
A beekeeper is preparing to harvest honey after a rainy week. Some frames are mostly capped, the smoker was used heavily, and the honey will be stored in plastic buckets. What quality risks should they check before harvesting and storing?
```

HTTP status: 200

Wall time: 184.947516 seconds

Answer rendered: yes

Sources rendered: yes

Top retrieved source: `harvest_quality.md` - `Avoid doing immediately`

Additional retrieved sources:

- `harvest_quality.md` - `Check first`
- `harvest_quality.md` - `Key checks`
- `harvest_quality.md` - `Suggested next step`
- `harvest_quality.md` - `Possible concern`

Short answer excerpt:

```text
The rainy week might have affected the honey's moisture content, potentially leading to uncapped or runny nectar. The use of the smoker heavily could indicate potential brood disturbance, and the use of plastic buckets might introduce contamination risks.
```

Clean-output check: passed. The answer and source area rendered without raw stdout, raw model prompt echo, llama.cpp chrome, traceback, stack trace, internal command details, filesystem paths, or runtime logs. The submitted question appeared only in the normal form textarea/example prompt area.

## Forage & Pollination Guide

Route tested: `POST /advisor/forage-pollination`

Prompt used:

```text
A beekeeper wants to support mango, pepper, and vegetable farms, but there may be a flowering gap after mango season and pesticide spraying nearby. What forage and pollination factors should they evaluate?
```

HTTP status: 200

Wall time: 207.264089 seconds

Answer rendered: yes

Sources rendered: yes

Top retrieved source: `forage_pollination.md` - `Check first`

Additional retrieved sources:

- `forage_pollination.md` - `Key checks`
- `forage_pollination.md` - `When to escalate`
- `forage_pollination.md` - `Possible concern`
- `site_readiness.md` - `Possible concern`

Short answer excerpt:

```text
The beekeeper's colonies may face a flowering gap after mango season, which could lead to a shortage of food and potential colony weakening. Additionally, pesticide spraying near the area might expose the bees to harmful chemicals.
```

Clean-output check: passed. The answer and source area rendered without raw stdout, raw model prompt echo, llama.cpp chrome, traceback, stack trace, internal command details, filesystem paths, or runtime logs. The submitted question appeared only in the normal form textarea/example prompt area.

## Hive Signal Check

Route tested: `POST /advisor/hive-signal`

Prompt used:

```text
A hive shows rising temperature, dropping humidity, low entrance activity, and bees clustering outside in the afternoon. What should the beekeeper check first, and what should they avoid doing immediately?
```

HTTP status: 200

Wall time: 182.483965 seconds

Answer rendered: yes

Sources rendered: yes

Top retrieved source: `hive_signals.md` - `Field use`

Additional retrieved sources:

- `hive_signals.md` - `Key checks`
- `hive_signals.md` - `Possible concern`
- `hive_signals.md` - `Avoid doing immediately`
- `site_readiness.md` - `Check first`

Short answer excerpt:

```text
The combination of rising temperature, dropping humidity, low entrance activity, and bees clustering outside in the afternoon could indicate heat stress, poor ventilation, crowding, or water scarcity.
```

Clean-output check: passed. The answer and source area rendered without raw stdout, raw model prompt echo, llama.cpp chrome, traceback, stack trace, internal command details, filesystem paths, or runtime logs. The submitted question appeared only in the normal form textarea/example prompt area.

## Tests

Commands run after evidence capture:

```bash
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
python3 -m unittest tests/test_web_app.py
```

Result:

- `tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py`: 45 tests passed.
- `tests/test_web_app.py`: 23 tests passed.

Note: `tests/test_web_app.py` emitted an existing `StarletteDeprecationWarning` from `fastapi.testclient`; the suite still passed.

## Boundary confirmation

No app architecture, metadata, model, profiler, retrieval, prompt builder, llama runtime, Yoruba, Guided Hive Walkthrough, cloud/API dependency, or UI refactor changes were made.
