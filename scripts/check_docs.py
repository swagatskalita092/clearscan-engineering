#!/usr/bin/env python3
"""Checks documentation hygiene and house rules.

Fails if a Markdown file has a broken relative link, uses CR line endings,
looks like it contains a secret, or breaks a house rule: no em dashes, no
currency amounts, no billing or pricing wording, no first person in the notes,
and no numbers in the prose of the scoring and anti-gaming pages. Standard
library only, so it keeps working without installing anything.
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

EM_DASH = "\u2014"
CURRENCY = re.compile(r"[\u20ac$\u00a3]\s?\d|\d\s?(?:EUR|USD|GBP|euros?|dollars?|pounds?)\b", re.I)
BILLING_WORDS = re.compile(r"\b(pricing|subscriptions?|subscribers?|billing|paid tier|paid plan)\b", re.I)
FIRST_PERSON = re.compile(r"\b(I|I'm|I've|I'll|my|mine|myself)\b")
NO_NUMBER_PAGES = {"docs/03-scoring-philosophy.md", "docs/04-anti-gaming.md"}
FIRST_PERSON_SCOPE = ("README.md", "docs/", "incidents/", "build-your-own/")
HOUSE_RULES_SKIP = {"CODE_OF_CONDUCT.md", "CHANGELOG.md", "LICENSE"}

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


def prose_only(text):
    """Text with code fences, inline code, link targets and quoted strings removed."""
    body = strip_code_fences(text)
    body = re.sub(r"`[^`]*`", "", body)
    body = re.sub(r"\]\([^)]*\)", "]", body)
    body = re.sub(r'(?:src|href)="[^"]*"', "", body)
    body = re.sub(r'"[^"]*"', "", body)
    return body


def house_rules(rel, text):
    problems = []
    name = rel.as_posix()
    if name in HOUSE_RULES_SKIP:
        return problems
    body = prose_only(text)
    if EM_DASH in text:
        problems.append(f"{name}: contains an em dash")
    if CURRENCY.search(text):
        problems.append(f"{name}: contains a currency amount")
    if BILLING_WORDS.search(body):
        problems.append(f"{name}: uses billing or pricing wording")
    if name.startswith(FIRST_PERSON_SCOPE) or name == "README.md":
        if FIRST_PERSON.search(body):
            problems.append(f"{name}: uses first person")
    if name in NO_NUMBER_PAGES:
        if re.search(r"\d", body):
            problems.append(f"{name}: contains digits in prose; keep this page free of figures")
    return problems


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

        problems.extend(house_rules(rel, text))

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
