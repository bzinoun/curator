---
name: curator
description: >
  Content curator turning harvested Claude Code session knowledge into publishable
  content — tweets, LinkedIn posts, deep articles (fr / en / Moroccan Darija in Arabic
  script). Use when the user says /curator, asks to curate nuggets, draft a post,
  write an article from harvested knowledge, publish a draft, or check pipeline status.
---

# Curator — de la session de code au contenu publiable

Repo pipeline : `data/queue` (transcripts en attente) → `knowledge/nuggets` (insights
extraits) → `drafts/` (contenu rédigé) → `published/` + `site/src/content/articles`
(publié, déployé sur GitHub Pages).

## Commandes

- `/curator status` — état du pipeline (queue, nuggets par statut, drafts en attente).
- `/curator harvest` — lance `python3 bin/harvest.py` puis résume ce qui a été extrait.
- `/curator curate` — le cœur : cluster + route + rédige (workflow ci-dessous).
- `/curator publish <draft>` — publie un draft validé (workflow Publication).
- `/curator import-chats <export.zip|conversations.json>` — importe les conversations
  claude.ai (via `bin/import_chats.py` ; l'export se demande dans claude.ai →
  Settings → Privacy → Export data, lien reçu par email). Les conversations
  substantielles rejoignent la queue et suivent le pipeline normal.
- `/curator review` — traite `knowledge/nuggets/_review/` (nuggets à confidentialité douteuse) : corriger et sortir de _review, ou supprimer.

## Workflow curate

1. **Inventaire** : lire tous les nuggets `status: new` dans `knowledge/nuggets/`
   (jamais `_review/` — ceux-là attendent une validation humaine).
2. **Clustering** : regrouper par thème. Un cluster = même sujet de fond, pas même
   projet. Écrire/mettre à jour `knowledge/clusters/<theme>.md` (liste des nuggets
   membres + synthèse 3 lignes).
3. **Scoring & routage** — pour chaque cluster ou nugget isolé :

   | Signal | Format |
   |---|---|
   | Cluster ≥ 3 nuggets, density moyenne ≥ 3, matière à schéma/tableau | **Article** |
   | 1-2 nuggets, `tone: opinionated`, position claire et défendable | **LinkedIn** |
   | 1 nugget, punchy, `tone: fun` ou factuel court | **Tweet** |
   | density 1 sans angle | rien — marquer `status: parked` |

   Ne pas forcer : un cycle curate peut produire zéro draft. Qualité > cadence.
4. **Choix de langue** (voir `references/formats.md` §Langues) : décider par contenu,
   pas par habitude. Citer un terme dans une autre langue que la principale est permis.
5. **Rédaction** : écrire le draft selon les specs de `references/formats.md`.
   Nommage : `drafts/<type>/YYYY-MM-DD-<slug>.md`. Frontmatter obligatoire :
   `title, format, lang, status: draft, nuggets: [fichiers sources], visual: <spec>`.
6. **Visuels** :
   - Article : diagrammes Mermaid inline (flowchart, sequence, C4) et/ou fichier
     `.drawio` + export `.drawio.svg` dans `assets/diagrams/`. Tableaux markdown natifs.
   - LinkedIn / Tweet : écrire un brief image précis dans le champ `visual:` du
     frontmatter (sujet, style, texte à incruster, format 1200x627 ou 16:9). Si le
     skill `banner-design` ou `design` est disponible dans la session, générer
     l'image dans `assets/images/` et référencer le fichier.
7. **Marquage** : passer les nuggets utilisés à `status: drafted`.
8. **Commit** : `git add -A && git commit -m "curate: <n> draft(s) — <themes>"` puis
   `git push` si un remote existe.

## Workflow publish

1. Lire le draft ; vérifier `status: draft` et relire une dernière fois la
   confidentialité (aucun nom réel, chemin, secret — cf. `config/redaction.json`).
2. **Article** : copier vers `site/src/content/articles/<slug>.md` avec le frontmatter
   du schéma site (`title, description, lang, date, tags, draft: false`). Passer le
   draft d'origine à `status: published`. Le push déclenche le déploiement Pages.
3. **LinkedIn / Tweet** : déplacer vers `published/<type>/` ; le texte est prêt à
   coller. Si le post référence un article, insérer l'URL
   `{site_base_url}/articles/<slug>/` (base dans `config/curator.json`).
4. Commit + push.

## Règles transverses

- **Confidentialité d'abord** : les alias de `config/redaction.json` s'appliquent à
  tout contenu produit. En cas de doute sur un détail → le généraliser ou le couper.
- **Honnêteté** : pas de métriques inventées, pas de superlatifs marketing. Une
  opinion tranchée s'appuie sur ce qui a été réellement vécu dans les sessions.
- **Un draft = autonome** : compréhensible sans avoir lu le nugget source.
- Ne jamais publier directement sur les réseaux : le repo produit des textes et
  visuels prêts à poster, l'humain poste.
