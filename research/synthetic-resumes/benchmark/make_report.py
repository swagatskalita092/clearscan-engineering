#!/usr/bin/env python3
"""Turns benchmark/results.json into RESULTS.md. Run after run_benchmark.py."""
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "benchmark" / "results.json").read_text(encoding="utf-8"))
PARSERS = [k for k in D["versions"] if "poppler-data" not in k]
TEXT = [p for p in PARSERS if p != "Tesseract OCR"]
FILES = {f["id"][:2]: f for f in D["files"]}


def m(num, parser, metric, mode="strict"):
    return FILES[num]["parsers"][parser][mode][metric]


def fmt(x):
    return f"{x:.2f}"


def mean(parser, metric, mode="strict"):
    return st.mean(f["parsers"][parser][mode][metric] for f in D["files"])


out = []
w = out.append
n = len(D["files"])

w("# Parser benchmark: results\n")
w("*How well do common open-source PDF text extractors read the "
  f"{n} synthetic resumes in this folder? Numbers below are generated from "
  "[results.json](benchmark/results.json) by "
  "[make_report.py](benchmark/make_report.py), not typed by hand.*\n")
w("Run on 9 November 2026. Every extractor ran with default settings. "
  "None of them is a commercial applicant tracking system, so these numbers "
  "describe text extraction only.\n")
w("Eleven readers are compared. Seven are plain text extractors "
  "(pypdf, pdfminer.six, pdfplumber, pypdfium2, PyMuPDF and poppler in two "
  "modes). Three are newer layout-aware or markdown-producing tools "
  "(pypdf in layout mode, PyMuPDF4LLM and MarkItDown), included because "
  "they are what people reach for when they feed documents to a language "
  "model. The last is Tesseract OCR, which reads a picture of the page.\n")

w("## Tools and versions\n")
w("| Extractor | Version |")
w("|---|---|")
for p, v in D["versions"].items():
    w(f"| {p} | {v} |")
w("")

w("## How the newer tools were called\n")
w("- **pypdf (layout mode)** is the same library as pypdf with "
  "`extraction_mode=\"layout\"`, which places text by its position on the "
  "page instead of by its order in the file.")
w("- **PyMuPDF4LLM** converts a page to markdown using layout analysis. "
  "On pages that contain an image it runs Tesseract OCR by itself and "
  "prints a notice. In this set that happened on the scanned page (`09`) "
  "and on the three files with a picture on a text page (`17`, `19`, "
  "`27`). It writes line breaks inside table cells as `<br>`. That is "
  "markup, not a word, so the benchmark turns it into a newline before "
  "scoring. Markdown symbols such as `#`, `**` and `|` are ignored by the "
  "word splitter and cost nothing.")
w("- **MarkItDown** is a document converter that produces markdown. For "
  "PDF files it calls pdfminer.six, and pdfplumber for table-like pages. "
  "Its output is scored as it comes.\n")

w("## What is measured\n")
w("Each resume has a ground-truth file listing its words in the order a person "
  "reads them. Words are split on letters and digits and compared in lower "
  "case.\n")
w("- **Recall** is the share of ground-truth words that appear whole in the "
  "extracted text. It measures what was lost.")
w("- **Order** is the longest run of ground-truth words that appears in the "
  "same sequence in the extracted text, divided by the number of "
  "ground-truth words. It measures what was scrambled. Recall can be 1.00 "
  "while order is low.")
w("- **Noise** is the share of extracted words that are not in the "
  "ground truth (repeated page headers, broken words and so on).")
w("- **Strict** compares the extracted text as it comes. **Lenient** first "
  "applies Unicode compatibility normalisation (NFKC), which folds ligature "
  "characters and combining accents into plain letters.\n")
w("Reading order for multi-column layouts is a choice: the ground truth reads "
  "a whole column before the next. Another reader could choose differently.\n")

w("## Summary over all resumes\n")
w("| Extractor | Recall (strict) | Recall (lenient) | Order | Noise |")
w("|---|---|---|---|---|")
for p in PARSERS:
    w(f"| {p} | {fmt(mean(p,'recall'))} | {fmt(mean(p,'recall','lenient'))} | "
      f"{fmt(mean(p,'order'))} | {fmt(mean(p,'noise'))} |")
