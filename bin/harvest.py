#!/usr/bin/env python3
"""Daily harvester: drain the transcript queue into knowledge nuggets.

For each queued session: extract conversational text, ask a cheap model to mine
publishable nuggets (redaction rules injected in the prompt), run a mechanical
redaction pass on the output, write nugget files, then commit & push.
Designed to run headless from launchd/cron.
"""
import json
import os
import re
import subprocess
import sys
import time
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(REPO, "data", "queue", "pending.jsonl")
PROCESSED = os.path.join(REPO, "data", "queue", "processed.jsonl")
NUGGETS = os.path.join(REPO, "knowledge", "nuggets")
REVIEW = os.path.join(NUGGETS, "_review")
LOCK = os.path.join(REPO, "data", ".harvest.lock")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60] or "nugget"


def take_lock():
    if os.path.exists(LOCK):
        if time.time() - os.path.getmtime(LOCK) < 7200:
            print("harvest already running, abort")
            sys.exit(0)
        os.remove(LOCK)  # stale lock
    open(LOCK, "w").close()


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def extract_convo(transcript, max_chars):
    r = run([sys.executable, os.path.join(REPO, "lib", "extract_text.py"),
             transcript, str(max_chars)])
    return r.stdout if r.returncode == 0 else ""


def mine(cfg, convo, project, aliases):
    prompt = open(os.path.join(REPO, "prompts", "extract.md"), encoding="utf-8").read()
    prompt = prompt.replace("{PROJECT}", project).replace("{ALIASES}", json.dumps(aliases, ensure_ascii=False))
    r = run([cfg["claude_bin"], "-p", prompt, "--model", cfg["extract_model"],
             "--allowedTools", ""], input=convo, timeout=600)
    if r.returncode != 0:
        print(f"  claude failed: {r.stderr[:300]}")
        return None
    return r.stdout


def redact(text):
    r = run([sys.executable, os.path.join(REPO, "lib", "redact.py")], input=text)
    return r.stdout, r.returncode == 3


def parse_nuggets(raw):
    for block in raw.split("=== NUGGET ==="):
        block = block.strip()
        if not block or "---" not in block:
            continue
        header, _, body = block.partition("---")
        meta = {}
        for line in header.strip().splitlines():
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
        if meta.get("topic") and body.strip():
            yield meta, body.strip()


def write_nugget(meta, body, project, session_id, needs_review):
    date = time.strftime("%Y-%m-%d")
    slug = slugify(meta["topic"])
    dest_dir = REVIEW if needs_review else NUGGETS
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, f"{date}-{slug}.md")
    n = 1
    while os.path.exists(path):
        n += 1
        path = os.path.join(dest_dir, f"{date}-{slug}-{n}.md")
    fm = [
        "---",
        f"topic: {meta['topic']}",
        f"date: {date}",
        f"project: {project}",
        f"session: {session_id[:8]}",
        f"density: {meta.get('density', '2')}",
        f"tone: {meta.get('tone', 'factual')}",
        f"lang_hint: {meta.get('lang_hint', 'fr')}",
        f"tags: [{meta.get('tags', '')}]",
        "status: new",
        "---",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(fm) + body + "\n")
    return path


def git_sync(n_new):
    run(["git", "add", "-A"], cwd=REPO)
    st = run(["git", "status", "--porcelain"], cwd=REPO)
    if not st.stdout.strip():
        return
    msg = f"harvest: {n_new} nugget(s) — {time.strftime('%Y-%m-%d')}"
    run(["git", "commit", "-m", msg], cwd=REPO)
    if run(["git", "remote"], cwd=REPO).stdout.strip():
        p = run(["git", "push"], cwd=REPO)
        if p.returncode != 0:
            print(f"push failed: {p.stderr[:300]}")


def main():
    cfg = load_json(os.path.join(REPO, "config", "curator.json"))
    aliases = load_json(os.path.join(REPO, "config", "redaction.json"))["replacements"]
    if not os.path.isfile(QUEUE):
        print("empty queue")
        return
    take_lock()
    try:
        entries = [json.loads(l) for l in open(QUEUE, encoding="utf-8") if l.strip()]
        remaining, total_nuggets = [], 0
        for e in entries:
            sid = e.get("session_id", "?")[:8]
            print(f"session {sid} ({e.get('project')})")
            if not os.path.isfile(e.get("transcript_path", "")):
                print("  transcript gone, drop")
                continue
            convo = extract_convo(e["transcript_path"], cfg["max_convo_chars"])
            if len(convo) < 2000:
                print("  too little text, drop")
                continue
            raw = mine(cfg, convo, e.get("project", "unknown"), aliases)
            if raw is None:
                remaining.append(e)  # retry next run
                continue
            if "NO_NUGGETS" in raw[:200]:
                print("  no nuggets")
            else:
                for meta, body in parse_nuggets(raw):
                    body, dirty = redact(body)
                    path = write_nugget(meta, body, e.get("project", "unknown"),
                                        e.get("session_id", ""), dirty)
                    total_nuggets += 1
                    print(f"  + {os.path.relpath(path, REPO)}{'  [REVIEW]' if dirty else ''}")
            with open(PROCESSED, "a", encoding="utf-8") as f:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        with open(QUEUE, "w", encoding="utf-8") as f:
            for e in remaining:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        git_sync(total_nuggets)
        print(f"done: {total_nuggets} nugget(s)")
    finally:
        os.remove(LOCK)


if __name__ == "__main__":
    main()
