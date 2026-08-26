#!/usr/bin/env python3
"""Import claude.ai chat conversations into the harvest queue.

The claude.ai web/desktop app stores conversations server-side, so capture goes
through the official data export (claude.ai → Settings → Privacy → Export data;
a download link arrives by email). Point this script at the downloaded zip or at
conversations.json:

    bin/import_chats.py ~/Downloads/data-2026-08-26.zip
    bin/import_chats.py conversations.json

Each substantial conversation becomes a plain-text file in data/chat_imports/
(git-ignored, pre-redaction) and a queue entry the daily harvester picks up like
any Claude Code session.
"""
import json
import os
import sys
import time
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(REPO, "data", "queue", "pending.jsonl")
PROCESSED = os.path.join(REPO, "data", "queue", "processed.jsonl")
IMPORTS = os.path.join(REPO, "data", "chat_imports")
MIN_CHARS = 4000  # chats are lighter than code sessions


def load_conversations(path):
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            names = [n for n in z.namelist() if n.endswith("conversations.json")]
            if not names:
                sys.exit("no conversations.json in this zip — is it a claude.ai data export?")
            return json.loads(z.read(names[0]))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def message_text(m):
    text = m.get("text") or ""
    if not text and isinstance(m.get("content"), list):
        text = "\n".join(b.get("text", "") for b in m["content"]
                         if isinstance(b, dict) and b.get("type") == "text")
    return text.strip()


def seen_sessions(path):
    ids = set()
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    ids.add(json.loads(line).get("session_id"))
                except (json.JSONDecodeError, AttributeError):
                    pass
    except OSError:
        pass
    return ids


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    convs = load_conversations(sys.argv[1])
    seen = seen_sessions(QUEUE) | seen_sessions(PROCESSED)
    os.makedirs(IMPORTS, exist_ok=True)
    queued = skipped_small = skipped_seen = 0
    with open(QUEUE, "a", encoding="utf-8") as q:
        for c in convs:
            uuid = c.get("uuid", "")
            sid = f"chat-{uuid}"
            if not uuid or sid in seen:
                skipped_seen += bool(uuid)
                continue
            parts = []
            for m in c.get("chat_messages", []):
                text = message_text(m)
                if not text:
                    continue
                role = "USER" if m.get("sender") == "human" else "ASSISTANT"
                parts.append(f"[{role}]\n{text}")
            convo = "\n\n".join(parts)
            if len(convo) < MIN_CHARS:
                skipped_small += 1
                continue
            title = (c.get("name") or "sans-titre").strip()
            txt_path = os.path.join(IMPORTS, f"{uuid}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(f"[Conversation claude.ai : {title}]\n\n{convo}")
            q.write(json.dumps({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "session_id": sid,
                "transcript_path": txt_path,
                "cwd": "/import/claude-chat",
                "project": "claude-chat",
            }, ensure_ascii=False) + "\n")
            queued += 1
    print(f"{queued} conversation(s) en queue, {skipped_small} trop courtes, "
          f"{skipped_seen} déjà connues")
    if queued:
        print("→ extraction au prochain harvest (19:30) ou tout de suite : python3 bin/harvest.py")


if __name__ == "__main__":
    main()
