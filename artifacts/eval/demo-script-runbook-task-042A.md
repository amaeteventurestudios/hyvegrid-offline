# Task 042A Demo Script and Runbook Audit

## Files created

- `artifacts/demo/demo-video-script-task-042A.md`
- `artifacts/demo/local-demo-runbook-task-042A.md`
- `artifacts/eval/demo-script-runbook-task-042A.md`

## Protected files unchanged

This task is documentation-only. No protected app, data, model, test, metadata,
download, scoring, report, spec, runtime, prompt-builder, retrieval, or language
logic files were edited.

## Constraint checks

- No app behavior changed.
- No runtime behavior changed.
- No model behavior changed.
- No retrieval behavior changed.
- No language behavior changed.
- No submission metadata changed.
- No OpenAI, Claude, GLM, external API, cloud API, cloud database, Supabase,
  Vercel, CDN asset, remote asset, or internet runtime dependency was added.
- No Phaser, Remotion, WebGL, canvas, generated image, generated art, or
  animation dependency was added.
- No proprietary hardware plan, sensor IP, firmware strategy, private dataset,
  commercial roadmap, partner strategy, investor material, or patent-sensitive
  claim was added.

## Demo coverage checklist

- HyveGrid Offline running locally at `localhost`: covered.
- Offline and local positioning: covered.
- Local GGUF model through llama.cpp: covered.
- One real local answer through the app: covered with the Hive Health live run.
- Retrieved local sources: covered.
- `Completed locally.`: covered.
- Five advisor areas: covered.
- Language selector with English, Yorùbá, Hausa, and Swahili: covered.
- Hausa and Swahili human-review-needed notes: covered.
- Offline System Status: covered.
- Field guidance and not certified diagnosis safety language: covered.

## Commands documented

The runbook includes:

```bash
cd /Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026
source .venv/bin/activate
python3 scripts/check_local_runtime.py
python -m app.web_app
```

The runbook includes:

```text
http://127.0.0.1:8000
```

The known system Python issue is documented exactly:

```text
Bare system Python may fail web tests if FastAPI is not installed. Use the project virtual environment or the known test venv.
```

## Runtime behavior changed?

No.

## Notes

The demo script avoids removed animation plans and does not reference keeper
walking sprites, bee or ant sprite animations, camera timelines, walkthrough
board animation, Phaser, WebGL, canvas, Remotion, generated art, or remote visual
assets.

The script uses cautious field-guidance language:

- possible concern
- check first
- avoid doing immediately
- confirm by physical inspection
- consult an experienced beekeeper or extension officer when needed

## Final status

`DEMO_SCRIPT_RUNBOOK_READY`
