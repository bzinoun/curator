#!/usr/bin/env python3
"""Mechanical redaction pass. Reads text on stdin, writes redacted text on stdout.

Applies the alias replacements from config/redaction.json, then scans for
forbidden patterns (secrets, internal paths, client emails). Exit codes:
  0 = clean, 3 = forbidden pattern found even after replacement (route to review).
"""
import json
import os
import re
import sys

CFG = os.path.join(os.path.dirname(__file__), "..", "config", "redaction.json")


def main():
    with open(CFG, encoding="utf-8") as f:
        cfg = json.load(f)
    text = sys.stdin.read()
    # forbidden patterns FIRST: alias replacement must not mangle a secret/path/email
    # into a form the patterns no longer match
    dirty = False
    for pat in cfg.get("forbidden_patterns", []):
        if re.search(pat, text):
            text = re.sub(pat, "[REDACTED]", text)
            dirty = True
    for src, dst in cfg.get("replacements", {}).items():
        text = re.sub(re.escape(src), dst, text, flags=re.IGNORECASE)
    sys.stdout.write(text)
    sys.exit(3 if dirty else 0)


if __name__ == "__main__":
    main()
