#!/usr/bin/env python3
"""Enqueue past Claude Code sessions of THIS machine for harvesting.

Scans ~/.claude/projects for main-session transcripts (subagents and automated
worktrees excluded), filters by size and age, dedupes against the queue, and
derives each session's project label from its real cwd.

Usage:
  bin/backfill.py --dry-run              # list what would be enqueued
  bin/backfill.py                        # enqueue (last 90 days by default)
  bin/backfill.py --days 365             # go further back
  bin/backfill.py --project llm          # only project dirs matching "llm"

Après enqueue : vérifie config/redaction.json (nouveaux noms de clients à aliaser ?)
puis lance `python3 bin/harvest.py`.
"""
import argparse
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS = os.path.expanduser("~/.claude/projects")
QUEUE = os.path.join(REPO, "data", "queue", "pending.jsonl")
PROCESSED = os.path.join(REPO, "data", "queue", "processed.jsonl")
EXCLUDE_DIR_PARTS = ("worktrees", "-private-tmp", "workspace-curator")


def seen_sessions():
    ids = set()
    for path in (QUEUE, PROCESSED):
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


def read_cwd(transcript):
    """The real cwd is recorded inside the transcript entries."""
    try:
        with open(transcript, encoding="utf-8", errors="replace") as f:
            for _ in range(50):
                line = f.readline()
                if not line:
                    break
                try:
                    cwd = json.loads(line).get("cwd")
                    if cwd:
                        return cwd
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--days", type=int, default=90, help="âge max des sessions (défaut 90)")
    ap.add_argument("--project", default="", help="filtre sous-chaîne sur le dossier projet")
    ap.add_argument("--dry-run", action="store_true", help="lister sans enqueuer")
    args = ap.parse_args()

    cfg = json.load(open(os.path.join(REPO, "config", "curator.json"), encoding="utf-8"))
    min_bytes = cfg.get("min_transcript_bytes", 20000)
    cutoff = time.time() - args.days * 86400
    seen = seen_sessions()
    candidates = []

    for proj_dir in sorted(os.listdir(PROJECTS)):
        full = os.path.join(PROJECTS, proj_dir)
        if not os.path.isdir(full):
            continue
        if any(part in proj_dir for part in EXCLUDE_DIR_PARTS):
            continue
        if args.project and args.project.lower() not in proj_dir.lower():
            continue
        for name in os.listdir(full):
            if not name.endswith(".jsonl"):
                continue  # skips subagent subdirs too (they are directories)
            path = os.path.join(full, name)
            st = os.stat(path)
            if st.st_size < min_bytes or st.st_mtime < cutoff:
                continue
            sid = name[:-6]
            if sid in seen:
                continue
            cwd = read_cwd(path)
            project = os.path.basename(cwd.rstrip("/")) if cwd else proj_dir.split("-")[-1]
            candidates.append({"session_id": sid, "transcript_path": path,
                               "cwd": cwd or "/backfill/" + project, "project": project,
                               "size": st.st_size, "mtime": st.st_mtime})

    candidates.sort(key=lambda c: -c["size"])
    if not candidates:
        print("rien à rattraper (déjà en queue, trop vieux ou trop petit)")
        return
    for c in candidates:
        print(f"  {c['project']:30s} {c['size'] // 1024:8d}KB  "
              f"{time.strftime('%Y-%m-%d', time.localtime(c['mtime']))}  {c['session_id'][:8]}")
    if args.dry_run:
        print(f"\n{len(candidates)} session(s) — relance sans --dry-run pour enqueuer")
        return
    os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
    with open(QUEUE, "a", encoding="utf-8") as f:
        for c in candidates:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                "session_id": c["session_id"],
                                "transcript_path": c["transcript_path"],
                                "cwd": c["cwd"], "project": c["project"]},
                               ensure_ascii=False) + "\n")
    print(f"\n{len(candidates)} session(s) en queue.")
    print("1. Vérifie config/redaction.json — nouveaux noms clients/projets à aliaser ?")
    print("2. Puis : python3 bin/harvest.py")


if __name__ == "__main__":
    main()
