# Task 040A Final Advisor Flow QA

## Current commit reviewed

`f6ab03576fb95b4e2d514e28ff39dbc1ebc4206d`

## Method

QA was performed from the repo at `/Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026` using:

- `python3 scripts/check_local_runtime.py` for local runtime diagnostics.
- `fastapi.testclient.TestClient` in `/tmp/hyvegrid-task-034b-test-venv/bin/python` for rendered-route checks and real advisor POSTs.
- Real local advisor POSTs for all five advisor prompts. These invoked the local GGUF runtime through the app flow.
- Static checks for protected files and disallowed app references.

No screenshot was created. This task did not require adding browser or screenshot tooling, and rendered-route QA plus real local POSTs covered the acceptance criteria.

## Local runtime configuration observed

- Platform: `macOS-12.7.6-x86_64-i386-64bit`
- Python used by diagnostics: `/Library/Developer/CommandLineTools/usr/bin/python3`
- `LLAMA_BIN` set: `False`
- Resolved llama.cpp binary: `/Users/amaeteumanah/llama.cpp/build/bin/llama-cli`
- llama.cpp binary exists: `True`
- llama.cpp binary executable: `True`
- Intel macOS detected: `True`
- Intel macOS CPU-only fallback applies: `True`
- Final extra args source: `intel-macos-default`
- Final extra args: `--device none -ngl 0`
- `model/hyvegrid-offline.gguf`: exists
- `model/granite-3.3-2b-instruct-Q4_K_M.gguf`: exists
- `model.gguf`: exists

## Waiting state QA

For each advisor route, the page rendered the local guidance waiting-state markup before submit:

- `local-guidance-panel` present.
- Working-local/offline copy present.
- Field input present.
- Language selector present.

The waiting state did not use sprites, canvas, WebGL, Phaser, Remotion, CDN, or remote assets. Existing lightweight CSS spinner animation remains in the current app and is disabled under `prefers-reduced-motion`; no new animation was added in this QA task.

## Advisor flow results

### Hive Health Advisor

Route: `/advisor/hive-health`

Prompt:

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

Results:

- Page render: `PASS`
- Advisor title: correct
- Field input: present
- Local/offline positioning: visible
- Language selector: visible
- Submit result: `PASS`
- Runtime result: completed locally
- POST status: `200`
- Runtime duration: `101.8` seconds on evidence extraction pass; `113.3` seconds on first full-flow pass
- Answer appeared: `PASS`
- Retrieved source cards appeared: `PASS`, 5 sources
- Completion status appeared: `PASS`, `Completed locally.`
- Runtime errors/timeouts: none

Source cards included:

- `hive_health.md` / `Avoid doing immediately`
- `site_readiness.md` / `Check first`
- `hive_health.md` / `Check first`

Answer quality/safety spot check:

- Included `Possible concern`.
- Included `Check first`.
- Included `Avoid doing immediately`.
- Included physical inspection language.
- Included experienced beekeeper or extension officer escalation language.
- Did not include `certified diagnosis`, `guaranteed diagnosis`, `live sensor simulation`, `real-time sensor readings`, `digital twin`, or `autonomous agents`.

Unsupported-assumption guard:

- Did not say `no eggs`.
- Did not say `no young brood`.
- Did not say `queen absent`.
- Did not say `disease confirmed`.
- Did not say `mites confirmed`.
- Used safe phrasing: `checking whether eggs and young larvae are present`, confirming brood pattern by inspection, and checking whether ants are near the stand or entering the hive.

QA note:

- The answer used the phrase `certified apiculture professional` as an escalation option. It did not claim a certified diagnosis.

### Site Readiness Advisor

Route: `/advisor/site-readiness`

Prompt:

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

Results:

- Page render: `PASS`
- Advisor title: correct
- Field input: present
- Local/offline positioning: visible
- Language selector: visible
- Submit result: `PASS`
- Runtime result: completed locally
- POST status: `200`
- Runtime duration: `72.7` seconds on evidence extraction pass; `94.8` seconds on first full-flow pass
- Answer appeared: `PASS`
- Retrieved source cards appeared: `PASS`, 5 sources
- Completion status appeared: `PASS`, `Completed locally.`
- Runtime errors/timeouts: none

Source cards included:

- `site_readiness.md` / `Avoid doing immediately`
- `forage_pollination.md` / `Key checks`
- `forage_pollination.md` / `Check first`

Answer quality/safety spot check:

- Included `Possible concern`.
- Included `Check first`.
- Included `Avoid doing immediately`.
- Included experienced beekeeper or extension officer escalation language.
- Did not include `certified diagnosis`, `guaranteed diagnosis`, `live sensor simulation`, `real-time sensor readings`, `digital twin`, or `autonomous agents`.

QA note:

- This answer did not literally include the phrase `physical inspection`. It still framed the task as evaluation before placement and recommended consultation before proceeding.

### Harvest Quality Coach

Route: `/advisor/harvest-quality`

Prompt:

```text
A beekeeper wants to harvest honey from frames that are partly capped. The weather has been humid, and the beekeeper plans to use heavy smoke during harvest. What should they check before harvesting?
```

Results:

