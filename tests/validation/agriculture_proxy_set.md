# Agriculture and Apiculture Proxy Validation Set

Purpose: This file provides a local proxy validation set for comparing small GGUF model candidates before the official ADTC agriculture validation set is available.

Use this set to compare models on agriculture, apiculture, field reasoning, safety, and caution language. This is not the official ADTC validation set. Replace or supplement it when the official set becomes available.

## Scoring

Each response should be scored from 0 to 5.

* 5 = strong, specific, safe, and field-useful
* 4 = mostly correct with minor omissions
* 3 = usable but incomplete or generic
* 2 = weak and shallow
* 1 = mostly wrong or unsafe
* 0 = failed response, dangerous advice, or irrelevant answer

## Required HyveGrid test prompts

### Prompt 1: Hive health

A beekeeper reports low hive activity, ants near the hive stand, normal smell, and partially capped brood. What should they check first, and what should they avoid doing immediately?

Expected strong-answer points:

* Check whether ants are entering the hive, not just near the stand
* Check colony strength and adult bee population
* Check brood pattern, eggs, larvae, capped brood, and queen-right signs
* Check food stores and water stress
* Check shade, heat, ventilation, and disturbance
* Avoid harvesting immediately
* Avoid applying chemicals blindly
* Avoid over-opening or disturbing the colony aggressively
* Recommend physical inspection and experienced help if signs worsen

### Prompt 2: Site readiness

An extension worker wants to place 20 hives near cassava, mango, pepper, and vegetable farms with a seasonal water source nearby. What site risks and forage factors should they evaluate before placing the hives?

Expected strong-answer points:

* Evaluate pesticide and spraying risk from pepper and vegetable farms
* Coordinate with farmers on spray timing
* Check water reliability because the water source is seasonal
* Evaluate forage diversity and flowering calendar
* Consider shade, wind, heat, and drainage
* Ensure safe distance from homes, paths, schools, roads, and livestock
* Check access for inspection, harvest, and security
* Consider whether the area can support 20 hives without overstocking
* Mention mango as useful seasonal forage, but not sufficient alone
* Recommend staged placement if forage and water are uncertain

## Additional proxy prompts

### 3. Weak colony

A beekeeper opens a hive and sees few adult bees, some stored honey, scattered capped brood, and wax moth webbing on one frame. What are the most likely concerns, and what should they check before adding more space?

### 4. Heat stress

Bees are clustering outside the hive in the afternoon. The hive is in full sun, the lid is hot, and the nearby water container is dry. What should the beekeeper check first?

### 5. Harvest timing

A beekeeper wants to harvest honey, but many comb cells are uncapped and the honey appears watery when shaken. What should they do?

### 6. Pesticide exposure risk

A beekeeper reports many dead bees near the entrance after nearby vegetable farms were sprayed. What should they ask, observe, and avoid doing immediately?

### 7. Water source

An apiary site has strong forage during the rainy season but no reliable water in the dry season. What should the extension worker evaluate before placing hives?

### 8. Brood pattern

A hive has spotty brood, few eggs, and no visible queen. What possible concerns should be considered, and what should be checked next?

### 9. Ant pressure

Ants are climbing the hive stand, but the colony still has normal entrance activity and pollen coming in. What should the beekeeper check and do first?

### 10. Absconding risk

A beekeeper finds an almost empty hive with little brood, few bees, ants, and signs of heat exposure. What possible causes should be considered?

### 11. Forage gap

An apiary has good flowering trees for two months, then very little bloom for the rest of the dry season. What risks does this create?

### 12. Pollination planning

A farmer wants to place hives near mango trees during flowering. What should they coordinate with nearby farms before moving hives?

### 13. Smoke contamination

A beekeeper used heavy smoke during harvest, and the honey smells smoky. What quality concern should be explained?

### 14. Storage risk

Freshly harvested honey is stored in open buckets near water and dust. What quality and contamination risks should be flagged?

### 15. Hive entrance activity

A hive has low entrance activity in the morning after heavy rain, but normal activity by afternoon. What should the beekeeper consider before assuming the colony is weak?

### 16. Robbing risk

Many bees are fighting at the entrance, and honey smell is strong near the hive. What possible concern should be checked?

### 17. Shade and wind

An apiary site is open, windy, and has no afternoon shade. What risks does this create for colony management?

### 18. Livestock safety

An extension worker wants to place hives near a livestock path. What risks should be evaluated?

### 19. Queen cells

A beekeeper sees queen cells on a crowded colony with many bees and limited empty comb. What possible management concern should they consider?

### 20. Food stores

A colony has brood but very little honey or pollen during a forage gap. What should the beekeeper check before deciding the colony is diseased?

### 21. Wax moth

A hive has wax moth larvae and damaged comb, but few adult bees. What does this usually suggest about colony strength?

### 22. Simple temperature signal

A sample hive signal shows rising temperature during the afternoon, low entrance activity, and bees clustering outside. What should the beekeeper check first?

### 23. Simple humidity signal

A sample hive signal shows dropping humidity and high temperature during a dry period. What field observations should be checked?

### 24. Site density

An extension worker plans to place 20 hives in one location with limited forage. What should they evaluate before placing all 20 hives?

### 25. Caution and escalation

A beekeeper sees abnormal brood and a bad smell but is not sure what disease it is. What should the assistant say and avoid saying?
