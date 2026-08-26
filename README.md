# curator

Pipeline git-only qui écoute mes sessions Claude Code et les transforme en contenu
publiable : **tweets**, **posts LinkedIn**, **articles** (fr / en / darija لتّرجة بالحروف العربية).
Déployé sur GitHub Pages, zéro backend.

## Architecture

```
Session Claude Code
   └─ hook SessionEnd (bin/enqueue.py)      capture gratuite → data/queue/pending.jsonl
        └─ LaunchAgent quotidien 19:30 (bin/harvest.py)
             ├─ lib/extract_text.py         texte conversationnel seul
             ├─ claude -p (Haiku)           0-4 nuggets / session, alias imposés
             ├─ lib/redact.py               passe regex secrets/chemins → _review/ si doute
             └─ knowledge/nuggets/*.md      commit + push
                  └─ /curator curate        cluster → score → route → drafts/
                       └─ /curator publish  → published/ + site/src/content/articles/
                            └─ GitHub Actions → GitHub Pages
```

## Installation

```bash
bin/install-automation.sh   # hook SessionEnd + LaunchAgent quotidien
cd site && npm install      # site Astro
```

## Commandes

| Commande | Effet |
|---|---|
| `bin/harvest.py` | Draine la queue → nuggets (aussi lancé par le LaunchAgent) |
| `bin/import_chats.py <export>` | Importe les chats claude.ai (export Settings → Privacy) dans la queue |
| `bin/curate.sh` ou `/curator curate` | Cluster + routage + rédaction des drafts |
| `/curator publish <draft>` | Publie (article → site, post → published/) |
| `/curator review` | Traite les nuggets à confidentialité douteuse |
| `/curator status` | État du pipeline |

## Plusieurs machines

Le pipeline est git-based précisément pour ça : chaque machine capture ses propres
sessions et pousse ses nuggets dans le même repo.

```bash
# sur l'autre machine (ex. celle des sessions LLM locaux)
git clone https://github.com/bzinoun/curator && cd curator
bin/install-automation.sh        # hook SessionEnd + harvest quotidien locaux
```

La queue (`data/queue/`) et les imports (`data/chat_imports/`) sont git-ignorés —
état local par machine. Seuls les nuggets anonymisés convergent. Pour rattraper des
sessions passées sur cette machine sans attendre le cron : remplir la queue à la
main (voir `bin/enqueue.py`) puis `python3 bin/harvest.py`.

## Routage éditorial

| Signal | Format |
|---|---|
| Cluster ≥3 nuggets denses, matière à schéma | **Article** (Mermaid/drawio/BPMN, 800-2500 mots) |
| Avis tranché défendable | **LinkedIn** (≤1300 chars, direct, image ou lien obligatoire) |
| Punchline | **Tweet** (fun/décalé, darija bienvenue, image ou lien obligatoire) |

La confidentialité est structurelle : alias dans `config/redaction.json`, double passe
(prompt + regex), file `_review/` pour tout ce qui doute. Rien ne se publie seul —
l'humain valide les drafts et poste lui-même sur les réseaux.
