# HyveGrid Offline Demo Video Script, Task 042A

## Purpose

Create a repeatable presenter script for recording or presenting HyveGrid Offline without improvising. The demo should show the current verified public ADTC 2026 challenge edition: local app, local GGUF inference through llama.cpp, local retrieved apiculture notes, five advisor areas, multilingual field-template support, and cautious safety boundaries.

## Recording length target

Target 5 to 7 minutes.

- Opening and offline setup: 45 seconds
- Mission Control and advisor overview: 60 seconds
- Hive Health live run: 2 to 3 minutes, depending on local inference speed
- Site Readiness quick mention: 45 seconds
- Language and status checks: 60 seconds
- Closing safety note: 30 seconds

## Presenter setup

Before recording:

1. Start the local app from the repo.
2. Open `http://127.0.0.1:8000`.
3. Keep the Hive Health prompt ready to paste.
4. Keep the Site Readiness prompt ready to paste.
5. Have a backup narration ready in case the first local answer takes more than a minute.

Use this exact offline positioning language:

```text
This app is running locally on this laptop at localhost. The answer path uses a local GGUF model through llama.cpp and local retrieved apiculture notes. No cloud model or external API is needed during the demo.
```

Use this exact safety language:

```text
HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
```

## Scene-by-scene script

### 1. Opening: what HyveGrid Offline is

Show the Mission Control page.

Say:

```text
This is HyveGrid Offline, the public ADTC 2026 challenge edition. It is a local, offline apiculture intelligence assistant for African beekeepers and extension workers.
```

Say:

```text
It is designed for field guidance and triage support, not certified diagnosis.
```

### 2. Offline status: show local-only operation

Point to the browser URL bar at `localhost` or `127.0.0.1`.

Say:

```text
This app is running locally on this laptop at localhost. The answer path uses a local GGUF model through llama.cpp and local retrieved apiculture notes. No cloud model or external API is needed during the demo.
```

Show any visible offline/local positioning on the page.

### 3. Mission Control: explain the five advisor areas

Show the Mission Control advisor cards.

Say:

```text
Mission Control organizes five field-support areas: Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, and Hive Signal Check.
```

Briefly hover or point to each:

- Hive Health Advisor
- Site Readiness Advisor
- Harvest Quality Coach
- Forage & Pollination Guide
- Hive Signal Check

Say:

```text
Each area keeps the same local pattern: a field question, local retrieval, local GGUF inference, retrieved sources, and a completion status.
```

### 4. Hive Health live run

Open Hive Health Advisor.

Say:

```text
For the main live run, I will use the Hive Health Advisor with the first ADTC prompt path.
```

Paste the main prompt exactly:

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

Submit the prompt.

Say:

```text
This sends the question through the local app. The app retrieves local apiculture notes, builds the prompt locally, and runs the local GGUF model through llama.cpp.
```

### 5. Waiting state: local guidance being prepared

Show the local guidance waiting state while the answer is prepared.

Say:

```text
While the model runs, the app shows a simple local guidance waiting state. This is not a cloud queue. It is local guidance being prepared on the machine.
```

Say:

```text
On a CPU-only laptop or iMac, the first answer can take a little time. That wait is part of the offline tradeoff.
```

Do not mention or show any removed animation plan.

### 6. Answer review: cautious triage, retrieved sources, Completed locally.

When the answer appears, show:

- answer text
- retrieved local sources
- `Completed locally.`

Say:

```text
The answer is structured as cautious field triage. It should talk in terms of possible concern, check first, avoid doing immediately, and confirm by physical inspection.
```

Say:

```text
Here are the retrieved local sources. This confirms the answer path used local apiculture notes, not a remote database.
```

Point to `Completed locally.`

Say:

```text
The completion status says Completed locally.
```

Say the safety line:

```text
HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
```

### 7. Site Readiness quick demo or mention

Open Site Readiness Advisor.

Say:

```text
The second official prompt path is Site Readiness. This supports placement questions before hives are installed.
```

Paste or narrate the second prompt:

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

Recommended recording choice:

- If the first answer was fast, submit this as a short second live run.
- If the first answer was slow, narrate that Task 040A verified this prompt completed locally with retrieved sources and `Completed locally.`

Say:

```text
For a short recording, I may not run the full second inference live, but this path was verified in final advisor QA with local answer completion, retrieved sources, and Completed locally.
```