w("")
w("The averages hide the story, because most files are easy and a few traps "
  "are severe. Use the per-resume table below.\n")

w("## Per resume: recall / order (strict)\n")
w("| Resume | " + " | ".join(PARSERS) + " |")
w("|---|" + "---|" * len(PARSERS))
for f in D["files"]:
    cells = [f"{fmt(f['parsers'][p]['strict']['recall'])} / "
             f"{fmt(f['parsers'][p]['strict']['order'])}" for p in PARSERS]
    w(f"| {f['id']} | " + " | ".join(cells) + " |")
w("")

w("## What the numbers show\n")

w("**Plain layouts are solved.** On the single-column control "
  f"(`01-baseline-single-column`) every extractor reads every word "
  f"(recall {fmt(min(m('01',p,'recall') for p in PARSERS))}). Order is "
  f"{fmt(min(m('01',p,'order') for p in PARSERS))} to "
  f"{fmt(max(m('01',p,'order') for p in PARSERS))}. "
  "The traps below are where extraction differs.\n")

FILE_ORDER = ["pypdf", "pypdfium2", "PyMuPDF"]
o03 = {p: m("03", p, "order") for p in PARSERS}
o25 = {p: m("25", p, "order") for p in PARSERS}
w("**Columns decide reading order, and the winner depends on how the file "
  "was written.** In `03-two-equal-columns` the text is written to the file "
  "column by column. Extractors that follow file order score "
  f"{fmt(o03['pypdf'])} (pypdf), {fmt(o03['pypdfium2'])} (pypdfium2) and "
  f"{fmt(o03['PyMuPDF'])} (PyMuPDF), while pdfminer.six scores "
  f"{fmt(o03['pdfminer.six'])} and pdfplumber {fmt(o03['pdfplumber'])}. In "
  "`25-two-columns-written-row-by-row` the same page is written line by "
  f"line across both columns and the file-order extractors drop to "
  f"{fmt(o25['pypdf'])} each. "
  "None of the plain extractors does well on both: pdfminer.six and poppler "
  f"(default mode) stay at {fmt(o03['pdfminer.six'])} to "
  f"{fmt(o03['pdfminer.six'] if False else max(o03['pdfminer.six'], o03['poppler pdftotext']))} on "
  "both files. Tesseract OCR, which looks at the "
  f"picture, scores {fmt(o03['Tesseract OCR'])} on both. Words are never "
  "lost here, only shuffled, which is why a scanner that ignores order can "
  "look fine while a reader of the same text cannot.\n")

w("**Layout analysis helps with columns, but it is not a cure.** "
  f"PyMuPDF4LLM scores {fmt(o03['PyMuPDF4LLM'])} on `03` and "
  f"{fmt(o25['PyMuPDF4LLM'])} on `25`, the same on both because it looks at "
  f"where text sits and not at the order it was written, and "
  f"{fmt(m('02','PyMuPDF4LLM','order'))} on the sidebar layout (`02`). "
  f"Its average order is {fmt(mean('PyMuPDF4LLM','order'))}, the best of "
  "any text-based reader here "
  f"(next is {fmt(max(mean(p,'order') for p in TEXT if p != 'PyMuPDF4LLM'))}). "
  "It still fails where the layout is a table: on the Word file whose "
  f"two columns are a table (`21`) it scores {fmt(m('21','PyMuPDF4LLM','order'))}, "
  "and on the LaTeX two-column file (`23`) "
  f"{fmt(m('23','PyMuPDF4LLM','order'))}. "
  f"pypdf in layout mode scores {fmt(m('03','pypdf (layout mode)','order'))} "
  f"on `03` and `25`, because it reads straight across both columns, but "
  f"{fmt(m('12','pypdf (layout mode)','order'))} on the reversed-order page "
  f"(`12`) where default pypdf scores {fmt(m('12','pypdf','order'))}. So "
  "pypdf has two modes with opposite strengths. MarkItDown scores the same "
  "order as pdfminer.six on every file except the two LaTeX ones.\n")

