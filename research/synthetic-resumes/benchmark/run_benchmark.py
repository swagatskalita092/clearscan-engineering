#!/usr/bin/env python3
"""Runs open-source text extractors over the synthetic resumes and scores them.

Usage: python benchmark/run_benchmark.py     (from research/synthetic-resumes)

Writes benchmark/results.json and RESULTS.md. Read RESULTS.md for how each
number is defined.
"""
import io
import json
import re
import subprocess
import sys
import tempfile
import unicodedata
from collections import Counter
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CJK = "\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff"
# Each Japanese or Chinese character is one token, because those scripts have
# no spaces between words. Everything else is split on letters and digits.
TOKEN = re.compile(f"[{CJK}]|[^\\W{CJK}]+", re.UNICODE)


# ------------------------------------------------------------------ parsers
def p_pypdf(path):
    from pypdf import PdfReader
    return "\n".join((pg.extract_text() or "") for pg in PdfReader(str(path)).pages)


def p_pdfminer(path):
    from pdfminer.high_level import extract_text
    return extract_text(str(path))


def p_pdfplumber(path):
    import pdfplumber
    with pdfplumber.open(str(path)) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def p_pypdfium2(path):
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(str(path))
    return "\n".join(pg.get_textpage().get_text_range() for pg in pdf)


def p_pymupdf(path):
    import pymupdf
    with pymupdf.open(str(path)) as doc:
        return "\n".join(pg.get_text() for pg in doc)


def p_poppler(path):
    return subprocess.run(["pdftotext", str(path), "-"], capture_output=True,
                          text=True, check=True).stdout


def p_poppler_layout(path):
    return subprocess.run(["pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True, check=True).stdout


def p_ocr(path, lang="eng"):
    import pypdfium2 as pdfium
    out = []
    pdf = pdfium.PdfDocument(str(path))
    for pg in pdf:
        img = pg.render(scale=300 / 72).to_pil().convert("L")
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "p.png"
            img.save(f)
            res = subprocess.run(["tesseract", str(f), "-", "-l",
                                  lang if lang == "eng" else f"{lang}+eng"],
                                 capture_output=True, text=True)
            out.append(res.stdout)
    return "\n".join(out)


PARSERS = [
    ("pypdf", "pypdf", p_pypdf),
    ("pdfminer.six", "pdfminer.six", p_pdfminer),
    ("pdfplumber", "pdfplumber", p_pdfplumber),
    ("pypdfium2", "pypdfium2", p_pypdfium2),
    ("PyMuPDF", "pymupdf", p_pymupdf),
    ("poppler pdftotext", None, p_poppler),
    ("poppler pdftotext -layout", None, p_poppler_layout),
    ("Tesseract OCR", None, p_ocr),
]


def version_of(dist):
    if dist is None:
        return ""
    try:
        return metadata.version(dist)
    except metadata.PackageNotFoundError:
        return ""


def tool_versions():
    v = {}
    for name, dist, _ in PARSERS:
        v[name] = version_of(dist)
    pop = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    v["poppler pdftotext"] = v["poppler pdftotext -layout"] = (
        (pop.stderr or pop.stdout).strip().splitlines()[0])
    pd = subprocess.run(["dpkg-query", "-W", "-f=${Version}", "poppler-data"],
                        capture_output=True, text=True)
    if pd.returncode == 0:
        v["poppler-data (CMaps, used by poppler)"] = pd.stdout.strip()
    tes = subprocess.run(["tesseract", "--version"], capture_output=True,
                         text=True)
    v["Tesseract OCR"] = (tes.stdout or tes.stderr).strip().splitlines()[0]
    return v


# ------------------------------------------------------------------ metrics
def tokens(s, lenient):
    if lenient:
        s = unicodedata.normalize("NFKC", s)
    return TOKEN.findall(s.lower())


def lcs_len(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def score(truth_lines, extracted, lenient):
    truth = tokens(" ".join(truth_lines), lenient)
    ext = tokens(extracted, lenient)
    if not truth:
        return dict(recall=0.0, order=0.0, noise=0.0)
    ct, ce = Counter(truth), Counter(ext)
    matched = sum(min(ct[k], ce[k]) for k in ct)
    recall = matched / len(truth)
    order = lcs_len(truth, ext) / len(truth)
    noise = 1 - matched / len(ext) if ext else 0.0
    return dict(recall=round(recall, 4), order=round(order, 4),
                noise=round(noise, 4))


def contact(truth_json, extracted, lenient):
    hit = 0
    for v in truth_json["contact_checks"].values():
        text = extracted
        if lenient:
            text = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text))
        hit += v in text
    return hit / len(truth_json["contact_checks"])


def annotation_urls(path):
    from pypdf import PdfReader
    urls = set()
    for pg in PdfReader(str(path)).pages:
        for a in pg.get("/Annots") or []:
            a = a.get_object()
            act = a.get("/A")
            if act and "/URI" in act.get_object():
                urls.add(str(act.get_object()["/URI"]))
    return urls


def main():
    files = sorted((ROOT / "truth").glob("*.json"))
    versions = tool_versions()
    results = []
    for tf in files:
        t = json.loads(tf.read_text(encoding="utf-8"))
        path = ROOT / t["file"]
        row = dict(id=t["id"], title=t["title"], producer=t["producer"],
                   pages=t["pages"], parsers={},
                   url_in_file_annotation=(
                       all(u in annotation_urls(path) for u in t["link_targets"])
                       if t["link_targets"] else None))
        for name, _, fn in PARSERS:
            try:
                text = (fn(path, t.get("ocr_lang", "eng"))
                        if fn is p_ocr else fn(path))
                err = None
            except Exception as e:  # a parser crash is a result too
                text, err = "", str(e)[:120]
            strict = score(t["reading_order"], text, False)
            lenient = score(t["reading_order"], text, True)
            row["parsers"][name] = dict(
                strict=strict, lenient=lenient,
                contact_strict=contact(t, text, False),
                contact_lenient=contact(t, text, True),
                url_in_text=any(u in text for u in t["link_targets"])
                if t["link_targets"] else None,
                chars=len(text), error=err)
        results.append(row)
        print("scored", t["id"], file=sys.stderr)
    out = dict(versions=versions, files=results)
    (ROOT / "benchmark" / "results.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Wrote benchmark/results.json")


if __name__ == "__main__":
    main()
