# Task 029: Yoruba advisor flow smoke test evidence

Date/time of run: 2026-06-25 16:11:31 PDT

Starting branch: `phase-1-eval-harness`

Current commit before Task 029: `0163b3566383812c7a5793972874cd4908d84f80`

Working tree at start: clean

Runtime path: local web app started with `python3 -m app.web_app`. Evidence used localhost HTTP requests only. One real Yoruba-mode Hive Health Advisor POST was submitted; no other advisor POST inference was run.

## GET Route Smoke Results

| Route | HTTP status | Wall time | Result |
| --- | ---: | ---: | --- |
| `GET /` | 200 | 0.026337 seconds | English default rendered |
| `GET /?lang=yo` | 200 | 0.044554 seconds | Yoruba Mission Control rendered |
| `GET /status?lang=yo` | 200 | 0.051646 seconds | Yoruba Offline System Status rendered |
| `GET /advisor/hive-health?lang=yo` | 200 | 0.020572 seconds | Yoruba Hive Health Advisor rendered |
| `GET /advisor/site-readiness?lang=yo` | 200 | 0.001670 seconds | Yoruba Site Readiness Advisor rendered |
| `GET /advisor/harvest-quality?lang=yo` | 200 | 0.002076 seconds | Yoruba Harvest Quality Coach rendered |
| `GET /advisor/forage-pollination?lang=yo` | 200 | 0.002166 seconds | Yoruba Forage & Pollination Guide rendered |
| `GET /advisor/hive-signal?lang=yo` | 200 | 0.002563 seconds | Yoruba Hive Signal Check rendered |

## Language Dropdown Verification

English default was verified on `GET /`:

- English option selected: `<option value="/" selected>English</option>`
- Yoruba option points to same page with `?lang=yo`: `<option value="/?lang=yo" >Yorùbá</option>`
- English mode does not require `?lang=yo`.

Yoruba selected state was verified on every Yoruba GET page:

- Mission Control: `<option value="/?lang=yo" selected>Yorùbá</option>`
- Status: `<option value="/status?lang=yo" selected>Yorùbá</option>`
- Hive Health: `<option value="/advisor/hive-health?lang=yo" selected>Yorùbá</option>`
- Site Readiness: `<option value="/advisor/site-readiness?lang=yo" selected>Yorùbá</option>`
- Harvest Quality: `<option value="/advisor/harvest-quality?lang=yo" selected>Yorùbá</option>`
- Forage & Pollination: `<option value="/advisor/forage-pollination?lang=yo" selected>Yorùbá</option>`
- Hive Signal: `<option value="/advisor/hive-signal?lang=yo" selected>Yorùbá</option>`

Same-page language switching was verified on representative pages:

- `/`: English option `/`; Yoruba option `/?lang=yo`
- `/?lang=yo`: English option `/`; Yoruba option `/?lang=yo`
- `/status?lang=yo`: English option `/status`; Yoruba option `/status?lang=yo`
- `/advisor/hive-health?lang=yo`: English option `/advisor/hive-health`; Yoruba option `/advisor/hive-health?lang=yo`

Hausa and Swahili were not active dropdown options. No external JavaScript package was used; the selector uses local inline navigation on the selected option URL.

## Yoruba Labels, Glossary, and Review Note

Yoruba labels were verified on the rendered pages, including:

- `Ibi Ìṣàkóso`
- `Ipò Ẹ̀rọ Àìsí Ayélujára`
- `Olùrànlọ́wọ́ Ìlera Ilé Oyin`
- `Béèrè lórí kọ̀ǹpútà yìí`
- `Àkójọ ọ̀rọ̀ pápá Yorùbá`

The Yoruba glossary appeared on Mission Control and advisor pages in Yoruba mode. The human review note appeared on each Yoruba page:

```text
Yoruba field labels and templates are controlled draft support and should be reviewed by a fluent Yoruba speaker before final submission.
```

## Real Yoruba-Mode Advisor POST

Route:

```text
POST /advisor/hive-health?lang=yo
```

Prompt used:

```text
Low hive activity, ants near the hive stand, normal smell, and partially capped brood.
```

HTTP status: 200

Wall time: 293.172773 seconds

Controlled Yoruba template headings appeared:

- `Àwọn template ìtọ́nisọ́nà Yorùbá`
- `Àkótán ohun tí a rí ní pápá`
- `Ohun tó lè jẹ́ ìṣòro`
- `Ṣàyẹ̀wò èyí kọ́kọ́`
- `Má ṣe èyí lẹ́sẹ̀kẹsẹ̀`
- `Ìgbésẹ̀ àìléwu tó kàn`
- `Bèrè lọ́wọ́ agbẹ oyin tó ní ìrírí tàbí òṣiṣẹ́ ìtẹ̀síwájú agbẹ`
- `Àkọsílẹ̀ ìpadà sí Gẹ̀ẹ́sì`

English fallback model answer appeared under:

```text
Ìdáhùn módẹ́lì ní Gẹ̀ẹ́sì
```

Retrieved sources appeared under:

```text
Àwọn orísun tí a rí
```

Retrieved source entries included:

- `hive_health.md` - `Possible concern`
- `hive_health.md` - `Field use`
- `hive_health.md` - `Check first`
- `hive_health.md` - `Key checks`
- `hive_health.md` - `Suggested next step`

Runtime tag: `Completed locally.`

## Clean-Output Check

The saved GET and POST responses did not contain traceback text, internal server error text, Python stack traces, Jinja undefined errors, raw stdout/stderr, internal filesystem paths, or llama.cpp runtime log text.

## Tests

Commands run:

```bash
python3 -m unittest tests/test_web_app.py
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
```

Results:

- `tests/test_web_app.py`: 28 tests passed.
- `tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py`: 45 tests passed.

Note: `tests/test_web_app.py` emitted the existing `StarletteDeprecationWarning` from `fastapi.testclient`; the suite still passed.

## Limitations

- Yoruba labels and templates are controlled draft support.
- Human Yoruba review is still required before final submission.
- Hausa and Swahili are not implemented.
- No animation or visual redesign is included.
- Only one real Yoruba-mode advisor POST was run for Task 029; this keeps evidence bounded because Task 028 and Task 028A already covered template behavior and web tests.

## IP and Compliance Note

Task 029 made no source-code changes. It added evidence only.

No proprietary hardware plans, sensor IP, firmware strategy, private datasets, partner strategy, commercial roadmap, Honey Flow Africa internal strategy, investor materials, or patent-sensitive claims were added.

No cloud dependency was added. No `metadata.json`, model files, `download_model.sh`, llama.cpp runtime integration, profiler artifacts, retrieval logic, prompt builder, Hausa, Swahili, visual redesign, or animation work was changed.
