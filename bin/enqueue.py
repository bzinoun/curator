#!/usr/bin/env python3
"""SessionEnd hook: enqueue a transcript pointer for later harvesting.

Reads the hook payload on stdin. Must be fast and must NEVER fail the session:
every error path exits 0. No model call happens here — capture is free.
"""
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(REPO, "data", "queue", "pending.jsonl")
PROCESSED = os.path.join(REPO, "data", "queue", "processed.jsonl")


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
    try:
        payload = json.load(sys.stdin)
        transcript = payload.get("transcript_path", "")
        cwd = payload.get("cwd", "")
        session_id = payload.get("session_id", "")
        # never listen to the curator itself (feedback loop)
        if not transcript or REPO in cwd:
            return
        min_bytes = 20000
        try:
            with open(os.path.join(REPO, "config", "curator.json"), encoding="utf-8") as f:
                min_bytes = json.load(f).get("min_transcript_bytes", min_bytes)
        except OSError:
            pass
        if not os.path.isfile(transcript) or os.path.getsize(transcript) < min_bytes:
            return
        if session_id in seen_sessions(QUEUE) | seen_sessions(PROCESSED):
            return
        entry = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "session_id": session_id,
            "transcript_path": transcript,
            "cwd": cwd,
            "project": os.path.basename(cwd.rstrip("/")) if cwd else "unknown",
        }
        os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
        with open(QUEUE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # a hook failure must never surface in the session
    sys.exit(0)


if __name__ == "__main__":
    main()