### 8. Language selector: English, Yorùbá, Hausa, Swahili

Return to Mission Control or an advisor page and show the language selector.

Say:

```text
English remains the default. Yorùbá is preserved as a supported African language layer. Hausa and Swahili are available as structured field-template modes.
```

Show the selector options:

- English
- Yorùbá
- Hausa
- Swahili

### 9. Hausa and Swahili human-review-needed note

Select Hausa on an advisor page.

Say:

```text
Hausa uses controlled structured field templates. It is not claimed as human-reviewed or native-quality.
```

Show the human-review-needed note.

Select Swahili on an advisor page.

Say:

```text
Swahili also uses controlled structured field templates with human review recommended before field deployment.
```

Show the human-review-needed note.

### 10. Offline System Status

Open or point to Offline System Status.

Say:

```text
Offline System Status summarizes the local runtime positioning: local app, local model, local retrieval, and no cloud access required during the demo.
```

### 11. Closing: public challenge edition, field triage, not certified diagnosis

Return to Mission Control or the completed answer.

Say:

```text
HyveGrid Offline is the public ADTC 2026 challenge edition. It demonstrates offline apiculture field guidance using a local GGUF model through llama.cpp, local retrieval, and a localhost app.
```

Close with:

```text
HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
```

## Exact prompts to paste

Main Hive Health prompt:

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

Second Site Readiness prompt:

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

## Lines to say on camera

```text
This is HyveGrid Offline, the public ADTC 2026 challenge edition.
```

```text
This app is running locally on this laptop at localhost. The answer path uses a local GGUF model through llama.cpp and local retrieved apiculture notes. No cloud model or external API is needed during the demo.
```

```text
Mission Control organizes five field-support areas: Hive Health Advisor, Site Readiness Advisor, Harvest Quality Coach, Forage and Pollination Guide, and Hive Signal Check.
```

```text
The answer is structured as cautious field triage: possible concern, check first, avoid doing immediately, confirm by physical inspection, and consult an experienced beekeeper or extension officer when needed.
```

```text
HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
```

## What to show on screen

- Browser URL at `http://127.0.0.1:8000` or localhost.
- Mission Control.
- Five advisor areas.
- Hive Health Advisor form.
- Main Hive Health prompt being pasted.
- Submit action.
- Local guidance waiting state.
- Returned answer.
- Retrieved local sources.
- `Completed locally.`
- Site Readiness Advisor and second prompt.
- Language selector showing English, Yorùbá, Hausa, and Swahili.
- Hausa and Swahili human-review-needed notes.
- Offline System Status.

## What not to claim

Do not claim:

- cloud model support
- external API support
- live sensor support
- real-time sensor readings
- autonomous agents
- digital twin functionality
- certified disease diagnosis
- human-reviewed Hausa
- human-reviewed Swahili
- native-quality Hausa
- native-quality Swahili
- proprietary hardware plans
- sensor IP
- firmware strategy
- private datasets
- commercial roadmap
- partner strategy
- investor materials
- patent-sensitive claims

## Backup narration if inference is slow

Say:

```text
This pause is expected on a local CPU path. The app is preparing local guidance using the GGUF model through llama.cpp and local retrieved apiculture notes. I will keep the screen on the waiting state so the offline flow is visible.
```

If recording time is tight, say:

```text
For the final recording, this can be shortened by starting the local run just before the narration reaches this point. The important proof points are the returned answer, retrieved local sources, and Completed locally status.
```

## Acceptance checklist

- [ ] App shown at localhost.
- [ ] Offline/local positioning stated.
- [ ] Local GGUF model through llama.cpp stated.
- [ ] Mission Control shown.
- [ ] Five advisor areas shown.
- [ ] Hive Health main prompt submitted.
- [ ] Local guidance waiting state shown.
- [ ] Answer shown.
- [ ] Retrieved local sources shown.
- [ ] `Completed locally.` shown.
- [ ] Site Readiness second prompt shown or narrated.
- [ ] Language selector shown with English, Yorùbá, Hausa, and Swahili.
- [ ] Hausa human-review-needed note shown.
- [ ] Swahili human-review-needed note shown.
- [ ] Offline System Status shown.
- [ ] Safety language stated.
- [ ] No certified diagnosis claim made.
- [ ] No cloud, external API, live sensor, real-time sensor, autonomous agent, or digital twin claim made.
