---
topic: index-discovery-by-measurement
date: 2026-08-26
project: ao-assurance
session: a8ff953a
density: 3
tone: factual
lang_hint: en
tags: [database, observability, methodology]
status: drafted
---
Don't assume indexes are "present and working"—**measure the plan**. A column used in filtering but carrying no dedicated index can hide under a primary-key index that's used only for sort, neutralizing its filtering power.

Found here: a contracts-table column (agent code) was queried on 100k rows in every search-by-agent, but never indexed. The planner used a composite PK for ordering but read all rows before filtering. Adding the index dropped cost by 6× and made it **constant**, not linear.

Human code review rarely catches this. A `EXPLAIN` or plan capture on a realistic workload will.
