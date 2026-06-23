# Granite Runtime Cleanup (Task 015)

1. **Task title and date:** Runtime cleanup and speed triage for the existing Granite
   llama.cpp CLI path. Date: 2026-06-23.

## Starting commit

- `b6fb65f13374e654d6f57ca89f885c57766fd533` (branch `phase-1-eval-harness`)

## Scope

Fix the Task 014 smoke issues on the locked Granite 3.3 2B Instruct Q4_K_M +
llama.cpp path, without changing the model, quantization, prompts, metadata, or
adding any UI/Yoruba/cloud work:

- Clean llama.cpp conversation-mode chrome and prompt echo from the final answer.
- Demote README.md and glossary.md so field notes outrank them for beekeeper and
  site-readiness questions (keep them for explicit glossary/definition queries).
- Reduce prompt/context bloat and prevent the Prompt 2 truncation.
- Light speed triage using safe levers only.

## Files changed

- `app/llama_runtime.py`
  - Added `clean_llama_output()` to strip banner/logo, "Loading model...",
    build/model/modalities lines, "available commands" help, the echoed prompt,
    the timing footer, and "Exiting...", keeping the real answer and its section
    headings ("Check first", "Avoid doing immediately", etc.).
  - `_build_command()` adds `--no-warmup` (skip the throwaway warmup pass).
  - `run_llama_prompt()` now runs the captured stdout through `clean_llama_output()`
    on both the success and timeout paths (raw stdout/stderr are still kept on the
    result dict for debugging).
  - `answer_question()` defaults: `max_context_chars` 3000 -> 1800, `max_tokens`
    384 -> 512.
- `app/retrieval.py`
  - Added `GENERIC_SOURCES = {"README.md", "glossary.md"}` and
    `_is_glossary_intent()` (definition/glossary/terminology/translate queries).
  - `search_knowledge()` excludes generic sources by default (still returns them
    for glossary-intent queries or when `include_generic=True`). `_fts_search()`
    and `_like_search()` accept an `exclude` set and filter via `source_file NOT IN`.
- `app/prompt_builder.py`
  - `build_prompt_with_retrieval()` default `max_context_chars` 3000 -> 1800.
- `scripts/ask_hyvegrid_cli.py`
  - Defaults `--max-context-chars` 3000 -> 1800, `--max-tokens` 384 -> 512.
  - Added opt-in `--show-stats` to print prompt/generation tokens-per-second parsed
    from the raw stdout (default off, so normal output is sources + answer only).
- `tests/test_retrieval.py`
  - Updated the LIKE-fallback mock stub for the new `_fts_search` signature.
  - Added ranking tests: README not top for the hive-health prompt; glossary does
    not outrank field notes; glossary-intent returns generic sources;
    `include_generic=True` override.
- `tests/test_llama_runtime.py`
  - Added `CleanLlamaOutputTests` covering chrome/echo stripping, the "last answer
    start" logic (echoed format list vs real answer), timing-footer removal,
    empty input, and the no-anchor fallback.

## What was fixed

