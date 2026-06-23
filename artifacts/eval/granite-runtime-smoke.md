# Granite Runtime Smoke Test

## Purpose

This is the first controlled full local runtime smoke test of the complete
HyveGrid Offline answer path:

```
user question
  -> public knowledge retrieval (SQLite FTS5)
  -> prompt builder
  -> llama.cpp (llama-cli, local subprocess)
  -> Granite GGUF answer
```

It confirms the offline path works end-to-end on the local target-class
hardware and captures rough runtime, memory, and answer-quality observations. It
is a smoke test only, not a new model search or a benchmark.

## Environment

- Branch: `phase-1-eval-harness`
- Starting HEAD: `205d0d56b4553947b9c51619f930aed1d5352a31`
- llama binary: `/home/amaete/llama.cpp/build/bin/llama-cli` (build `b9753-7c082bc41`)
- model path: `model/granite-3.3-2b-instruct-q4_k_m.gguf`
  -> resolves to `model-candidates/granite-3.3-2b-instruct-Q4_K_M.gguf` (~1.5 GB Q4_K_M)
- knowledge DB generated: **yes** (`data/knowledge/knowledge.db`, 73 chunks)
- runtime: **local only** (single llama-cli subprocess per question)
- cloud/API dependency: **no** (stdlib + local app modules; no network)
- CLI: `scripts/ask_hyvegrid_cli.py`, defaults (`-n 384`, `--temp 0.2`, `-t 4`)
- hardware: Intel i7-6700K (4 cores), ~6.7 GB RAM, ~2 GB swap. The model's ~6 GB
  RSS exceeds free RAM, so generation pages against swap (1.8-2.2 tokens/s).

Runtime-wrapper note: a tiny fix was applied for this task. The default
`run_llama_prompt(timeout_seconds=...)` was raised from 180 to 600 s because the
first two attempts timed out at 180 s under swap paging on the 6.7 GB box. The
path otherwise needed no code changes; the wrapper, prompt builder, and
retrieval behaved correctly. All 36 unit tests still pass.

## Prompt 1 result

Prompt text:

> A beekeeper reports low hive activity, ants near the hive stand, normal smell,
> and partially capped brood. What should they check first, and what should they
> avoid doing immediately?

Retrieved sources (top 5 from CLI):

- `README.md` | Field use
- `hive_health.md` | Avoid doing immediately
- `site_readiness.md` | Check first
- `hive_health.md` | Check first
- `hive_health.md` | Possible concern

Answer summary (Granite, 5-section format followed):

1. Possible concern - low activity, ants, and partially capped brood could
   indicate a robber attack, parasitic mite infestation, or a collapsing colony.
2. Check first - confirm by physical inspection whether the entrance is blocked
   by bees/debris/pests; check for eggs and a solid brood pattern across frames;
   look for wax-moth webbing/tunnels/larvae; check recent disturbance, weather,
   spray, or feeding changes.
3. Avoid doing immediately - avoid harvesting from the weak/stressed colony;
   avoid splitting, moving, or merging before checking; avoid spraying chemicals
   into or near the hive; avoid opening the hive repeatedly in poor weather.
4. Suggested next step - determine whether ants are scavenging or harming the
   colony; monitor closely; consider consulting an experienced beekeeper or
   extension officer.
5. When to escalate - if no improvement or mites/disease suspected, escalate to
   an experienced beekeeper or extension officer.

Format followed: **yes** - all five sections present, cautious language used,
physical inspection recommended, escalation recommended, no certified-diagnosis
claim, no cloud/API claim, no private/hardware/sensor data, on-topic.

Rough runtime (`/usr/bin/time -v`):

- Elapsed (wall clock): 5:55.73 (~355.7 s)
- User time: 361.49 s; System time: 117.46 s; CPU ~134%
- Prompt processing: 17.4 t/s; Generation: 2.2 t/s
- Maximum resident set size: 6,166,872 kB (~5.88 GB)
- Exit status: 0

Issues found:

