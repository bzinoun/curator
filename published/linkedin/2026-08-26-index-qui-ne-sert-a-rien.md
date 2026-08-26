---
title: "Vos index existent. Ils ne servent à rien."
format: linkedin
lang: fr
status: published
date: 2026-08-26
nuggets:
  - 2026-08-26-search-query-neutralizing-indexes.md
  - 2026-08-26-index-discovery-by-measurement.md
visual: "brief: image 1200x627, fond sombre (Majorelle), deux barres horizontales côte à côte — 'coût 162' longue en rouge vs 'coût 28' courte en saffron — avec la légende 'même table, même index, requête différente'. Style flat, typographie grasse, pas d'icône DB cliché."
link: ""
---
Un index qu'on ne mesure pas est un index qu'on suppose. Et une supposition, ça ne filtre pas 100 000 lignes.

Deux découvertes la même semaine, sur un legacy DB2 d'assurance :

1. Une recherche en `LIKE '%q%'` avec `UPPER(colonne)`. Les index sont là, bien créés. Le planner les ignore tous : function sur la colonne + joker en tête = full scan, prédicat appliqué ligne par ligne. Coût estimé : 162.

2. Une colonne "code agent" filtrée dans chaque recherche par agent. Jamais indexée. Le planner utilise la PK composite… pour trier. Il lit tout, puis filtre.

Aucune revue de code n'aurait vu ça. Le code est propre. Les index "existent". C'est le `EXPLAIN` sur une charge réaliste qui a parlé.

Le fix, ce n'est pas plus d'index. C'est qualifier l'entrée AVANT de requêter : 6 chiffres → police, texte → nom, format plaque → véhicule. Chaque route tape un préfixe indexé. Coût : 162 → 28, et surtout constant au lieu de linéaire.

On perd la recherche par sous-chaîne. On l'a demandé au métier : personne ne l'utilisait. C'était de la métadonnée, pas une exigence.

Vous mesurez vos plans, ou vous faites confiance à la présence des index ?
