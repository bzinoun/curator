# Cluster : SQL perf legacy — les index qu'on suppose
Membres :
- 2026-08-26-search-query-neutralizing-indexes.md
- 2026-08-26-index-discovery-by-measurement.md

Synthèse : sur un legacy DB2 (100k lignes), `LIKE '%q%'` + `UPPER(col)` neutralise tous
les index (coût 162 → 28 après aiguillage lexical vers des recherches par préfixe), et une
colonne filtrée partout n'était jamais indexée (6× de gain, coût constant). Seul un
`EXPLAIN` sur charge réaliste révèle les deux. → LinkedIn FR (2 membres ; article si un 3e arrive).