1. **Output chrome / prompt echo:** the final CLI answer now contains only the
   model answer. Verified live on both prompts (answers begin at
   "1. Possible concern:" with no banner, "Loading model...", "available
   commands", echoed prompt, timing line, or "Exiting...").
2. **README.md ranking:** README no longer appears for the hive-health or
   site-readiness prompts; `hive_health.md` is now the top source for Prompt 1.
3. **glossary.md ranking:** glossary no longer appears for normal beekeeper/site
   questions (still returned for definition/glossary queries).
4. **Prompt 2 truncation:** `max_tokens` 384 -> 512; Prompt 2's section 5 now
   completes fully ("...suitability for hive placement.").
5. **Context bloat:** `max_context_chars` 3000 -> 1800 (fewer prompt-eval tokens,
   less memory pressure).

## What was intentionally not changed

- Model file / quantization (Granite 3.3 2B Instruct Q4_K_M is locked).
- The two official ADTC prompts.
- `metadata.json`, `download_model.sh`, scoring formulas, rubric, existing eval
  artifacts (this file is the only new artifact).
- System instructions and the cautious 5-section answer framing.
- No UI, no Yoruba, no cloud/network dependency added.

## Runtime settings before and after

| Setting | Before (Task 014) | After (Task 015) |
|---|---|---|
| llama-cli flags | `-m -p -n -t --temp --single-turn --no-display-prompt --simple-io` | same **+ `--no-warmup`** |
| max_tokens | 384 | **512** (fixes truncation) |
| max_context_chars | 3000 | **1800** (bloat/speed) |
| timeout_seconds | 600 | 600 (unchanged) |
| answer post-processing | raw stdout (chrome included) | **`clean_llama_output()`** |
| retrieval generic docs | README/glossary eligible | **excluded unless glossary-intent** |

Chosen max token value and why: **512**. Task 014 truncated Prompt 2's section 5
at 384. 512 gives ~33% headroom while staying conservative on RAM/speed; with EOS
honored, short answers still stop early so the cap only costs extra time when the
answer is genuinely long.

## Retrieval behavior before and after

| Prompt | Before (Task 014) top source | After (Task 015) top source | README? | glossary? |
|---|---|---|---|---|
| 1 (hive health / ants / brood) | `README.md` (Field use) | `hive_health.md` (Avoid doing immediately) | no | no |
| 2 (20 hives / cassava / mango / pepper / vegetables / water) | `site_readiness.md` (Avoid doing immediately) | `site_readiness.md` (Avoid doing immediately) | no | no |

After cleanup, both official prompts return only field notes; README and glossary
are absent from normal beekeeper/site retrieval but still indexed and returned for
definition/glossary/terminology queries.

## Prompt 1 result

- Command: `/usr/bin/time -v python3 scripts/ask_hyvegrid_cli.py --show-stats "<prompt 1>"`
- Wall time: 7:53.44 (~473.4 s)
- Max RSS: 6,067,000 kB (~5.79 GB)
- Generation: 2.8 t/s | Prompt eval: 3.5 t/s
- Exit code: 0
- Retrieved sources (order): `hive_health.md` (Avoid doing immediately),
  `site_readiness.md` (Check first), `hive_health.md` (Check first),
  `hive_health.md` (Possible concern), `site_readiness.md` (Avoid doing immediately)
- README.md appeared: no
- glossary.md appeared: no
- Final answer clean: yes (no chrome, no prompt echo)
- Prompt echo absent: yes
- Output truncated: no (all five sections complete)
- Quality notes: 5-section format; "possible concern" + cautious language;
  recommends physical inspection (entrance, brood pattern, food stores, ants);
  avoid harvesting / splitting / moving / merging; monitor for a few days;
  escalate to experienced beekeeper/extension officer; no certified-diagnosis or
  cloud claims.

## Prompt 2 result

- Command: `/usr/bin/time -v python3 scripts/ask_hyvegrid_cli.py --show-stats "<prompt 2>"`
- Wall time: 4:00.66 (~240.7 s)
- Max RSS: 6,059,616 kB (~5.78 GB)
- Generation: 3.6 t/s | Prompt eval: 17.5 t/s
- Exit code: 0
- Retrieved sources (order): `site_readiness.md` (Avoid doing immediately),
  `forage_pollination.md` (Key checks), `forage_pollination.md` (Check first),
  `site_readiness.md` (Possible concern), `site_readiness.md` (Key checks)
- README.md appeared: no
- glossary.md appeared: no
- Final answer clean: yes
- Prompt echo absent: yes
- Output truncated: no (section 5 completes fully — the 384->512 fix worked)
- Quality notes: identifies crop-dependence risk; recommends a flowering calendar
  and forage-gap check; avoid placing 20 hives in close proximity; build a diverse
  forage base; coordinate pesticide schedules with farmers; escalate to
  experienced beekeeper/extension officer; no certified-diagnosis or cloud claims.

## Test results

```
python3 -m unittest tests/test_retrieval.py tests/test_prompt_builder.py tests/test_llama_runtime.py
Ran 45 tests in 0.716s
OK
```

45/45 pass (36 carried over + 4 retrieval-ranking + 5 output-cleaning).
`python3 -m py_compile` clean for all edited modules and tests.

## Speed triage

- Wall time is **variable and bounded by RAM/swap paging**, not by the code. The
  ~6 GB Q4 model on a 6.7 GB VM pages against swap, so prompt-eval t/s swings
  (Prompt 1: 3.5 t/s under thrash; Prompt 2: 17.5 t/s when not thrashing).
- Safe levers applied: smaller context (3000 -> 1800 chars) and `--no-warmup`.
  These reduce prompt size and skip a throwaway pass; Prompt 2 improved markedly
  (240 s vs Task 014's 438 s). Prompt 1 happened to land in a thrashing window
  (473 s) despite the smaller prompt.
- Conclusion: speed **did not regress from the code**; it is dominated by
  environmental memory pressure. No model/quant change (out of scope and locked).

## Decision

**PASS**

All acceptance criteria met: final CLI output contains only the answer; prompt
echo and llama.cpp chrome are absent; README.md is not the top source for the
hive-health prompt (it is absent); glossary.md does not outrank field notes for
the beekeeper/site prompts (absent); Prompt 2 is not truncated; both official
prompts exit 0; 45/45 tests pass; no model/metadata/download_model/UI/Yoruba/
cloud changes.

## Remaining issues and recommended next task

- **Latency variance** from swap paging on the 6.7 GB VM remains (a 6 GB model on
  6.7 GB RAM). This is environmental; the only real fix would be a smaller
  footprint (different quant/model), which is out of scope since the runtime
  candidate is locked.
- Recommended **Task 016**: now that the runtime path and output are clean and
  correct, move to the local demo/UI polish layer (answer post-check for the
  5-section format, CLI/demo ergonomics) while keeping no-Yoruba/no-cloud. Only
  revisit latency if a smaller quant is ever approved.
