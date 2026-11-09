#!/usr/bin/env python3
"""Builds a static, searchable website from the Markdown in this repository.

Run from anywhere:  python3 scripts/build_site.py
Output goes to _site/ (ignored by git). Needs the "markdown" package.

The site makes no requests to other domains: no web fonts, no analytics, no
badges. Search runs in the browser against search-index.json.
After building, the script checks that every internal link and image in the
generated pages points at a file that exists, and fails if one does not.
"""
import html
import json
import os
import posixpath
import re
import shutil
import sys
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SRC = Path(__file__).resolve().parent / "site"

REPO_URL = "https://github.com/swagatskalita092/clearscan-engineering"
SITE_URL = "https://swagatskalita092.github.io/clearscan-engineering/"
SITE_PATH = "/" + SITE_URL.split("/", 3)[3]
SITE_NAME = "ClearScan engineering notes"

SKIP_DIRS = {".git", ".github", "node_modules", "_site", "__pycache__", ".snap_tmp"}
COPY_SUFFIXES = {".png", ".svg", ".jpg", ".jpeg", ".gif", ".webp", ".pdf"}
GROUPS = [
    ("Start", lambda r: r in ("README.md", "docs/README.md")),
    ("The notes", lambda r: r.startswith("docs/")),
    ("Incidents", lambda r: r.startswith("incidents/")),
    ("Build your own", lambda r: r.startswith("build-your-own/")),
    ("Research", lambda r: r.startswith("research/")),
    ("Project", lambda r: True),
]


def slugify(value, separator="-"):
    value = re.sub(r"<[^>]+>", "", value).lower().strip()
    value = re.sub(r"[^\w\- ]", "", value)
    return value.replace(" ", separator)


def drop_number_tables(fragment):
    """Tables that are mostly figures add noise to search results."""
    def keep(m):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", m.group(0), flags=re.S)
        numeric = [c for c in cells if re.fullmatch(r"[\d./\s-]*", strip_tags(c))]
        return "" if cells and len(numeric) / len(cells) > 0.5 else m.group(0)
    return re.sub(r"<table>.*?</table>", keep, fragment, flags=re.S)


def strip_tags(fragment):
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def out_path(rel):
    """Markdown path (posix, relative to the repo) -> output path."""
    p = posixpath.dirname(rel)
    name = posixpath.basename(rel)
    new = "index.html" if name == "README.md" else name[:-3] + ".html"
    return posixpath.join(p, new) if p else new


class Page:
    def __init__(self, rel, text):
        self.rel = rel
        self.text = text
        self.out = out_path(rel)
        m = re.search(r"^#\s+(.+?)\s*$", text, re.M)
        self.h1 = m.group(1) if m else rel
        self.title = SITE_NAME if rel == "README.md" else self.h1
        self.nav_title = "Home" if rel == "README.md" else self.h1
        self.description = describe(text)
        self.body = ""
        self.generated = False


