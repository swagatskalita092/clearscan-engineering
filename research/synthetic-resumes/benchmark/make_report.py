#!/usr/bin/env python3
"""Turns benchmark/results.json into RESULTS.md. Run after run_benchmark.py."""
import json
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "benchmark" / "results.json").read_text(encoding="utf-8"))
PARSERS = list(D["files"][0]["parsers"])
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
w("Run on 10 November 2026. Every extractor ran with default settings. "
  "None of them is a commercial applicant tracking system, so these numbers "
  "describe text extraction only.\n")
w("Eleven readers are compared. Seven are plain text extractors "
  "(pypdf, pdfminer.six, pdfplumber, pypdfium2, PyMuPDF and poppler in two "
  "modes). Three are newer layout-aware or markdown-producing tools "
  "(pypdf in layout mode, PyMuPDF4LLM and MarkItDown), included because "
  "they are what people reach for when they feed documents to a language "
  "model. The last is Tesseract OCR, which reads a picture of the page.\n")

w("## Tools and versions\n")
w("| Tool | Version |")
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
def mean_over(parser, metric, ids, mode="strict"):
    return st.mean(FILES[k]["parsers"][parser][mode][metric] for k in ids)


FIRST30 = [k for k in FILES if int(k) <= 30]
BEST_ALL = max((p for p in TEXT), key=lambda p: mean(p, "order"))
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
  f"Across the first 30 resumes its average order is "
  f"{fmt(mean_over('PyMuPDF4LLM','order',FIRST30))}, the best of the text "
  f"readers (next is {fmt(max(mean_over(p,'order',FIRST30) for p in TEXT if p != 'PyMuPDF4LLM'))}). "
  f"Across all {n} it is {fmt(mean('PyMuPDF4LLM','order'))}, behind "
  f"{BEST_ALL} at {fmt(mean(BEST_ALL,'order'))}, because of the Hindi and "
  "Thai files discussed below. "
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
assert mean_over("PyMuPDF4LLM","order",FIRST30) == max(mean_over(p,"order",FIRST30) for p in TEXT)
assert BEST_ALL != "PyMuPDF4LLM"

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
assert sorted(set(p for _, p in bad)) == ["MarkItDown", "Tesseract OCR",
                                          "pdfplumber", "pypdf (layout mode)"], bad
