#!/usr/bin/env python3
"""Extract user/assistant text from a Claude Code transcript (.jsonl).

Tool calls, tool results and meta events are dropped: only the conversational
text survives, which is what the harvester mines for knowledge.
Usage: extract_text.py <transcript.jsonl> [max_chars]
"""
import json
import sys


def block_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text":
                parts.append(b.get("text", ""))
        return "\n".join(parts)
    return ""


def main():
    path = sys.argv[1]
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 120000
    out = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") not in ("user", "assistant"):
                continue
            if obj.get("isMeta"):
                continue
            msg = obj.get("message") or {}
            text = block_text(msg.get("content")).strip()
            if not text or text.startswith("<system-reminder>"):
                continue
            role = "USER" if obj["type"] == "user" else "ASSISTANT"
            out.append(f"[{role}]\n{text}")
    convo = "\n\n".join(out)
    if len(convo) > max_chars:
        # keep the opening context and the (denser) end of the session
        head = convo[: int(max_chars * 0.3)]
        tail = convo[-int(max_chars * 0.7):]
        convo = head + "\n\n[... transcript tronqué ...]\n\n" + tail
    sys.stdout.write(convo)


if __name__ == "__main__":
    main()
