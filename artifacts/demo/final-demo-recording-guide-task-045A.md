# Task 045A Final Demo Recording Guide

## Purpose

Guide the final HyveGrid Offline demo recording using the verified local app, Task 042A demo script, Task 042A local runbook, and Task 044B shot list. This guide does not record, edit, or upload the final video.

## Recording target

Recommended target: 2 minutes, with a hard ceiling of 3 minutes if local inference is slow.

Because the Task 045A dry run completed the Hive Health local answer in about 164.5 seconds, start the live inference as early as practical in the recording and use backup narration while the local answer is prepared.

## Recording setup

- Open a clean terminal.
- Activate `.venv`.
- Run diagnostics.
- Start the local app.
- Open localhost in the browser.
- Keep Task 042A script and Task 044B shot list nearby.
- Close unrelated browser tabs and private files before recording.

## Exact commands

```bash
cd /Users/amaeteumanah/Desktop/Projects/hyvegrid-offline-adtc-2026
source .venv/bin/activate
python3 scripts/check_local_runtime.py
python -m app.web_app
```

## Local URL

```text
http://127.0.0.1:8000
```

## Final shot order

1. Terminal and local app startup
2. Mission Control
3. Offline/local positioning
4. Hive Health Advisor live run
5. Waiting state
6. Answer, retrieved sources, Completed locally.
7. Site Readiness Advisor quick run or mention
8. Language selector
9. Hausa/Swahili human-review-needed caveat
10. Offline System Status
11. Safety limitation and close

## Main prompt to paste

```text
A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?
```

## Second prompt to paste

```text
An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?
```

## Spoken proof points

- This app is running locally at localhost.
- The answer path uses a local GGUF model through llama.cpp.
- The app retrieves public local apiculture notes.
- Retrieved sources are shown with the answer.
- The completion status says Completed locally.
- HyveGrid Offline provides field guidance and triage support. It is not a certified disease diagnosis tool. Users should confirm by physical inspection and consult an experienced beekeeper or extension officer when needed.
- This is the public ADTC 2026 challenge edition.

## If inference is slow

- Say local CPU inference is preparing guidance.
- Keep recording on the waiting state.
- Do not restart unless there is an actual failure.
- Do not claim cloud fallback.
- Use the time to narrate the local path: local app, local GGUF model through llama.cpp, and local retrieved apiculture notes.

Backup narration:

```text
This pause is expected on a local CPU path. The app is preparing local guidance using the GGUF model through llama.cpp and local retrieved apiculture notes. I will keep the screen on the waiting state so the offline flow is visible.
```

## Must show on screen

- [ ] localhost URL
- [ ] Mission Control
- [ ] five advisor areas
- [ ] Hive Health prompt
- [ ] retrieved sources
- [ ] Completed locally.
- [ ] language selector
- [ ] Offline System Status

## Must not show or say

- cloud model dependency
- external API dependency
- live sensor support
- real-time sensor readings
- autonomous agents
- digital twin functionality
- certified disease diagnosis claim
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
- removed animation work

## Language caveat

Hausa and Swahili are included as structured field-template modes for demonstration and reviewer evaluation. They are not claimed as human-reviewed or native-quality translations.

## Public challenge edition boundary

This is a public challenge edition. It does not include proprietary hardware plans, sensor IP, firmware strategy, private datasets, commercial roadmap, partner strategy, investor materials, or patent-sensitive claims.

## Final recording checklist

- [ ] Runtime diagnostics pass.
- [ ] App starts locally.
- [ ] Browser shows `http://127.0.0.1:8000`.
- [ ] Mission Control is visible.
- [ ] Five advisor areas are visible.
- [ ] Hive Health prompt is pasted exactly.
- [ ] Waiting state appears.
- [ ] Local answer returns.
- [ ] Retrieved local sources appear.
- [ ] `Completed locally.` appears.
- [ ] Site Readiness prompt is shown or narrated.
- [ ] Language selector is visible.
- [ ] Hausa/Swahili caveat is stated.
- [ ] Offline System Status is shown.
- [ ] Safety limitation is stated.
