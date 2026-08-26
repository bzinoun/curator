#!/bin/bash
# Headless curation: cluster fresh nuggets, route them to tweet/linkedin/article,
# write drafts. The editorial logic lives in .claude/skills/curator/SKILL.md.
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"
CLAUDE_BIN="$(jq -r .claude_bin config/curator.json)"
CURATE_MODEL="$(jq -r .curate_model config/curator.json)"
"$CLAUDE_BIN" -p "/curator curate" --model "$CURATE_MODEL" \
  --allowedTools "Read,Glob,Grep,Write,Edit,Bash(git add:*),Bash(git commit:*),Bash(git push:*),Bash(git status:*),Bash(ls:*)" \
  2>&1 | tee -a data/logs/curate.log
