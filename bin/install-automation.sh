#!/bin/bash
# Installs the two background pieces:
#  1. SessionEnd hook in ~/.claude/settings.json  (capture — free, instant)
#  2. LaunchAgent running bin/harvest.py daily at 19:30  (extraction — batched)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"

# --- 1. hook ---
python3 - "$REPO" <<'PY'
import json, sys, os
repo = sys.argv[1]
path = os.path.expanduser("~/.claude/settings.json")
with open(path) as f:
    cfg = json.load(f)
cmd = f"python3 {repo}/bin/enqueue.py"
hooks = cfg.setdefault("hooks", {}).setdefault("SessionEnd", [])
already = any(h.get("command") == cmd for grp in hooks for h in grp.get("hooks", []))
if not already:
    hooks.append({"hooks": [{"type": "command", "command": cmd}]})
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)
    print("hook SessionEnd installé")
else:
    print("hook SessionEnd déjà présent")
PY

# --- 2. LaunchAgent (daily harvest 19:30) ---
PLIST="$HOME/Library/LaunchAgents/com.curator.harvest.plist"
cat > "$PLIST" <<XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.curator.harvest</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
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
echo
echo "Curation : manuelle via 'bin/curate.sh' ou '/curator curate' dans une session."
