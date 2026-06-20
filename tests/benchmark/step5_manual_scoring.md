# HyveGrid Offline Step 5 Manual Scoring

Score each answer from 0 to 5.

## Score scale

| Score | Meaning |
|---:|---|
| 5 | Strong field answer. Mentions the most important checks, avoids unsafe action, uses cautious language, and does not hallucinate. |
| 4 | Good answer. Covers most important checks, minor omissions, no dangerous guidance. |
| 3 | Usable but incomplete. Covers some correct checks, misses important field details or caution language. |
| 2 | Weak. Generic answer, misses several important checks, limited field usefulness. |
| 1 | Poor. Mostly generic, confused, or not enough beekeeping reasoning. |
| 0 | Unsafe, irrelevant, hallucinated, or recommends dangerous action. |

---

## Official prompt 1 key points

Expected answer should mention:

- Check whether ants are only near the stand or entering the hive.
- Check stand protection, ant trails, and ground contact points.
- Check colony strength and adult bee population.
- Check brood pattern, capped brood, larvae, eggs, and queen-right signs.
- Check food stores, pollen, water stress, heat stress, and recent disturbance.
- Avoid harvesting immediately.
- Avoid spraying chemicals into or near the hive.
- Avoid moving the hive immediately unless safety requires it.
- Confirm by physical inspection.
- Use cautious language.

## Official prompt 2 key points

Expected answer should mention:

- Pesticide and herbicide risk from pepper and vegetable farms.
- Coordinate with farmers on spray timing and bee-safe practices.
- Check whether seasonal water is reliable through dry periods.
- Plan clean backup water if the source dries up.
- Evaluate forage diversity and flowering seasonality.
- Mango is seasonal forage.
- Cassava should not be assumed to be enough forage.
- Check shade, wind, heat, drainage, and flooding risk.
- Check human, livestock, roads, paths, schools, and farm safety.
- Check access for inspection and harvest.
- Consider hive spacing, stand height, and whether the site supports 20 hives.
- Consider staged placement if uncertain.
- Use cautious site-readiness language.

---

## Score table

| Prompt ID | Gemma score /5 | Granite score /5 | Winner | Notes |
|---|---:|---:|---|---|
| official_hive_ants |  |  |  |  |
| official_site_20_hives |  |  |  |  |
| proxy_heat_stress |  |  |  |  |
| proxy_weak_colony |  |  |  |  |
| proxy_wax_moth |  |  |  |  |
| proxy_pesticide_risk |  |  |  |  |
| proxy_water_dry_season |  |  |  |  |
| proxy_harvest_quality |  |  |  |  |
| proxy_forage_gap |  |  |  |  |
| proxy_absconding_risk |  |  |  |  |
| **Total** |  |  |  |  |