def describe(text):
    after = re.split(r"^#\s+.+$", text, maxsplit=1, flags=re.M)
    body = after[-1] if len(after) > 1 else text
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or block.startswith(("#", "<", "|", ">", "```", "!", "[!")):
            continue
        plain = re.sub(r"[*_`]", "", re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", block))
        plain = re.sub(r"\s+", " ", plain)
        if len(plain) > 200:
            plain = plain[:200].rsplit(" ", 1)[0] + "..."
        return plain
    return SITE_NAME


def collect_pages():
    pages = {}
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        pages[rel] = Page(rel, path.read_text(encoding="utf-8"))
    return pages


def add_directory_indexes(pages):
    """A folder of pages with no README gets a generated list page."""
    by_dir = {}
    for rel, page in pages.items():
        by_dir.setdefault(posixpath.dirname(rel), []).append(page)
    for folder, members in sorted(by_dir.items()):
        if not folder or any(posixpath.basename(m.rel) == "README.md" for m in members):
            continue
        title = folder.replace("-", " ").capitalize()
        lines = [f"# {title}", ""]
        for m in sorted(members, key=lambda p: p.rel):
            lines.append(f"- [{m.h1}]({posixpath.basename(m.rel)}): {m.description}")
        rel = posixpath.join(folder, "README.md")
        page = Page(rel, "\n".join(lines) + "\n")
        page.generated = True
        page.nav_title = "All " + folder.replace("-", " ")
        pages[rel] = page


def rel_url(from_out, to_out):
    start = posixpath.dirname(from_out) or "."
    return posixpath.relpath(to_out, start)


class Site:
    def __init__(self):
        self.pages = collect_pages()
        add_directory_indexes(self.pages)
        self.copied = set()
        self.md = markdown.Markdown(
            extensions=["tables", "fenced_code", "sane_lists", "md_in_html", "toc"],
            extension_configs={"toc": {
                "slugify": slugify, "permalink": "#",
                "permalink_class": "anchor",
                "permalink_title": "Link to this section"}},
            output_format="html",
        )

    # ---------- links ----------
    def rewrite_target(self, url, page):
        if re.match(r"^([a-z][a-z0-9+.-]*:|#|//)", url, re.I):
            return url
        path, sep, frag = url.partition("#")
        path = path.split("?")[0]
        if not path:
            return url
        target = (ROOT / posixpath.dirname(page.rel) / path).resolve()
        try:
            rel = target.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return url
        if rel == ".":
            rel = ""
        suffix = ("#" + frag) if sep else ""
        if target.is_dir():
            readme = posixpath.join(rel, "README.md") if rel else "README.md"
            if readme in self.pages:
                return rel_url(page.out, self.pages[readme].out) + suffix
            return f"{REPO_URL}/tree/main/{rel}"
        if rel in self.pages:
            return rel_url(page.out, self.pages[rel].out) + suffix
        if target.is_file():
            if target.suffix.lower() in COPY_SUFFIXES:
                self.copied.add(rel)
                return rel_url(page.out, rel) + suffix
            return f"{REPO_URL}/blob/main/{rel}"
        return url

    def rewrite_html(self, body, page):
        def sub(m):
            return f'{m.group(1)}="{self.rewrite_target(html.unescape(m.group(2)), page)}"'
        return re.sub(r'\b(href|src)="([^"]*)"', sub, body)

    # ---------- rendering ----------
    def render(self, page):
        text = page.text
        text = text.replace('<div align="center">', '<div align="center" markdown="1">')
        text = text.replace("<details>", '<details markdown="1">')
        self.md.reset()
        body = self.md.convert(text)
        # Mermaid source is not drawn on the site; the SVG diagram above it is.
        body = re.sub(r"<details[^>]*>(?:(?!</details>).)*?language-mermaid.*?</details>",
                      "", body, flags=re.S)
        # Any Mermaid block left (GitHub draws it, this site does not) becomes
        # the system overview image that the architecture page also uses.
        diagram = posixpath.relpath("assets/diagrams/architecture-overview.svg",
                                    posixpath.dirname(page.rel) or ".")
        body = re.sub(
            r'<pre><code class="language-mermaid">.*?</code></pre>',
            '<p class="diagram"><img src="%s" alt="System overview: a user reaches a '
            'browser app, which calls an API and signs in directly with the '
            'authentication service. The API reads and writes the database and calls '
            'a language model provider and an email provider." width="100%%"></p>' % diagram,
            body, flags=re.S)
        # Badges would call another domain on every visit.
        body = re.sub(r'<a [^>]*>\s*<img [^>]*shields\.io[^>]*>\s*</a>', "", body)
        body = re.sub(r'<img [^>]*shields\.io[^>]*>', "", body)
        body = re.sub(r"<p>\s*(?:<br\s*/?>\s*)*</p>", "", body)
        body = re.sub(
            r"<blockquote>\s*<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*",
            lambda m: ('<blockquote class="callout callout-%s"><p><strong class="callout-title">'
                       '%s</strong><br>' % (m.group(1).lower(), m.group(1).capitalize())),
            body)
        body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
        body = body.replace("</table>", "</table></div>")
        body = self.rewrite_html(body, page)
        page.body = body

    def nav_html(self, current):
        groups = {name: [] for name, _ in GROUPS}
        for rel, page in sorted(self.pages.items(), key=lambda kv: (kv[0] != "README.md", kv[0])):
            for name, test in GROUPS:
                if test(rel):
                    groups[name].append(page)
                    break
        for name in groups:
            groups[name].sort(key=lambda p: (posixpath.basename(p.rel) != "README.md"
                                              and not p.generated, p.rel))
        parts = []
        for name, members in groups.items():
            if not members:
                continue
            items = []
            for p in members:
                cur = ' aria-current="page"' if p.rel == current.rel else ""
                items.append('<li><a href="%s"%s>%s</a></li>' % (
                    html.escape(rel_url(current.out, p.out)), cur, html.escape(p.nav_title)))
            parts.append('<h2 class="nav-group">%s</h2><ul>%s</ul>' % (name, "".join(items)))
        return "".join(parts)

    def write_page(self, page, template, root, nav, edit_rel=None, canonical=None):
        edit = ""
        if edit_rel and not page.generated:
            edit = ('<a href="%s/edit/main/%s">Suggest a change to this page on GitHub</a>'
                    % (REPO_URL, edit_rel))
        values = dict(
            title=html.escape(page.title if page.rel == "README.md" else
                              "%s | %s" % (page.title, SITE_NAME)),
            description=html.escape(page.description, quote=True),
            root=root, nav=nav, content=page.body, edit=edit,
            canonical=canonical or SITE_URL + page.out.replace("index.html", ""),
            og_image=SITE_URL + "assets/banner.png",
        )
        return template.substitute(values)

    # ---------- search index ----------
    def chunks(self, page):
        title, url = page.title, page.out
        pattern = re.compile(r'<h([1-3]) id="([^"]+)">(.*?)</h\1>', re.S)
        marks = list(pattern.finditer(page.body))
        rows = []
        intro_end = marks[0].start() if marks else len(page.body)
        intro = strip_tags(drop_number_tables(page.body[:intro_end]))
        if intro:
            rows.append({"t": title, "h": "", "u": url, "x": intro})
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(page.body)
            heading = strip_tags(re.sub(r'<a class="anchor".*?</a>', "", m.group(3)))
            text = strip_tags(drop_number_tables(page.body[m.end():end]))
            if heading == title and not text:
                continue
            rows.append({"t": title, "h": heading, "u": "%s#%s" % (url, m.group(2)),
                         "x": text})
        return rows

    # ---------- build ----------
    def build(self):
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir()
        static = OUT / "_static"
        static.mkdir()
        for name in ("site.css", "site.js"):
            shutil.copy(SRC / name, static / name)
        shutil.copy(ROOT / "assets" / "brand" / "clearscan-logo.png", static / "logo.png")
        (OUT / ".nojekyll").write_text("", encoding="utf-8")
        template = Template((SRC / "page.html").read_text(encoding="utf-8"))

        index_rows = []
        for rel, page in self.pages.items():
            self.render(page)
        for rel, page in self.pages.items():
            root = posixpath.relpath(".", posixpath.dirname(page.out) or ".")
            root = "./" if root == "." else root + "/"
            doc = self.write_page(page, template, root, self.nav_html(page), rel)
            target = OUT / page.out
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(doc, encoding="utf-8")
            index_rows.extend(self.chunks(page))

        for rel in sorted(self.copied | {"assets/banner.png"}):
            dest = OUT / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, dest)

        (OUT / "search-index.json").write_text(
            json.dumps(index_rows, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8")

        missing = Page("404", "# Page not found\n\nThat page does not exist. Try the search box, "
                       "or start from the [home page](index.html).\n")
        missing.out = "404.html"
        missing.generated = True
        self.render(missing)
        missing.body = missing.body.replace('href="index.html"', 'href="%s"' % SITE_PATH)
        (OUT / "404.html").write_text(
            self.write_page(missing, template, SITE_PATH, self.nav_html(missing)),
            encoding="utf-8")

        urls = [SITE_URL + p.out.replace("index.html", "") for p in self.pages.values()]
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join("  <url><loc>%s</loc></url>\n" % u for u in sorted(urls))
            + "</urlset>\n", encoding="utf-8")
        (OUT / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % SITE_URL, encoding="utf-8")
        return len(self.pages), len(index_rows)


def check_output():
    """Every relative href and src in the built pages must exist."""
    problems = []
    for page in OUT.rglob("*.html"):
        if page.name == "404.html":
            continue
        text = page.read_text(encoding="utf-8")
        for target in re.findall(r'\b(?:href|src)="([^"]+)"', text):
            if re.match(r"^([a-z][a-z0-9+.-]*:|#|//|/)", target, re.I):
                continue
            clean = target.split("#")[0].split("?")[0]
            if clean and not (page.parent / clean).exists():
                problems.append("%s: missing %s" % (page.relative_to(OUT), target))
    return problems


def main():
    pages, chunks = Site().build()
    problems = check_output()
    print("Built %d pages and %d search entries into %s" % (pages, chunks, OUT))
    if problems:
        print("Site check failed:")
        for p in problems:
            print("  " + p)
        return 1
    print("Site check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