assert sorted(i[:2] for i, p in bad if p == "Tesseract OCR") == ["32"]
assert sorted(i[:2] for i, p in bad if p == "pdfplumber") == ["23", "24"]
assert sorted(i[:2] for i, p in bad if p == "MarkItDown") == ["22", "23"]
assert sorted(i[:2] for i, p in bad if p == "pypdf (layout mode)") == ["22"]
assert FILES["22"]["parsers"]["pypdf (layout mode)"]["contact_lenient"] == 1
ne = [m_ for m_ in ("27", "28", "29", "30")]
short = [(k, p_) for k in ne for p_ in TEXT if m(k, p_, "recall") < 1.0]
assert short == [("29", "PyMuPDF4LLM")], short
w("**Scripts that draw one glyph per letter are not the problem.** On "
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


AT = json.loads((ROOT / "benchmark" / "actualtext_check.json").read_text(encoding="utf-8"))
SHAPED_OK = ["poppler pdftotext", "PyMuPDF"]
ON_ACTUALTEXT = [p for p in TEXT if m("32", p, "recall") < 0.3 and m("33", p, "recall") < 0.5]
assert sorted(ON_ACTUALTEXT) == sorted(["pypdf", "pdfminer.six", "pdfplumber",
        "pypdf (layout mode)", "PyMuPDF4LLM", "MarkItDown"]), ON_ACTUALTEXT
assert all(m("32", p, "recall") > 0.9 for p in SHAPED_OK)
assert AT["32-devanagari-hindi"]["poppler pdftotext"]["without_actualtext"] < 0.3
assert AT["32-devanagari-hindi"]["PyMuPDF"]["without_actualtext"] < 0.3
assert AT["32-devanagari-hindi"]["pypdf"]["original"] == AT["32-devanagari-hindi"]["pypdf"]["without_actualtext"]
clean_best = max(FILES[k]["parsers"][p]["cleaned"]["recall"] for k in ("32", "33") for p in ON_ACTUALTEXT)
assert clean_best < 0.5
def rng(lo, hi):
    return fmt(lo) if fmt(lo) == fmt(hi) else f"{fmt(lo)} to {fmt(hi)}"


lo32 = min(m("32", p, "recall") for p in ON_ACTUALTEXT)
hi32 = max(m("32", p, "recall") for p in ON_ACTUALTEXT)
lo33 = min(m("33", p, "recall") for p in ON_ACTUALTEXT)
hi33 = max(m("33", p, "recall") for p in ON_ACTUALTEXT)
w("**Scripts that need shaping are the hard case, and readers fail on them "
  "differently.** `32` (Hindi) and `33` (Thai) were made by LibreOffice, "
  "which draws vowel signs and conjuncts from several glyphs and records "
  "the real text of each such cluster in a separate `/ActualText` entry "
  f"({AT['32-devanagari-hindi']['actualtext_entries']} entries in the Hindi "
  f"file, {AT['33-thai-no-spaces']['actualtext_entries']} in the Thai file). "
  f"Poppler reads Hindi at {fmt(m('32','poppler pdftotext','recall'))} and "
  f"Thai at {fmt(m('33','poppler pdftotext','recall'))}, PyMuPDF at "
  f"{fmt(m('32','PyMuPDF','recall'))} and {fmt(m('33','PyMuPDF','recall'))}. "
  "pypdf, pdfminer.six, pdfplumber, pypdf in layout mode, MarkItDown and "
  f"PyMuPDF4LLM read Hindi at {rng(lo32, hi32)} and Thai at "
  f"{rng(lo33, hi33)}. For the clusters they cannot map, pypdf writes a "
  "control character, pdfminer.six and MarkItDown write a literal `(cid:4)` "
  "marker, and PyMuPDF4LLM writes the Unicode replacement character, in the "
  "middle of the word. Vowel signs also end up on the wrong letters. "
  "Removing the control characters and `(cid:N)` markers does not repair "
  f"the words (best cleaned recall {fmt(clean_best)}), because the letters "
  "themselves are wrong, not only extra.\n")
w("To test the cause, `benchmark/check_actualtext.py` copies both files "
  "with the `/ActualText` entries emptied. Poppler's recall on Hindi falls "
  f"from {fmt(AT['32-devanagari-hindi']['poppler pdftotext']['original'])} to "
  f"{fmt(AT['32-devanagari-hindi']['poppler pdftotext']['without_actualtext'])} "
  "and PyMuPDF's from "
  f"{fmt(AT['32-devanagari-hindi']['PyMuPDF']['original'])} to "
  f"{fmt(AT['32-devanagari-hindi']['PyMuPDF']['without_actualtext'])}. "
  "pypdf, which never used the entries, does not change. Poppler and PyMuPDF "
  "do well on these two files because they read `/ActualText`; pypdfium2 "
  "was not tested this way. That describes how one producer stores shaped text. A file from another "
  "producer may be stored differently, so these numbers do not transfer to "
  "other word processors.\n")
w("OCR does not depend on how the text was stored, and reads all three new "
  f"scripts: Arabic {fmt(m('31','Tesseract OCR','recall'))}, Hindi "
  f"{fmt(m('32','Tesseract OCR','recall'))} and Thai "
  f"{fmt(m('33','Tesseract OCR','recall'))} strict "
  f"({fmt(m('33','Tesseract OCR','recall','lenient'))} lenient for Thai, "
  "because Unicode normalisation treats a combined vowel character and its "
  "two-part form as the same letters: the page has the single character "
  "U+0E33 and OCR returns the two characters U+0E4D U+0E32). On every one "
  "of the three it is below the best text reader, and far above the text "
  "readers that fail.\n")
assert all(m(k, "Tesseract OCR", "recall") < max(m(k, p, "recall") for p in TEXT)
           for k in ("31", "32", "33"))

ARAB_OK = ["pypdf", "PyMuPDF", "poppler pdftotext", "PyMuPDF4LLM"]
ARAB_REV = ["pdfminer.six", "pdfplumber", "pypdf (layout mode)", "MarkItDown"]
assert all(m("31", p, "recall") > 0.9 and m("31", p, "order") > 0.9 for p in ARAB_OK)
assert all(m("31", p, "recall") < 0.2 for p in ARAB_REV)
assert m("31", "pypdfium2", "recall") > 0.9 and m("31", "pypdfium2", "order") < 0.5
glued = sorted(p for p in PARSERS if not FILES["31"]["parsers"][p]["email_standalone"])
assert glued == sorted(["pypdf", "PyMuPDF", "poppler pdftotext",
                        "poppler pdftotext -layout", "PyMuPDF4LLM"]), glued
assert all(FILES["31"]["parsers"][p]["contact_strict"] == 1 for p in PARSERS)
w("**Right-to-left text separates logical order from visual order.** In "
  "`31` (Arabic, with an English email address and a phone number inside "
  "the right-to-left line) pypdf, PyMuPDF, poppler and PyMuPDF4LLM keep the "
  f"words whole and in order (recall {fmt(min(m('31',p,'recall') for p in ARAB_OK))} "
  f"to {fmt(max(m('31',p,'recall') for p in ARAB_OK))}). pypdfium2 keeps the "
  "words but returns each line in visual order, so its recall is "
  f"{fmt(m('31','pypdfium2','recall'))} and its order "
  f"{fmt(m('31','pypdfium2','order'))}. pdfminer.six, pdfplumber, pypdf in "
  "layout mode and MarkItDown return each word with its letters reversed, "
  f"so recall is {fmt(m('31','pdfminer.six','recall'))}. The email address "
  "and phone number stay intact as strings for every reader, but in five "
  "of them the address is glued to what comes before it: to the Arabic "
  "city name in pypdf, PyMuPDF and PyMuPDF4LLM, and to an invisible "
  "direction character in both poppler modes. A pattern that looks for an "
  "email address after a space can miss it or capture the extra character. "
  "Poppler also wraps lines and Latin runs in invisible direction "
  "characters throughout the Arabic text.\n")

w("**Contact details mostly survive.** The email address and phone number "
  "appeared intact in the extracted text for every text-layer resume and "
  "every reader except four cases. pdfplumber on `23` and `24` joined "
  "words and the phone number lost its spaces. MarkItDown on `22` and `23` "
  "split the phone number across table cells. pypdf in layout mode on `22` "
  "padded the gaps between words with runs of spaces, so an exact match "
  "fails, while a match that ignores extra whitespace passes. "
  "Tesseract misread the phone number on the Hindi file (`32`) and returned "
  "`00` where the page has `010`, which is an ordinary OCR error and shows "
  "why contact details deserve a check against the source. PyMuPDF4LLM kept "
  "every contact detail, including on the scanned page.\n")
assert all(FILES[k]["parsers"]["PyMuPDF4LLM"]["contact_strict"] == 1 for k in FILES)

w("## Limits of this benchmark\n")
w("- The resumes are synthetic and short. Real files are messier.")
w("- Most generated files write text in reading order, which favours "
  "file-order extractors. Resumes `12`, `25` and `26` show the opposite, "
  "but the real mix of producers is unknown.")
w("- Thai has no spaces between words, so the word splitter returns whole "
  "phrases as single tokens. One wrong character then loses the whole "
  "phrase, and the Thai scores are stricter than the others for that reason.")
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
  "one file each in German, Russian, Greek, Japanese, Arabic, Hindi and Thai. "
  "The Arabic, Hindi and Thai files come from a single producer "
  "(LibreOffice, version above) and show how it stores shaped text, not how "
  "every word processor does. Right-to-left layouts with columns or tables, "
  "Eastern Arabic digits, and date conventions are not scored, although the "
  "Thai file uses Buddhist Era years. No statistical claims are made.")
w("- Two traps depend on the tool that produced the file (the LaTeX "
  "installation and the word processor). The PDFs are committed so results "
  "can be reproduced, but rebuilding them elsewhere may differ.\n")

w("## Reproduce\n")
w("```text\npip install -r benchmark/requirements.txt\n"
  "python generator/build.py\npython benchmark/run_benchmark.py\n"
  "python benchmark/make_report.py\n```\n")
w("Tesseract with the `deu`, `rus`, `ell`, `jpn`, `ara`, `hin` and `tha` "
  "language packs, and poppler (`pdftotext`) with `poppler-data`, must be "
  "installed separately. LibreOffice and a LaTeX installation are needed "
  "only to rebuild resumes `20` to `24` and `31` to `33`. The test of the "
  "`/ActualText` explanation is `python benchmark/check_actualtext.py`.\n")

(ROOT / "RESULTS.md").write_text("\n".join(out), encoding="utf-8")
print("Wrote RESULTS.md")
