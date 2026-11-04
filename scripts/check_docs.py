#!/usr/bin/env python3
"""Checks documentation hygiene.

Fails if a Markdown file has a broken relative link, uses CR line endings, or
looks like it contains a secret. Standard library only, so it keeps working
without installing anything.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules"}

SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9]+"),
    re.compile(r"whsec_[A-Za-z0-9]+"),
    re.compile(r"cs_live_[A-Za-z0-9]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

LINK_PATTERNS = [
    re.compile(r"\]\(([^)\s]+)"),
    re.compile(r'(?:src|href)="([^"]+)"'),
]


def markdown_files():
    for path in ROOT.rglob("*.md"):
        if not any(part in SKIP_DIRS for part in path.parts):
            yield path


def strip_code_fences(text):
    kept = []
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            kept.append(line)
    return "\n".join(kept)


def check():
    problems = []
    for path in markdown_files():
        rel = path.relative_to(ROOT)
        raw = path.read_bytes()
        if b"\r" in raw:
            problems.append(f"{rel}: contains CR characters, use LF line endings")
        text = raw.decode("utf-8", errors="replace")

        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                problems.append(f"{rel}: looks like it contains a secret")

        body = strip_code_fences(text)
        for pattern in LINK_PATTERNS:
            for target in pattern.findall(body):
                if target.startswith(("http://", "https://", "mailto:", "#", "data:")):
                    continue
                clean = target.split("#")[0].split("?")[0]
                if not clean:
                    continue
                if not (path.parent / clean).resolve().exists():
                    problems.append(f"{rel}: broken link {target}")
    return problems


def main():
    problems = check()
    if problems:
        print("Documentation check failed:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("Documentation check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
