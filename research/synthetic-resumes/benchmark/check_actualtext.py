#!/usr/bin/env python3
"""Tests one explanation for the Hindi and Thai results.

LibreOffice writes an /ActualText entry for every cluster of shaped glyphs.
This script copies resumes 32 and 33 with those entries emptied, then reads
both the original and the copy with poppler and with pypdf, and writes the
recall to benchmark/actualtext_check.json. If a reader depends on the
entries, its recall falls on the copy.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import run_benchmark as rb  # noqa: E402

from pypdf import PdfReader, PdfWriter  # noqa: E402
from pypdf.generic import ContentStream, NameObject  # noqa: E402

FILES = ["32-devanagari-hindi", "33-thai-no-spaces"]


def strip_actualtext(src, dst):
    reader = PdfReader(str(src))
    writer = PdfWriter()
    for page in reader.pages:
        data = page.get_contents().get_data()
        new = re.sub(rb"/ActualText\s*<[0-9A-Fa-f]*>", b"/ActualText<>", data)
        stream = ContentStream(None, reader)
        stream.set_data(new)
        page[NameObject("/Contents")] = writer._add_object(stream)
        writer.add_page(page)
    with open(dst, "wb") as fh:
        writer.write(fh)


def main():
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        for name in FILES:
            t = json.loads((ROOT / "truth" / f"{name}.json").read_text(encoding="utf-8"))
            copy = Path(tmp) / f"{name}.pdf"
            strip_actualtext(ROOT / t["file"], copy)
            data = b"".join(pg.get_contents().get_data()
                            for pg in PdfReader(str(ROOT / t["file"])).pages)
            row = {"actualtext_entries": data.count(b"/ActualText")}
            for label, fn in (("poppler pdftotext", rb.p_poppler),
                              ("PyMuPDF", rb.p_pymupdf), ("pypdf", rb.p_pypdf)):
                row[label] = dict(
                    original=rb.score(t["reading_order"], fn(ROOT / t["file"]), False)["recall"],
                    without_actualtext=rb.score(t["reading_order"], fn(copy), False)["recall"])
            out[name] = row
    (HERE / "actualtext_check.json").write_text(
        json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
