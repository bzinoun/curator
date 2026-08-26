# Installer curator sur une nouvelle machine

Objectif : que cette machine **capture ses propres sessions Claude Code** et pousse
ses nuggets anonymisés dans ce repo. La curation et le site restent centralisés —
n'importe quelle machine peut les lancer, une seule en a besoin.

## Prérequis

| Outil | Vérification | Note |
|---|---|---|
| git + accès en écriture au repo | `git push` fonctionne | via `gh auth login` ou clé SSH |
| Claude Code CLI | `claude --version` | l'installeur détecte son chemin |
| python3 | `python3 --version` | stdlib uniquement, aucun pip install |
| jq | `jq --version` | utilisé par les scripts shell |

macOS et Linux supportés (LaunchAgent ou crontab, choisi automatiquement).

## Installation — 3 commandes

```bash
git clone https://github.com/bzinoun/curator && cd curator
bin/install-automation.sh
bin/backfill.py --dry-run
```

`install-automation.sh` fait deux choses, de façon idempotente :

1. **Hook `SessionEnd`** dans `~/.claude/settings.json` — chaque session terminée
   sur cette machine (> 20 Ko) est empilée dans `data/queue/pending.jsonl`.
   Capture instantanée, zéro token.
2. **Harvest quotidien 19:30** (LaunchAgent macOS / crontab Linux) — draine la
   queue via Haiku, écrit les nuggets anonymisés, commit + push.

Il détecte aussi le chemin du CLI `claude` et l'écrit dans `config/curator.json`
(ce chemin est propre à chaque machine — c'est normal qu'il change après un pull,
ne pas s'en inquiéter).

## Rattraper les sessions passées

Le hook ne capture que le futur. Pour l'historique de cette machine :

```bash
bin/backfill.py --dry-run              # voir ce qui serait enqueué (90 jours)
bin/backfill.py --days 365             # élargir la fenêtre
bin/backfill.py --project llm          # cibler un projet (ex: sessions LLM locaux)
bin/backfill.py                        # enqueuer pour de vrai
```

**⚠️ Avant de lancer le harvest** : ouvre `config/redaction.json` et ajoute les
noms de clients/entreprises/projets sensibles propres à cette machine dans
`replacements`. Le repo est public — tout ce qui n'est pas aliasé peut fuiter
dans un nugget. Dans le doute, ajoute l'alias.

Puis :

```bash
python3 bin/harvest.py                 # ou attendre 19:30
```

Les nuggets arrivent dans `knowledge/nuggets/` et sont poussés automatiquement.

## Ce qui est partagé vs local

| Partagé (git) | Local (git-ignoré, par machine) |
|---|---|
| nuggets, clusters, drafts, published | `data/queue/` (pointeurs de transcripts) |
| config (`curator.json`, `redaction.json`) | `data/chat_imports/`, `data/logs/` |
| skill, scripts, site | chemin `claude_bin` (réécrit par l'installeur) |

Deux machines peuvent harvester le même jour sans conflit : les nuggets sont des
fichiers nouveaux. Si un `git push` est rejeté, le prochain harvest repoussera —
ou `git pull --rebase && git push` à la main.

## Curation et publication (depuis n'importe quelle machine)

```bash
claude                    # dans le repo
> /curator status         # état du pipeline
> /curator curate         # cluster + route + rédige (articles écrits par Fable)
> /curator publish <draft>
```

Ou en headless : `bin/curate.sh`. Le push d'un article déclenche le déploiement
GitHub Pages ; rien ne se poste seul sur les réseaux sociaux.

## Vérifier que ça tourne

```bash
tail -5 data/queue/pending.jsonl       # les sessions s'empilent ?
tail -20 data/logs/harvest.log         # dernier harvest
launchctl list | grep curator          # macOS
crontab -l | grep harvest              # Linux
```