assert m("03","pypdf (layout mode)","order") == m("25","pypdf (layout mode)","order")
assert m("03","PyMuPDF4LLM","order") == o25["PyMuPDF4LLM"] or abs(m("03","PyMuPDF4LLM","order") - o25["PyMuPDF4LLM"]) < 0.02
assert m("12","pypdf (layout mode)","order") == 1.0
assert all(m(k, "MarkItDown", "order") == m(k, "pdfminer.six", "order")
           for k in FILES if k not in ("22", "23"))
assert mean("PyMuPDF4LLM","order") == max(mean(p,"order") for p in TEXT)

o12 = {p: m("12", p, "order") for p in PARSERS}
w("**A page that looks right can be written in reverse.** In "
  "`12-drawing-order-reversed` the page looks normal, but the sections are "
  "written to the file bottom-up. File-order extractors score "
  f"{fmt(o12['pypdf'])} (pypdf, pypdfium2, PyMuPDF) while pdfplumber, "
  f"poppler with -layout, pypdf in layout mode, PyMuPDF4LLM and Tesseract "
  f"score {fmt(o12['pdfplumber'])}.\n")
assert all(o12[p] == 1.0 for p in ("pdfplumber", "poppler pdftotext -layout",
           "pypdf (layout mode)", "PyMuPDF4LLM", "Tesseract OCR"))

assert all(FILES["09"]["parsers"][p]["error"] in (None, "") for p in PARSERS)
assert {m("17", p, "recall") for p in TEXT if p != "PyMuPDF4LLM"} == {m("17", "pypdf", "recall")}
assert m("17", "PyMuPDF4LLM", "recall") == m("17", "Tesseract OCR", "recall") == 1.0
SCAN_ZERO = [p for p in TEXT if m("09", p, "recall") == 0]
assert len(SCAN_ZERO) == len(TEXT) - 1 and "PyMuPDF4LLM" not in SCAN_ZERO
w("**A scanned page has no text for a text extractor.** On "
  f"`09-scanned-image-only` {len(SCAN_ZERO)} of {len(TEXT)} text readers "
  "return recall 0.00. The exception is PyMuPDF4LLM, which notices the "
  "image and runs OCR itself and reaches recall "
  f"{fmt(m('09','PyMuPDF4LLM','recall'))}. Its OCR output is lower than "
  "calling Tesseract directly "
  f"({fmt(m('09','Tesseract OCR','recall'))}) because some neighbouring "
  "words come out joined without a space. The other nine return no words "
  "and raise no error, which is the more dangerous behaviour. A name that "
  "exists only as an image (`17-name-as-image`) also needs OCR: "
  f"{fmt(m('17','pypdf','recall'))} for the other text "
  f"readers, {fmt(m('17','Tesseract OCR','recall'))} for Tesseract and for "
  "PyMuPDF4LLM through its own OCR. OCR is "
  "not free of problems: on accented names it scores "
  f"{fmt(m('15','Tesseract OCR','recall'))} on "
  "`15-composed-accents`, where the text extractors score "
  f"{fmt(m('15','pypdf','recall'))}.\n")

w("**Small glyph choices cost whole words.**\n")
w(f"- Letter-spaced headings (`11`): pdfminer.six, pdfplumber, PyMuPDF, "
  f"PyMuPDF4LLM and MarkItDown reach recall "
  f"{fmt(m('11','pdfminer.six','recall'))} because heading words "
  "come out as single letters. pypdf (both modes), pypdfium2 and poppler "
  "keep them.")
assert m("11","PyMuPDF4LLM","recall") == m("11","pdfminer.six","recall")
assert m("11","pypdf (layout mode)","recall") == 1.0
w(f"- Ligature characters (`10`): pypdf, pdfminer.six, PyMuPDF, both "
  f"poppler modes, pypdf in layout mode and MarkItDown return recall "
  f"{fmt(m('10','pypdf','recall'))} under strict "
  "comparison because words such as `financial` come out with a ligature "
  "character. pdfplumber, pypdfium2 and PyMuPDF4LLM expand them and score "
  f"{fmt(m('10','pdfplumber','recall'))}.")
