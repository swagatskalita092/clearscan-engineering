#!/usr/bin/env python3
"""Builds the synthetic resume set.

Usage: python generator/build.py            (from research/synthetic-resumes)

Writes resumes/*.pdf, truth/*.json and manifest.json. Everything is invented.
Needs: reportlab, pillow, pypdfium2, numpy, python-docx; LibreOffice (soffice)
and pdflatex for the word-processor and LaTeX variants.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from content import (P1, P2, P3, P4, P5, P6, P7, P8, P9,  # noqa: E402
                     DEFAULT_HEADINGS, contact_line)
import layouts as L  # noqa: E402

OUT = ROOT / "resumes"
TRUTH = ROOT / "truth"

SPECS = []  # (id, title, trap, producer, note, builder)


def spec(id_, title, trap, producer, builder, persona=P1, note=""):
    SPECS.append(dict(id=id_, title=title, trap=trap, producer=producer,
                      builder=builder, persona=persona, note=note))


# ---- reportlab layouts
spec("01-baseline-single-column", "Baseline, single column",
     "Control: a plain one-column resume.", "reportlab", lambda: L.single())
spec("02-sidebar-two-column", "Left sidebar plus main column",
     "Reading order across a shaded sidebar and a main column.", "reportlab",
     lambda: L.sidebar())
spec("03-two-equal-columns", "Two equal body columns",
     "Reading order across two text columns of the same width.", "reportlab",
     lambda: L.two_column_body())
spec("04-skills-grid-table", "Skills in a bordered grid",
     "Short items laid out in table cells.", "reportlab",
     lambda: L.single(grid=True))
spec("05-experience-date-column", "Dates in a left table column",
     "Table where dates sit beside the description.", "reportlab",
     lambda: L.experience_table())
spec("06-contact-in-footer", "Contact details in the page footer",
     "Contact details placed away from the top of the page.", "reportlab",
     lambda: L.single(contact_footer=True))
spec("07-icon-glyphs-contact", "Icon glyphs before contact items",
     "Symbol characters used as icons.", "reportlab",
     lambda: L.single(icons=True, font="DejaVu"))
spec("08-symbol-bullets", "Arrow glyph bullets",
     "Non-standard bullet characters.", "reportlab",
     lambda: L.single(bullet=("\u27a4", "DejaVu")))
spec("10-ligature-glyphs", "Ligature characters in words",
     "Letters such as fi and fl stored as single ligature characters.",
     "reportlab", lambda: L.single(lig=True, font="DejaVu", bold="DejaVu-Bold"))
spec("11-letter-spaced-headings", "Letter-spaced section headings",
     "Headings drawn with wide character spacing.", "reportlab",
     lambda: L.single(head_style="spaced"))
spec("12-drawing-order-reversed", "Drawing order differs from reading order",
     "Sections written to the file bottom-up; the page looks normal.",
     "reportlab", lambda: L.single(group_order=[4, 3, 2, 1, 0]))
spec("13-repeated-page-furniture", "Two pages with repeated header and footer",
     "Text that repeats on every page and is not content.", "reportlab",
     lambda: L.single(furniture=True, size=17, leading=36))
spec("14-decomposed-accents", "Accented names, decomposed form",
     "Letters stored as a base letter plus a combining mark.", "reportlab",
     lambda: L.single(p=P2, nfd=True, font="DejaVu", bold="DejaVu-Bold"),
     persona=P2)
spec("15-composed-accents", "Accented names, composed form",
     "Control for 14: the same text with single-character accents.",
     "reportlab",
     lambda: L.single(p=P2, font="DejaVu", bold="DejaVu-Bold"), persona=P2)
spec("16-link-label-only", "Link visible as a label only",
     "The address lives in a link annotation, not in the page text.",
     "reportlab", lambda: L.single(link=True))
spec("17-name-as-image", "Name rendered as an image",
     "A name that exists only as pixels.", "reportlab",
     lambda: L.single(name_img=True))
spec("18-dot-leader-dates", "Dot leaders between title and dates",
     "Rows of dots used as a visual tab.", "reportlab",
     lambda: L.single(leader=True))
spec("19-photo-and-sidebar", "Portrait photo above a sidebar",
     "A picture at the top of a two-column layout.", "reportlab",
     lambda: L.sidebar(photo=True))


spec("25-two-columns-written-row-by-row", "Two body columns written row by row",
     "Text written to the file line by line across both columns.",
     "reportlab", lambda: L.two_column_body(rows=True))
spec("26-sidebar-written-row-by-row", "Sidebar layout written row by row",
     "Text written to the file line by line across sidebar and main column.",
     "reportlab", lambda: L.sidebar(rows=True))


spec("27-german-cv-with-photo", "German-language CV with photo",
     "Second-language headings, umlauts, month/year dates and a portrait.",
     "reportlab", lambda: L.single(p=P3, photo=True), persona=P3)
spec("28-cyrillic-text", "Cyrillic script",
     "A resume written entirely in Russian.", "reportlab",
     lambda: L.single(p=P4, font="DejaVu", bold="DejaVu-Bold"), persona=P4)
spec("29-greek-text", "Greek script",
     "A resume written entirely in Greek.", "reportlab",
     lambda: L.single(p=P5, font="DejaVu", bold="DejaVu-Bold"), persona=P5)
spec("30-japanese-cid-font", "Japanese with a CID font",
     "Japanese text in an unembedded CID font, with no spaces between words.",
     "reportlab",
     lambda: L.single(p=P6, font="HeiseiKakuGo-W5", bold="HeiseiKakuGo-W5"),
     persona=P6)


SCRIPT_FILES = [
    ("31-arabic-right-to-left", "Arabic, right to left",
     "Right-to-left Arabic in a word-processor export, with a Latin email "
     "address and a phone number inside the right-to-left line.", P7),
    ("32-devanagari-hindi", "Hindi in Devanagari",
     "Devanagari text: vowel signs and conjuncts drawn from several code "
     "points, as a font and shaping engine produce them.", P8),
    ("33-thai-no-spaces", "Thai",
     "Thai text: no spaces between words, stacked vowel and tone marks, "
     "and years in the Buddhist Era.", P9),
]


def build_reportlab(s):
    r, order = s["builder"]()
    path = OUT / f"{s['id']}.pdf"
    r.save(path, group_order=order)
    return r, path


def page_count(path):
    import pypdfium2 as pdfium
    return len(pdfium.PdfDocument(str(path)))


# ---- scanned variant (image only)
def build_scanned():
    import io
    import numpy as np
    import pypdfium2 as pdfium
    from PIL import Image
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas

    base, _ = L.single()
    tmp = Path(tempfile.mkdtemp()) / "base.pdf"
    base.save(tmp)
    page = pdfium.PdfDocument(str(tmp))[0]
    img = page.render(scale=200 / 72).to_pil().convert("L")
    img = img.rotate(0.6, resample=Image.BICUBIC, fillcolor=255)
    arr = np.asarray(img, dtype=np.float32)
    rng = np.random.default_rng(7)
    arr = np.clip(arr + rng.normal(0, 6, arr.shape), 0, 255).astype("uint8")
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, "JPEG", quality=70)
    path = OUT / "09-scanned-image-only.pdf"
    c = canvas.Canvas(str(path), pagesize=A4, invariant=1)
    c.drawImage(ImageReader(io.BytesIO(buf.getvalue())), 0, 0, *A4)
    c.showPage()
    c.save()
    return base.truth, path


# ---- word processor and LaTeX variants
def unit_truth(p, order):
    out = []
    hd = p.get("headings", DEFAULT_HEADINGS)
    for u in order:
        if u == "header":
            out += [p["name"], p["title"], contact_line(p)]
        elif u == "summary":
            out += [hd["summary"], p["summary"]]
        elif u == "experience":
            out.append(hd["experience"])
            for e in p["experience"]:
                out += [e["role"], e["dates"], e["org"]] + e["bullets"]
        elif u == "education":
            out.append(hd["education"])
            e = p["education"][0]
            out += [e["degree"], e["dates"], e["school"]]
        elif u == "skills":
            out += [hd["skills"], p.get("skill_sep", ", ").join(p["skills"])]
    return out


def soffice(docx, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(outdir), str(docx)],
                   check=True, capture_output=True, timeout=180)


def _tabbed(para, width_cm):
    import docx
    import docx.enum.text
    para.paragraph_format.tab_stops.add_tab_stop(
        docx.shared.Cm(width_cm), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT)


def _docx_blocks(doc_or_cell, p, units, tabw=17.2):
    for u in units:
        if u == "header":
            para = doc_or_cell.add_paragraph()
            run = para.add_run(p["name"])
            run.bold = True
            run.font.size = __import__("docx").shared.Pt(22)
            doc_or_cell.add_paragraph(p["title"])
            doc_or_cell.add_paragraph(contact_line(p))
        elif u == "summary":
            h = doc_or_cell.add_paragraph()
            h.add_run("Summary").bold = True
            doc_or_cell.add_paragraph(p["summary"])
        elif u == "experience":
            h = doc_or_cell.add_paragraph()
            h.add_run("Experience").bold = True
            for e in p["experience"]:
                para = doc_or_cell.add_paragraph()
                para.add_run(e["role"]).bold = True
                if tabw > 10:
                    _tabbed(para, tabw)
                    para.add_run("\t" + e["dates"])
                else:
                    doc_or_cell.add_paragraph(e["dates"])
                doc_or_cell.add_paragraph(e["org"])
                for b in e["bullets"]:
                    doc_or_cell.add_paragraph(b, style="List Bullet")
        elif u == "education":
            h = doc_or_cell.add_paragraph()
            h.add_run("Education").bold = True
            e = p["education"][0]
            para = doc_or_cell.add_paragraph()
            para.add_run(e["degree"]).bold = True
            if tabw > 10:
                _tabbed(para, tabw)
                para.add_run("\t" + e["dates"])
            else:
                doc_or_cell.add_paragraph(e["dates"])
            doc_or_cell.add_paragraph(e["school"])
        elif u == "skills":
            h = doc_or_cell.add_paragraph()
            h.add_run("Skills").bold = True
            doc_or_cell.add_paragraph(", ".join(p["skills"]))


def build_docx(table):
    import docx
    import docx.enum.text
    p = P1
    d = docx.Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = docx.shared.Cm(1.8)
    sec.top_margin = sec.bottom_margin = docx.shared.Cm(1.6)
    if table:
        _docx_blocks(d, p, ["header"])
        t = d.add_table(rows=1, cols=2)
        _docx_blocks(t.rows[0].cells[0], p, ["experience"], 7.6)
        _docx_blocks(t.rows[0].cells[1], p, ["summary", "education", "skills"], 7.6)
        order = ["header", "experience", "summary", "education", "skills"]
        name = "21-docx-table-two-column"
    else:
        _docx_blocks(d, p, ["header", "summary", "experience", "education",
                            "skills"])
        order = ["header", "summary", "experience", "education", "skills"]
        name = "20-docx-baseline"
    tmpd = Path(tempfile.mkdtemp())
    src = tmpd / f"{name}.docx"
    d.save(src)
    soffice(src, tmpd)
    shutil.copy(tmpd / f"{name}.pdf", OUT / f"{name}.pdf")
    return unit_truth(p, order), OUT / f"{name}.pdf"


def _script_run(run, p, bold=False, size=None):
    """Font, complex-script and right-to-left settings for one run."""
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    rpr = run._r.get_or_add_rPr()
    fonts = OxmlElement("w:rFonts")
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), p["font"])
    rpr.insert(0, fonts)
    if bold:
        rpr.append(OxmlElement("w:b"))
        rpr.append(OxmlElement("w:bCs"))
    if size:
        for tag in ("w:sz", "w:szCs"):
            el = OxmlElement(tag)
            el.set(qn("w:val"), str(size * 2))
            rpr.append(el)
    if p.get("rtl"):
        rpr.append(OxmlElement("w:rtl"))
    lang = OxmlElement("w:lang")
    lang.set(qn("w:bidi"), p["lang"])
    rpr.append(lang)


def build_docx_script(p, name):
    """One-column Word file in a script that needs text shaping."""
    import docx
    from docx.oxml import OxmlElement
    d = docx.Document()
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = docx.shared.Cm(1.8)
    sec.top_margin = sec.bottom_margin = docx.shared.Cm(1.6)
    hd = p.get("headings", DEFAULT_HEADINGS)

    def add(text, bold=False, size=None, style=None):
        para = d.add_paragraph(style=style) if style else d.add_paragraph()
        if p.get("rtl"):
            ppr = para._p.get_or_add_pPr()
            ppr.insert(1 if ppr.find(docx.oxml.ns.qn("w:pStyle")) is not None else 0,
                       OxmlElement("w:bidi"))
        _script_run(para.add_run(text), p, bold, size)

    add(p["name"], True, 22)
    add(p["title"])
    add(contact_line(p))
    add(hd["summary"], True)
    add(p["summary"])
    add(hd["experience"], True)
    for e in p["experience"]:
        add(e["role"], True)
        add(e["dates"])
        add(e["org"])
        for b in e["bullets"]:
            add(b, style="List Bullet")
    add(hd["education"], True)
    e = p["education"][0]
    add(e["degree"], True)
    add(e["dates"])
    add(e["school"])
    add(hd["skills"], True)
    add(p.get("skill_sep", ", ").join(p["skills"]))
    tmpd = Path(tempfile.mkdtemp())
    src = tmpd / f"{name}.docx"
    d.save(src)
    soffice(src, tmpd)
    shutil.copy(tmpd / f"{name}.pdf", OUT / f"{name}.pdf")
    order = ["header", "summary", "experience", "education", "skills"]
    return unit_truth(p, order), OUT / f"{name}.pdf"


LATEX = r"""\documentclass[10pt,a4paper]{article}
\usepackage[margin=1.8cm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{multicol}
\usepackage{enumitem}
%%PREAMBLE%%
\pagestyle{empty}
\begin{document}
\begin{center}{\LARGE\bfseries NAME}\\[2pt] TITLE\\[2pt] CONTACT\end{center}
%%OPEN%%
\section*{Summary}
SUMMARY
\section*{Experience}
EXPERIENCE
\section*{Education}
EDUCATION
\section*{Skills}
SKILLS
%%CLOSE%%
\end{document}
"""


def build_latex(multi, fix):
    p = P1
    exp = ""
    for e in p["experience"]:
        exp += "\\noindent\\textbf{%s} \\hfill %s\\\\\n%s\n\\begin{itemize}[nosep]\n" % (
            e["role"], e["dates"], e["org"])
        for b in e["bullets"]:
            exp += "\\item %s\n" % b
        exp += "\\end{itemize}\n"
    e = p["education"][0]
    edu = "\\noindent\\textbf{%s} \\hfill %s\\\\\n%s\n" % (
        e["degree"], e["dates"], e["school"])
    tex = (LATEX.replace("NAME", p["name"]).replace("TITLE", p["title"])
           .replace("CONTACT", contact_line(p).replace("|", "$|$"))
           .replace("SUMMARY", p["summary"]).replace("EXPERIENCE", exp)
           .replace("EDUCATION", edu).replace("SKILLS", ", ".join(p["skills"])))
    pre = ""
    if fix:
        pre += "\\usepackage{times}\n\\input{glyphtounicode}\n\\pdfgentounicode=1\n"
    pre += "\\hyphenpenalty=10000 \\exhyphenpenalty=10000\n"
    tex = tex.replace("%%PREAMBLE%%", pre)
    tex = tex.replace("%%OPEN%%", "\\begin{multicols}{2}" if multi else "")
    tex = tex.replace("%%CLOSE%%", "\\end{multicols}" if multi else "")
    name = ("23-latex-two-column" if multi else
            "24-latex-single-column-unicode-map" if fix else
            "22-latex-single-column")
    tmpd = Path(tempfile.mkdtemp())
    (tmpd / f"{name}.tex").write_text(tex, encoding="utf-8")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", f"{name}.tex"],
                   cwd=tmpd, check=True, capture_output=True, timeout=120)
    shutil.copy(tmpd / f"{name}.pdf", OUT / f"{name}.pdf")
    order = ["header", "summary", "experience", "education", "skills"]
    return unit_truth(p, order), OUT / f"{name}.pdf"


def main():
    OUT.mkdir(exist_ok=True)
    TRUTH.mkdir(exist_ok=True)
    manifest = []
    # --only 31 32 ...  builds just those files and keeps the rest untouched.
    only = tuple(a for a in sys.argv[1:] if a != "--only")
    wanted = (lambda i: i.startswith(only)) if only else (lambda i: True)

    def record(id_, title, trap, producer, truth, path, persona, links=()):
        em, ph = persona["email"], persona["phone"]
        data = dict(id=id_, file=f"resumes/{id_}.pdf", title=title, trap=trap,
                    producer=producer, pages=page_count(path),
                    ocr_lang=persona.get("ocr_lang", "eng"),
                    reading_order=truth,
                    contact_checks={"email": em, "phone": ph},
                    link_targets=list(links))
        (TRUTH / f"{id_}.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
        manifest.append(dict(id=id_, title=title, trap=trap, producer=producer,
                             pages=data["pages"]))

    for s in SPECS:
        if not wanted(s["id"]):
            continue
        r, path = build_reportlab(s)
        links = [u for (_, _, u) in r.links]
        record(s["id"], s["title"], s["trap"], s["producer"], r.truth, path,
               s["persona"], links)

    if not only:
        main_rest(record)
    for sid, title, trap, persona in SCRIPT_FILES:
        if wanted(sid):
            t, path = build_docx_script(persona, sid)
            record(sid, title, trap, "python-docx + LibreOffice", t, path, persona)
    finish(manifest, bool(only))


def main_rest(record):
    t, path = build_scanned()
    record("09-scanned-image-only", "Scanned page, no text layer",
           "A page that is only a picture of text.", "reportlab (raster)", t,
           path, P1)
    t, path = build_docx(False)
    record("20-docx-baseline", "Word-processor export, single column",
           "Control from a different producer.", "python-docx + LibreOffice",
           t, path, P1)
    t, path = build_docx(True)
    record("21-docx-table-two-column", "Word-processor export, table columns",
           "Two columns made with a borderless table.",
           "python-docx + LibreOffice", t, path, P1)
    t, path = build_latex(False, False)
    record("22-latex-single-column", "LaTeX export, default fonts",
           "Bitmap Type 3 fonts with no text mapping: ligature letters are "
           "lost (depends on the TeX Live installation).", "pdflatex", t,
           path, P1)
    t, path = build_latex(True, True)
    record("23-latex-two-column", "LaTeX export, text flows in two columns",
           "Running text that wraps from one column to the next "
           "(Type 1 font, Unicode map).", "pdflatex", t, path, P1)
    t, path = build_latex(False, True)
    record("24-latex-single-column-unicode-map",
           "LaTeX export, Type 1 font and Unicode map",
           "Control for 22: the same text with an embedded Type 1 font and "
           "a Unicode map.",
           "pdflatex", t, path, P1)


def finish(manifest, merge):
    path = ROOT / "manifest.json"
    if merge and path.exists():
        keep = {m["id"]: m for m in json.loads(path.read_text(encoding="utf-8"))}
        keep.update({m["id"]: m for m in manifest})
        manifest = list(keep.values())
    manifest.sort(key=lambda m: m["id"])
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    print(f"Manifest lists {len(manifest)} resumes.")


if __name__ == "__main__":
    main()