- The captured CLI stdout includes llama.cpp UI chrome (the "Loading model..."
  banner, ASCII logo, "available commands" list, and an echoed/truncated copy of
  the prompt) before the actual answer. The generated 5-section answer itself is
  clean.
- The top retrieved source was the generic `README.md` "Field use" chunk rather
  than a `hive_health.md` chunk, although `hive_health.md` appeared three times
  in the top 5.

## Prompt 2 result

Prompt text:

> An extension worker wants to place 20 hives near cassava, mango, pepper, and
> vegetable farms with a seasonal water source nearby. What site risks and
> forage factors should they evaluate before placing the hives?

Retrieved sources (top 5 from CLI):

- `site_readiness.md` | Avoid doing immediately
- `forage_pollination.md` | Key checks
- `forage_pollination.md` | Check first
- `site_readiness.md` | Possible concern
- `site_readiness.md` | Key checks

Answer summary (Granite, 5-section format followed):

1. Possible concern - crop-dependence risk: over-reliance on cassava/mango/
   pepper/vegetables; if these finish flowering or are sprayed, colonies lose a
   major food source.
2. Check first - physical inspection of the area: note what is flowering, forage
   diversity, and nearby pesticide application schedules/timings; check colony
   stores before and after the expected flowering gap.
3. Avoid doing immediately - avoid placing all 20 hives at once (overwhelms
   forage); avoid placing hives close to homes, paths, children, or livestock.
4. Suggested next step - assess overall forage diversity, including other
   flowering plants, trees, and wildflowers, to build a more resilient forage
   base.
5. When to escalate - consult an experienced beekeeper or local apiculture
   expert when unsure about site suitability or risks.

Format followed: **yes** - five sections, cautious language, physical
inspection recommended, escalation recommended, no certified-diagnosis claim,
no cloud/API claim, no private/hardware/sensor data, on-topic. Section 5 was
slightly truncated at the 384-token budget ("...associated with the proposed").

Rough runtime (`/usr/bin/time -v`):

- Elapsed (wall clock): 7:18.30 (~438.3 s)
- User time: 511.49 s; System time: 112.41 s; CPU ~142%
- Prompt processing: 14.6 t/s; Generation: 1.8 t/s
- Maximum resident set size: 6,122,488 kB (~5.84 GB)
- Exit status: 0

Issues found:

- Same llama.cpp UI chrome in captured stdout as Prompt 1.
- Section 5 truncated at the 384-token generation limit.
- Generation slow (1.8 t/s) due to swap paging on the 6.7 GB box.

## Smoke decision

**PASS WITH ISSUES**

The complete offline answer path works end-to-end on local target-class
hardware: retrieval -> prompt builder -> llama.cpp -> Granite produced cautious,
on-topic, correctly formatted (5-section) answers for both prompts, with no
cloud dependency and no crash or OOM (swap absorbed the memory pressure).

The issues are output-quality/formatting, not a broken path:

1. Captured stdout contains llama.cpp UI chrome (banner + echoed prompt) that
   must be stripped so the `answer` field is clean for display.
2. Prompt 2's final section truncated at the 384-token budget.
3. Prompt 1's top retrieved source was a generic `README.md` chunk rather than
   the most relevant `hive_health.md` chunk.
4. Generation is slow (1.8-2.2 t/s) under swap paging; acceptable for a smoke
   test but worth noting for any latency-sensitive demo.

## Next recommended task

Task 015 should fix the exact output-quality issues above, in priority order:

1. Strip llama.cpp banner/echo from the runtime result so `answer` contains only
   the generated text (parse the output or use a cleaner invocation).
2. Raise or otherwise manage the generation token budget so the 5-section answer
   is not truncated.
3. Tune retrieval filtering so answer-critical questions surface the most
   relevant note (e.g., down-rank or exclude `README.md`/`glossary.md` from
   top results for field-symptom questions).
4. Optionally reduce prompt context size or thread/memory pressure to ease swap
   paging and improve tokens/s.

The runtime path itself is sound, so Task 015 should be output-quality work
before moving on to UI or Yoruba.