assert m("10","PyMuPDF4LLM","recall") == 1.0 and m("10","MarkItDown","recall") < 1.0
assert m("10","pypdf (layout mode)","recall") < 1.0
assert len({m("14", p, "recall") for p in PARSERS}) == 1
assert len({m("14", p, "recall", "lenient") for p in TEXT}) == 1
w(f"- Decomposed accents (`14`): every reader scores "
  f"{fmt(m('14','pypdf','recall'))} strict and "
  f"{fmt(m('14','pypdf','recall','lenient'))} lenient, against "
  f"{fmt(m('15','pypdf','recall'))} for the composed control (`15`). The "
  "extractors did nothing wrong. A tool that matches words without "
  "normalising Unicode will miss them.")
assert len({m("13", p, "noise") for p in PARSERS}) == 1
w(f"- Repeated page headers and footers (`13`) add noise of "
  f"{fmt(m('13','pypdf','noise'))} for every extractor.\n")

w("**Links are invisible to text extraction.** In `16-link-label-only` the "
  "web address is stored in the file as a link annotation, "
  "which the benchmark confirmed by reading the file's annotations, and it "
  f"is absent from the extracted text for all {len(PARSERS)} readers, "
  "including the markdown converters, which could have written it as a link "
  "and did not. The visible label is read; the address is not.\n")
assert not any(FILES["16"]["parsers"][p]["url_in_text"] for p in PARSERS)

assert {m("22", p, "recall") for p in TEXT if p != "pypdf (layout mode)"} <= \
    {m("22", "pypdf", "recall"), m("22", "PyMuPDF4LLM", "recall")}
assert m("22", "pypdf (layout mode)", "recall") < m("22", "pypdf", "recall")
w("**The producer matters.** The LaTeX file built with the default fonts "
  f"(`22`) loses ligature letters for every text extractor (recall "
  f"{fmt(m('22','pypdf','recall'))}), because the fonts in that build are "
  "bitmap Type 3 fonts with no text mapping. pypdf in layout mode does "
  f"worse (recall {fmt(m('22','pypdf (layout mode)','recall'))}) because "
  "it also splits ordinary words inside that font, such as `op` and "
  "`erations`. The same text with an embedded "
  f"Type 1 font and a Unicode map (`24`) scores "
  f"{fmt(m('24','pypdf','recall'))} on pypdf, but pdfplumber with default "
  f"settings reads it at {fmt(m('24','pdfplumber','recall'))}, because it "
  "joins words that the typesetter separated with narrow spaces. Changing "
  "pdfplumber's tolerance would change that number. This is a result about "
  "default settings, and a reminder that tuning matters.\n")

w("**Converters can invent structure.** MarkItDown turned the plain "
  "single-column LaTeX resume (`22`) into a markdown table and put the "
  "email address and the phone number in different cells, so the phone "
  "number no longer appears as one string. PyMuPDF4LLM did something "
  "similar to the Word file (`20`): it detected a table and split a bold "
  f"word across cells (`Ex | perience`), so recall fell to "
  f"{fmt(m('20','PyMuPDF4LLM','recall'))} on a file every plain extractor "
  f"reads at {fmt(m('20','pypdf','recall'))}. Layout analysis helps on "
  "hard pages and can hurt on easy ones.\n")
assert m("20","PyMuPDF4LLM","recall") < 1.0 and m("20","pypdf","recall") == 1.0
assert FILES["22"]["parsers"]["MarkItDown"]["contact_strict"] < 1

bad = [(FILES[k]["id"], p) for k in FILES if k != "09" for p in PARSERS
       if FILES[k]["parsers"][p]["contact_strict"] < 1]
assert sorted(set(p for _, p in bad)) == ["MarkItDown", "pdfplumber",
                                          "pypdf (layout mode)"], bad
assert sorted(i[:2] for i, p in bad if p == "pdfplumber") == ["23", "24"]
assert sorted(i[:2] for i, p in bad if p == "MarkItDown") == ["22", "23"]
assert sorted(i[:2] for i, p in bad if p == "pypdf (layout mode)") == ["22"]
assert FILES["22"]["parsers"]["pypdf (layout mode)"]["contact_lenient"] == 1
ne = [m_ for m_ in ("27", "28", "29", "30")]
short = [(k, p_) for k in ne for p_ in TEXT if m(k, p_, "recall") < 1.0]
assert short == [("29", "PyMuPDF4LLM")], short
w("**Other scripts and second-language headings are not the problem.** On "
  "`27` to `30` (a German CV with a photo, then Russian, Greek and Japanese "
  "text) every text extractor reads every word (recall 1.00), with one "
  "exception: PyMuPDF4LLM split a single Greek word in two on `29` "
  f"(recall {fmt(m('29','PyMuPDF4LLM','recall'))}). Two details "
  "matter in practice:\n")
