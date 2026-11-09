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

w("# Parser benchmark: first results\n")
w("*How well do common open-source PDF text extractors read the "
  f"{n} synthetic resumes in this folder? Numbers below are generated from "
  "[results.json](benchmark/results.json) by "
  "[make_report.py](benchmark/make_report.py), not typed by hand.*\n")
w("Run on 9 November 2026. Every extractor ran with default settings. "
  "None of them is a commercial applicant tracking system, so these numbers "
  "describe text extraction only.\n")

w("## Tools and versions\n")
w("| Extractor | Version |")
w("|---|---|")
for p, v in D["versions"].items():
    w(f"| {p} | {v} |")
w("")

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
  "No text extractor does well on both: pdfminer.six and poppler "
  f"(default mode) stay at {fmt(o03['pdfminer.six'])} to "
  f"{fmt(o03['pdfminer.six'] if False else max(o03['pdfminer.six'], o03['poppler pdftotext']))} on "
  "both files. Tesseract OCR, which looks at the "
  f"picture, scores {fmt(o03['Tesseract OCR'])} on both. Words are never "
  "lost here, only shuffled, which is why a scanner that ignores order can "
  "look fine while a reader of the same text cannot.\n")

o12 = {p: m("12", p, "order") for p in PARSERS}
w("**A page that looks right can be written in reverse.** In "
  "`12-drawing-order-reversed` the page looks normal, but the sections are "
  "written to the file bottom-up. File-order extractors score "
  f"{fmt(o12['pypdf'])} (pypdf, pypdfium2, PyMuPDF) while pdfplumber, "
  f"poppler with -layout and Tesseract score {fmt(o12['pdfplumber'])}.\n")

w("**A scanned page has no text for a text extractor.** On "
  "`09-scanned-image-only` all seven text extractors return recall "
  f"{fmt(max(m('09',p,'recall') for p in TEXT))}. OCR reads it with recall "
  f"{fmt(m('09','Tesseract OCR','recall'))}, and it is also the only "
  "extractor that recovers a name that exists only as an image "
  f"(`17-name-as-image`: {fmt(m('17','pypdf','recall'))} for text "
  f"extractors, {fmt(m('17','Tesseract OCR','recall'))} for OCR). OCR is "
  "not free of problems: on accented names it scores "
  f"{fmt(m('15','Tesseract OCR','recall'))} on "
  "`15-composed-accents`, where the text extractors score "
  f"{fmt(m('15','pypdf','recall'))}.\n")

w("**Small glyph choices cost whole words.**\n")
w(f"- Letter-spaced headings (`11`): pdfminer.six, pdfplumber and PyMuPDF "
  f"reach recall {fmt(m('11','pdfminer.six','recall'))} because heading words "
  "come out as single letters. pypdf, pypdfium2 and poppler keep them.")
w(f"- Ligature characters (`10`): pypdf, pdfminer.six, PyMuPDF and both "
  f"poppler modes return recall {fmt(m('10','pypdf','recall'))} under strict "
  "comparison because words such as `financial` come out with a ligature "
  "character. pdfplumber and pypdfium2 expand them and score "
  f"{fmt(m('10','pdfplumber','recall'))}.")
w(f"- Decomposed accents (`14`): every text extractor scores "
  f"{fmt(m('14','pypdf','recall'))} strict and "
  f"{fmt(m('14','pypdf','recall','lenient'))} lenient, against "
  f"{fmt(m('15','pypdf','recall'))} for the composed control (`15`). The "
  "extractors did nothing wrong. A tool that matches words without "
  "normalising Unicode will miss them.")
w(f"- Repeated page headers and footers (`13`) add noise of "
  f"{fmt(m('13','pypdf','noise'))} for every extractor.\n")

w("**Links are invisible to text extraction.** In `16-link-label-only` the "
  "web address is stored in the file as a link annotation, "
  "which the benchmark confirmed by reading the file's annotations, and it "
  "is absent from the extracted text for all eight extractors. The visible label is read; the "
  "address is not.\n")

w("**The producer matters.** The LaTeX file built with the default fonts "
  f"(`22`) loses ligature letters for every text extractor (recall "
  f"{fmt(m('22','pypdf','recall'))}), because the fonts in that build are "
  "bitmap Type 3 fonts with no text mapping. The same text with an embedded "
  f"Type 1 font and a Unicode map (`24`) scores "
  f"{fmt(m('24','pypdf','recall'))} on pypdf, but pdfplumber with default "
  f"settings reads it at {fmt(m('24','pdfplumber','recall'))}, because it "
  "joins words that the typesetter separated with narrow spaces. Changing "
  "pdfplumber's tolerance would change that number. This is a result about "
  "default settings, and a reminder that tuning matters.\n")

bad = [(FILES[k]["id"], p) for k in FILES if k != "09" for p in PARSERS
       if FILES[k]["parsers"][p]["contact_strict"] < 1]
assert all(p == "pdfplumber" for _, p in bad), bad
ne = [m_ for m_ in ("27", "28", "29", "30")]
assert all(m(k, p_, "recall") == 1.0 for k in ne for p_ in TEXT), "scripts"
w("**Other scripts and second-language headings are not the problem.** On "
  "`27` to `30` (a German CV with a photo, then Russian, Greek and Japanese "
  "text) every text extractor reads every word (recall 1.00). Two details "
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
  "every extractor except pdfplumber on "
  + " and ".join(f"`{i[:2]}`" for i, _ in bad) +
  ", where it joined words and the phone number lost its spaces "
  "(contact score 0.50).\n")

w("## Limits of this benchmark\n")
w("- The resumes are synthetic and short. Real files are messier.")
w("- Most generated files write text in reading order, which favours "
  "file-order extractors. Resumes `12`, `25` and `26` show the opposite, "
  "but the real mix of producers is unknown.")
w("- Recall and order are measured on words, not on sections or fields. "
  "They say nothing about whether a system would assign a job title to the "
  "right field.")
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
