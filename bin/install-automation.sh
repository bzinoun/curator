#!/bin/bash
# Installs the two background pieces on THIS machine:
#  1. SessionEnd hook in ~/.claude/settings.json  (capture — free, instant)
#  2. Daily harvest at 19:30 — LaunchAgent on macOS, crontab on Linux
# Idempotent: safe to re-run.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"

# --- 0. locate the claude CLI and pin it in config ---
CLAUDE_BIN="$(jq -r '.claude_bin // empty' "$REPO/config/curator.json" 2>/dev/null || true)"
if [ ! -x "${CLAUDE_BIN:-/nonexistent}" ]; then
  for c in "$HOME/.local/bin/claude" "$HOME/.claude/local/claude" "$(command -v claude || true)"; do
    [ -x "${c:-/nonexistent}" ] && CLAUDE_BIN="$c" && break
  done
  if [ ! -x "${CLAUDE_BIN:-/nonexistent}" ]; then
    echo "ERREUR: claude CLI introuvable. Installe Claude Code puis relance." >&2
    exit 1
  fi
  tmp=$(mktemp)
  jq --arg c "$CLAUDE_BIN" '.claude_bin = $c' "$REPO/config/curator.json" > "$tmp" \
    && mv "$tmp" "$REPO/config/curator.json"
  echo "claude_bin -> $CLAUDE_BIN (écrit dans config/curator.json)"
fi

# --- 1. hook SessionEnd ---
python3 - "$REPO" <<'PY'
import json, sys, os
repo = sys.argv[1]
path = os.path.expanduser("~/.claude/settings.json")
cfg = {}
if os.path.isfile(path):
    with open(path) as f:
        cfg = json.load(f)
cmd = f"python3 {repo}/bin/enqueue.py"
hooks = cfg.setdefault("hooks", {}).setdefault("SessionEnd", [])
already = any(h.get("command") == cmd for grp in hooks for h in grp.get("hooks", []))
if not already:
    hooks.append({"hooks": [{"type": "command", "command": cmd}]})
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print("hook SessionEnd installé")
else:
    print("hook SessionEnd déjà présent")
PY

# --- 2. daily harvest 19:30 ---
PYBIN="$(command -v python3)"
if [ "$(uname)" = "Darwin" ]; then
  PLIST="$HOME/Library/LaunchAgents/com.curator.harvest.plist"
  cat > "$PLIST" <<XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.curator.harvest</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYBIN</string>
    <string>$REPO/bin/harvest.py</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>19</integer><key>Minute</key><integer>30</integer></dict>
  <key>StandardOutPath</key><string>$REPO/data/logs/harvest.log</string>
  <key>StandardErrorPath</key><string>$REPO/data/logs/harvest.err.log</string>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$HOME/.local/bin</string></dict>
</dict>
</plist>
XML
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
  echo "LaunchAgent com.curator.harvest chargé (quotidien 19:30)"
else
  LINE="30 19 * * * $PYBIN $REPO/bin/harvest.py >> $REPO/data/logs/harvest.log 2>&1"
  ( crontab -l 2>/dev/null | grep -vF "bin/harvest.py" ; echo "$LINE" ) | crontab -
  echo "crontab installé (quotidien 19:30)"
fi
mkdir -p "$REPO/data/logs" "$REPO/data/queue"
echo
echo "Capture active pour les prochaines sessions. Sessions passées : bin/backfill.py --dry-run"