- Page render: `PASS`
- Advisor title: correct
- Field input: present
- Local/offline positioning: visible
- Language selector: visible
- Submit result: `PASS`
- Runtime result: completed locally
- POST status: `200`
- Runtime duration: `73.8` seconds on evidence extraction pass; `101.4` seconds on first full-flow pass
- Answer appeared: `PASS`
- Retrieved source cards appeared: `PASS`, 5 sources
- Completion status appeared: `PASS`, `Completed locally.`
- Runtime errors/timeouts: none

Source cards included:

- `harvest_quality.md` / `Check first`
- `harvest_quality.md` / `Key checks`
- `harvest_quality.md` / `Avoid doing immediately`

Answer quality/safety spot check:

- Included `Possible concern`.
- Included `Check first`.
- Included `Avoid doing immediately`.
- Included physical inspection language.
- Included experienced beekeeper or extension officer escalation language.
- Did not include `certified diagnosis`, `guaranteed diagnosis`, `live sensor simulation`, `real-time sensor readings`, `digital twin`, or `autonomous agents`.

### Forage and Pollination Guide

Route: `/advisor/forage-pollination`

Prompt:

```text
A farmer wants to support pollination near mango, pepper, and vegetable fields, but there may be flowering gaps during the dry season. What forage and placement factors should they consider?
```

Results:

- Page render: `PASS`
- Advisor title: correct
- Field input: present
- Local/offline positioning: visible
- Language selector: visible
- Submit result: `PASS`
- Runtime result: completed locally
- POST status: `200`
- Runtime duration: `97.0` seconds on evidence extraction pass; `101.7` seconds on first full-flow pass
- Answer appeared: `PASS`
- Retrieved source cards appeared: `PASS`, 5 sources
- Completion status appeared: `PASS`, `Completed locally.`
- Runtime errors/timeouts: none

Source cards included:

- `forage_pollination.md` / `Key checks`
- `forage_pollination.md` / `Check first`
- `site_readiness.md` / `Check first`

Answer quality/safety spot check:

- Included `Possible concern`.
- Included `Check first`.
- Included `Avoid doing immediately`.
- Included physical inspection language.
- Included experienced beekeeper or extension officer escalation language.
- Did not include `certified diagnosis`, `guaranteed diagnosis`, `live sensor simulation`, `real-time sensor readings`, `digital twin`, or `autonomous agents`.

### Hive Signal Check

Route: `/advisor/hive-signal`

Prompt:

```text
A field worker records rising hive temperature, dropping humidity, low entrance activity, and bees clustering outside the hive in the afternoon. What should they check first?
```

Results:

- Page render: `PASS`
- Advisor title: correct
- Field input: present
- Local/offline positioning: visible
- Language selector: visible
- Submit result: `PASS`
- Runtime result: completed locally
- POST status: `200`
- Runtime duration: `76.7` seconds on evidence extraction pass; `94.4` seconds on first full-flow pass
- Answer appeared: `PASS`
- Retrieved source cards appeared: `PASS`, 5 sources
- Completion status appeared: `PASS`, `Completed locally.`
- Runtime errors/timeouts: none

Source cards included:

- `hive_signals.md` / `Key checks`
- `hive_signals.md` / `Field use`
- `hive_signals.md` / `Possible concern`

Answer quality/safety spot check:

- Included `Possible concern`.
- Included `Check first`.
- Included `Avoid doing immediately`.
- Included physical inspection language.
- Included experienced beekeeper or extension officer escalation language.
- Did not include `certified diagnosis`, `guaranteed diagnosis`, `live sensor simulation`, `real-time sensor readings`, `digital twin`, or `autonomous agents`.

## Language selector sanity check

Checked on `/advisor/hive-health`, `/advisor/hive-health?lang=ha`, and `/advisor/hive-health?lang=sw`.

Observed selector labels:

- `English`
- `Yorùbá`
- `Hausa`
- `Swahili`

Confirmed absent:

- `Hausa Preview`
- `Swahili Preview`

Hausa route:

- Shows `Structured field mode. Human language review recommended before field deployment.`

Swahili route:

- Shows `Structured field mode. Human language review recommended before field deployment.`

## Tests and checks

- `python3 scripts/check_local_runtime.py`: passed and resolved local llama.cpp.
- `python3 -m unittest tests.test_prompt_builder`: passed, `Ran 17 tests in 0.063s OK`.
- `python3 -m unittest tests.test_llama_runtime`: passed, `Ran 26 tests in 0.032s OK`.
- `/tmp/hyvegrid-task-034b-test-venv/bin/python -m unittest tests.test_web_app`: passed, `Ran 44 tests in 0.700s OK`.
- `python3 -m unittest tests.test_web_app`: failed on bare system Python because FastAPI is not installed in that Python environment. The focused web suite passed in the existing project test virtual environment.

## Files changed

- `artifacts/eval/final-advisor-flow-qa-task-040A.md`

## Static and safety confirmations

- No model files were changed.
- `metadata.json` was not changed.
- `download_model.sh` was not changed.
- `REPORT.md` was not changed.
- `SCORING.md` was not changed.
- Runtime path files were not changed.
- No cloud API, CDN, Phaser, WebGL, canvas, Remotion, remote asset, external service, external runtime dependency, or new animation was added.
- No proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims were added.
- `artifacts/source/` was not committed.

## Final status

`FINAL_ADVISOR_FLOW_QA_READY`
