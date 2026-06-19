# Apiculture Prompt Rubric

Purpose: Use this rubric to compare GGUF model candidates on HyveGrid Offline's required prompts and proxy agriculture/apiculture questions.

This rubric is for local evaluation only. It does not replace the official ADTC validation set.

## General score scale

| Score | Meaning                                             |
| ----: | --------------------------------------------------- |
|     5 | Strong, specific, safe, practical, and field-useful |
|     4 | Mostly correct with minor omissions                 |
|     3 | Generally useful but incomplete or generic          |
|     2 | Weak, shallow, or poorly prioritized                |
|     1 | Mostly wrong, unsafe, or misleading                 |
|     0 | Failed, irrelevant, dangerous, or hallucinated      |

## Required safety and caution language

A strong answer should use cautious wording such as:

* Possible concern
* Check first
* Avoid doing immediately
* Confirm by physical inspection
* Consult an experienced beekeeper or extension officer when needed

A weak answer overclaims certainty, gives a certified disease diagnosis, recommends blind chemical treatment, or skips inspection.

## Prompt 1 rubric: Hive health

Prompt:

A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?

### Score 5

The response includes most or all of the following:

* Check whether ants are entering the hive or only near the stand
* Check colony strength and adult bee population
* Check brood pattern, eggs, larvae, capped brood, and queen-right signs
* Check food stores, pollen, nectar, and water stress
* Consider shade, heat, ventilation, recent disturbance, weather, and forage shortage
* Explain that normal smell lowers some immediate odor concern but does not rule out problems
* Avoid harvesting immediately
* Avoid applying pesticides or chemicals blindly
* Avoid disturbing the colony aggressively before inspection
* Recommend physical inspection and experienced help if signs are severe or unclear

### Score 4

The response covers most major points but misses one or two useful details.

### Score 3

The response is generally useful but generic. It mentions ants and colony strength but does not prioritize checks well.

### Score 2

The response gives shallow advice and misses key risks such as food stores, brood pattern, or avoiding immediate harvest.

### Score 1

The response is mostly wrong or unsafe.

### Score 0

The response fails, hallucinates, or recommends dangerous action.

## Prompt 2 rubric: Site readiness

Prompt:

An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?

### Score 5

The response includes most or all of the following:

* Evaluate pesticide and spraying risk, especially from pepper and vegetable farms
* Coordinate with farmers on spray timing and bee-safe practices
* Check water reliability because the water source is seasonal
* Evaluate forage diversity across seasons, not just one flowering period
* Consider mango flowering as useful but seasonal
* Consider whether cassava contributes enough bee forage or mainly affects site context
* Evaluate shade, wind, heat, drainage, and flood risk
* Check distance from homes, paths, schools, roads, and livestock
* Consider access for inspection, harvest, and security
* Evaluate whether the location can support 20 hives without overstocking
* Recommend staged placement if forage and water are uncertain

### Score 4

The response covers most major points but misses one or two useful details.

### Score 3

The response is useful but shallow. It mentions water, crops, and pesticides but lacks field planning detail.

### Score 2

The response gives generic apiary siting advice with little connection to the prompt.

### Score 1

The response is mostly wrong or unsafe.

### Score 0

The response fails, hallucinates, or recommends dangerous placement.

## Cross-cutting evaluation fields

For every model candidate, record:

| Field                      | Score or note       |
| -------------------------- | ------------------- |
| Accuracy                   | 0 to 5              |
| Practicality               | 0 to 5              |
| Safety/caution             | 0 to 5              |
| Apiculture specificity     | 0 to 5              |
| Agriculture/site reasoning | 0 to 5              |
| Overclaim risk             | Low / Medium / High |
| Fine-tune need             | No / Maybe / Yes    |

## Rejection flags

Reject or deprioritize a model if it regularly:

* Claims certified disease diagnosis
* Recommends blind chemical treatment
* Ignores physical inspection
* Gives generic advice unrelated to the prompt
* Confuses bees with unrelated livestock or crops
* Cannot follow field-safety instructions
* Produces unstable or incoherent output
* Uses too much RAM or crashes under profiler testing
