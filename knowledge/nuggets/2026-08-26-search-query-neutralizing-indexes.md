---
topic: search-query-neutralizing-indexes
date: 2026-08-26
project: ao-assurance
session: a8ff953a
density: 4
tone: factual
lang_hint: en
tags: [sql-optimization, measurement, performance]
status: new
---
A query using **LIKE '%q%'** with **a function on the column** (`UPPER(colname)`) defeats all indexes, even if they exist. The planner falls back to a full table scan applying predicates row-by-row.

Measured on 100k rows: query cost 162.2 (DB2 estimate) → 27.9 after reclassing to prefix search with lexical aiguillage. Cost becomes **constant**, not linear.

The fix: qualify the input **before** querying. A 6-digit string goes to CIN/police; text goes to name search; a plate format goes to vehicle table. Route each to a dedicated, prefix-based query. Loses substring search, but that trade-off is usually **metadata, not requirement**—confirm with the business.
