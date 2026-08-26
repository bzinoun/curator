# Specs des trois formats

## Article (deep dive)

- **But** : lecture profonde ; explique UN élément fort de bout en bout.
- **Langues** : anglais ou français (Darija possible mais rare — sujet culturel tech local).
- **Structure** : hook (le problème vécu) → contexte généralisé → mécanisme expliqué
  (schémas !) → trade-offs honnêtes → ce qu'on referait différemment → takeaways.
- **Longueur** : 800–2500 mots.
- **Visuels obligatoires** : au moins un schéma qui porte l'explication —
  Mermaid (flowchart, sequenceDiagram, C4), BPMN/ArchiMate via fichier
  `assets/diagrams/<slug>.drawio` + export SVG référencé dans le markdown,
  croquis, ou tableau comparatif. Un schéma décoratif ne compte pas.
- **Ton** : pédagogique, précis, sans jargon gratuit ; les termes techniques restent
  en anglais même dans un article en français.

## Post LinkedIn

- **But** : avis tranché, clair, direct. Dire simplement les choses, concis, sans
  diplomatie excessive. Une seule idée par post.
- **Langues** : français ou anglais selon l'audience de l'idée.
- **Structure** : accroche 1 ligne (la position) → 3-6 lignes de justification vécue
  → 1 ligne de chute ou question. Pas de "Thread 🧵", pas de storytelling gonflé,
  pas d'emojis en rafale (0 à 2 max).
- **Longueur** : ≤ 1300 caractères (au-delà, LinkedIn tronque avant "voir plus" — le
  hook doit tenir dans les 210 premiers caractères).
- **Accompagnement obligatoire** : une image (brief dans `visual:`) OU un lien vers
  un article — le nôtre (site Pages) ou externe.

## Tweet

- **But** : format court, 1 tweet max (Premium : jusqu'à 4000 chars mais viser < 500).
  Plus fun, décalé, style simple, décontracté et direct.
- **Langues** : les trois — c'est le format naturel de la Darija (lettres arabes).
- **Structure** : la punchline d'abord. Autodérision et concret > leçon de morale.
- **Accompagnement obligatoire** : image (brief dans `visual:`) ou lien article.

## Langues — règles de choix

- `fr` : défaut pro ; sujets archi/orga, audience LinkedIn francophone.
- `en` : sujet à portée internationale (outillage, frameworks, Claude Code, Garmin…),
  articles techniques pointus, tweets dev.
- `ary` (Darija, lettres arabes, dir=rtl) : ton fun/culturel, punchlines, tweets
  décalés, réalités du terrain tech au Maroc. Jamais forcé sur un sujet froid.
- **Mélange autorisé** : citer un terme/une phrase dans une autre langue que la
  langue principale du post (ex. punchline darija dans un post fr, terme en anglais
  partout). Le corps reste cohérent dans la langue principale.

## Frontmatter draft (obligatoire)

```yaml
---
title: "..."
format: article | linkedin | tweet
lang: fr | en | ary
status: draft            # draft → published
date: YYYY-MM-DD
nuggets: [2026-08-26-topic.md, ...]
visual: "mermaid inline" | "assets/diagrams/x.drawio.svg" | "brief: <description image>"
link: ""                 # URL article lié, si applicable
---
```