w("- Poppler needs its separate `poppler-data` package to read the Japanese "
  "file, which uses an unembedded CID font. In an earlier run on the same "
  "machine without that package, both poppler modes returned recall 0.00 on "
  "`30` and no error. With it installed they score "
  f"{fmt(m('30','poppler pdftotext','recall'))}. The version is listed in the "
  "table above. A silent empty result is the dangerous part.")
w("- OCR needs to be told the language. It was given the right language pack "
  "for each file here, which a real pipeline would have to guess. Even then, "
  f"Greek scores {fmt(m('29','Tesseract OCR','recall'))} strict and "
  f"{fmt(m('29','Tesseract OCR','recall','lenient'))} lenient, because the "
  "OCR returns the micro sign (U+00B5) where the text has the Greek letter "
  "mu (U+03BC), so words containing mu fail an exact comparison. Unicode "
  "compatibility normalisation fixes it.\n")

w("**Contact details mostly survive.** The email address and phone number "
  "appeared intact in the extracted text for every text-layer resume and "
  "every reader except three cases. pdfplumber on `23` and `24` joined "
  "words and the phone number lost its spaces. MarkItDown on `22` and `23` "
  "split the phone number across table cells. pypdf in layout mode on `22` "
  "padded the gaps between words with runs of spaces, so an exact match "
  "fails, while a match that ignores extra whitespace passes. "
  "Tesseract and PyMuPDF4LLM kept every contact detail, including on the "
  "scanned page.\n")
assert all(FILES[k]["parsers"]["Tesseract OCR"]["contact_strict"] == 1 for k in FILES)
assert all(FILES[k]["parsers"]["PyMuPDF4LLM"]["contact_strict"] == 1 for k in FILES)

w("## Limits of this benchmark\n")
w("- The resumes are synthetic and short. Real files are messier.")
w("- Most generated files write text in reading order, which favours "
  "file-order extractors. Resumes `12`, `25` and `26` show the opposite, "
  "but the real mix of producers is unknown.")
w("- Recall and order are measured on words, not on sections or fields. "
  "They say nothing about whether a system would assign a job title to the "
  "right field.")
w("- The markdown converters are scored on words, as the others are. A "
  "pipeline that feeds markdown to a language model also depends on how "
  "well that model copes with tables and broken words, which this does not "
  "measure.")
w("- PyMuPDF4LLM was run without the optional RapidOCR package, so its OCR "
  "used Tesseract. Results with other OCR engines may differ.")
w("- These are open-source libraries on default settings. Commercial "
  "applicant tracking systems use their own parsers, and nothing here "
  "predicts what any of them does.")
w("- One run, one machine, one resume structure, mostly English text, plus "
  "one German, one Russian, one Greek and one Japanese file. Scripts that "
  "need text shaping, such as Arabic, Devanagari and Thai, are not covered "
  "because the generator cannot draw them. No statistical claims are made.")
w("- Two traps depend on the tool that produced the file (the LaTeX "
  "installation and the word processor). The PDFs are committed so results "
  "can be reproduced, but rebuilding them elsewhere may differ.\n")

w("## Reproduce\n")
w("```text\npip install -r benchmark/requirements.txt\n"
  "python generator/build.py\npython benchmark/run_benchmark.py\n"
  "python benchmark/make_report.py\n```\n")
w("Tesseract with the `deu`, `rus`, `ell` and `jpn` language packs, and "
  "poppler (`pdftotext`) with `poppler-data`, must be installed separately. "
  "LibreOffice and a LaTeX installation are needed only to rebuild resumes "
  "`20` to `24`.\n")

(ROOT / "RESULTS.md").write_text("\n".join(out), encoding="utf-8")
print("Wrote RESULTS.md")
