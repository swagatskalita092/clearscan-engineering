# Parser benchmark: results

*How well do common open-source PDF text extractors read the 30 synthetic resumes in this folder? Numbers below are generated from [results.json](benchmark/results.json) by [make_report.py](benchmark/make_report.py), not typed by hand.*

Run on 9 November 2026. Every extractor ran with default settings. None of them is a commercial applicant tracking system, so these numbers describe text extraction only.

Eleven readers are compared. Seven are plain text extractors (pypdf, pdfminer.six, pdfplumber, pypdfium2, PyMuPDF and poppler in two modes). Three are newer layout-aware or markdown-producing tools (pypdf in layout mode, PyMuPDF4LLM and MarkItDown), included because they are what people reach for when they feed documents to a language model. The last is Tesseract OCR, which reads a picture of the page.

## Tools and versions

| Extractor | Version |
|---|---|
| pypdf | 6.17.0 |
| pdfminer.six | 20260107 |
| pdfplumber | 0.11.10 |
| pypdfium2 | 5.13.0 |
| PyMuPDF | 2.1 |
| poppler pdftotext | pdftotext version 24.02.0 |
| poppler pdftotext -layout | pdftotext version 24.02.0 |
| pypdf (layout mode) | 6.17.0 |
| PyMuPDF4LLM | 2.1 |
| MarkItDown | 0.1.7 |
| Tesseract OCR | tesseract 5.3.4 |
| poppler-data (CMaps, used by poppler) | 0.4.12-1 |

## How the newer tools were called

- **pypdf (layout mode)** is the same library as pypdf with `extraction_mode="layout"`, which places text by its position on the page instead of by its order in the file.
- **PyMuPDF4LLM** converts a page to markdown using layout analysis. On pages that contain an image it runs Tesseract OCR by itself and prints a notice. In this set that happened on the scanned page (`09`) and on the three files with a picture on a text page (`17`, `19`, `27`). It writes line breaks inside table cells as `<br>`. That is markup, not a word, so the benchmark turns it into a newline before scoring. Markdown symbols such as `#`, `**` and `|` are ignored by the word splitter and cost nothing.
- **MarkItDown** is a document converter that produces markdown. For PDF files it calls pdfminer.six, and pdfplumber for table-like pages. Its output is scored as it comes.

## What is measured

Each resume has a ground-truth file listing its words in the order a person reads them. Words are split on letters and digits and compared in lower case.

- **Recall** is the share of ground-truth words that appear whole in the extracted text. It measures what was lost.
- **Order** is the longest run of ground-truth words that appears in the same sequence in the extracted text, divided by the number of ground-truth words. It measures what was scrambled. Recall can be 1.00 while order is low.
- **Noise** is the share of extracted words that are not in the ground truth (repeated page headers, broken words and so on).
- **Strict** compares the extracted text as it comes. **Lenient** first applies Unicode compatibility normalisation (NFKC), which folds ligature characters and combining accents into plain letters.

Reading order for multi-column layouts is a choice: the ground truth reads a whole column before the next. Another reader could choose differently.

## Summary over all resumes

| Extractor | Recall (strict) | Recall (lenient) | Order | Noise |
|---|---|---|---|---|
| pypdf | 0.96 | 0.96 | 0.92 | 0.01 |
| pdfminer.six | 0.96 | 0.96 | 0.86 | 0.02 |
| pdfplumber | 0.93 | 0.93 | 0.86 | 0.04 |
| pypdfium2 | 0.96 | 0.96 | 0.93 | 0.01 |
| PyMuPDF | 0.96 | 0.96 | 0.92 | 0.02 |
| poppler pdftotext | 0.96 | 0.96 | 0.88 | 0.01 |
| poppler pdftotext -layout | 0.96 | 0.96 | 0.89 | 0.01 |
| pypdf (layout mode) | 0.96 | 0.96 | 0.89 | 0.02 |
| PyMuPDF4LLM | 0.99 | 0.99 | 0.95 | 0.03 |
| MarkItDown | 0.95 | 0.95 | 0.86 | 0.03 |
| Tesseract OCR | 0.99 | 0.99 | 0.98 | 0.02 |

The averages hide the story, because most files are easy and a few traps are severe. Use the per-resume table below.

## Per resume: recall / order (strict)

| Resume | pypdf | pdfminer.six | pdfplumber | pypdfium2 | PyMuPDF | poppler pdftotext | poppler pdftotext -layout | pypdf (layout mode) | PyMuPDF4LLM | MarkItDown | Tesseract OCR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-baseline-single-column | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 02-sidebar-two-column | 1.00 / 1.00 | 1.00 / 0.93 | 1.00 / 0.78 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.82 | 1.00 / 0.78 | 1.00 / 0.78 | 1.00 / 0.96 | 1.00 / 0.93 | 1.00 / 0.96 |
| 03-two-equal-columns | 1.00 / 1.00 | 1.00 / 0.72 | 1.00 / 0.65 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.74 | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.95 | 1.00 / 0.72 | 1.00 / 0.96 |
| 04-skills-grid-table | 1.00 / 1.00 | 1.00 / 0.93 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.93 | 1.00 / 1.00 |
| 05-experience-date-column | 1.00 / 1.00 | 1.00 / 0.98 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.98 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.98 | 1.00 / 0.99 |
| 06-contact-in-footer | 1.00 / 0.91 | 1.00 / 0.86 | 1.00 / 0.91 | 1.00 / 0.91 | 1.00 / 0.91 | 1.00 / 0.86 | 1.00 / 0.91 | 1.00 / 0.91 | 1.00 / 0.91 | 1.00 / 0.86 | 1.00 / 0.91 |
| 07-icon-glyphs-contact | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 08-symbol-bullets | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 09-scanned-image-only | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 | 0.88 / 0.88 | 0.00 / 0.00 | 1.00 / 1.00 |
| 10-ligature-glyphs | 0.96 / 0.96 | 0.96 / 0.91 | 1.00 / 1.00 | 1.00 / 1.00 | 0.96 / 0.96 | 0.96 / 0.93 | 0.96 / 0.96 | 0.96 / 0.96 | 1.00 / 1.00 | 0.96 / 0.91 | 1.00 / 1.00 |
| 11-letter-spaced-headings | 1.00 / 1.00 | 0.96 / 0.91 | 0.96 / 0.96 | 1.00 / 1.00 | 0.96 / 0.96 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 0.96 / 0.96 | 0.96 / 0.91 | 1.00 / 1.00 |
| 12-drawing-order-reversed | 1.00 / 0.54 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 0.54 | 1.00 / 0.54 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 13-repeated-page-furniture | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 |
| 14-decomposed-accents | 0.93 / 0.93 | 0.93 / 0.84 | 0.93 / 0.93 | 0.93 / 0.93 | 0.93 / 0.93 | 0.93 / 0.88 | 0.93 / 0.93 | 0.93 / 0.93 | 0.93 / 0.93 | 0.93 / 0.84 | 0.93 / 0.93 |
| 15-composed-accents | 1.00 / 1.00 | 1.00 / 0.90 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.94 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.91 | 1.00 / 0.90 | 0.93 / 0.93 |
| 16-link-label-only | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 17-name-as-image | 0.98 / 0.98 | 0.98 / 0.93 | 0.98 / 0.98 | 0.98 / 0.98 | 0.98 / 0.98 | 0.98 / 0.93 | 0.98 / 0.98 | 0.98 / 0.98 | 1.00 / 1.00 | 0.98 / 0.93 | 1.00 / 1.00 |
| 18-dot-leader-dates | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 |
| 19-photo-and-sidebar | 1.00 / 1.00 | 1.00 / 0.67 | 1.00 / 0.70 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.82 | 1.00 / 0.70 | 1.00 / 0.70 | 1.00 / 0.85 | 1.00 / 0.67 | 1.00 / 0.96 |
| 20-docx-baseline | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 0.93 / 0.93 | 1.00 / 0.96 | 1.00 / 1.00 |
| 21-docx-table-two-column | 1.00 / 1.00 | 1.00 / 0.75 | 1.00 / 0.65 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.84 | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.69 | 1.00 / 0.75 | 1.00 / 1.00 |
| 22-latex-single-column | 0.96 / 0.96 | 0.96 / 0.91 | 0.96 / 0.96 | 0.96 / 0.96 | 0.96 / 0.96 | 0.96 / 0.91 | 0.96 / 0.96 | 0.86 / 0.86 | 0.96 / 0.95 | 0.96 / 0.96 | 1.00 / 1.00 |
| 23-latex-two-column | 1.00 / 1.00 | 1.00 / 0.74 | 0.70 / 0.49 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.82 | 1.00 / 0.72 | 0.98 / 0.71 | 1.00 / 0.76 | 0.70 / 0.49 | 0.99 / 0.98 |
| 24-latex-single-column-unicode-map | 1.00 / 1.00 | 1.00 / 0.95 | 0.24 / 0.24 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 |
| 25-two-columns-written-row-by-row | 1.00 / 0.65 | 1.00 / 0.72 | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.74 | 1.00 / 0.65 | 1.00 / 0.65 | 1.00 / 0.95 | 1.00 / 0.72 | 1.00 / 0.96 |
| 26-sidebar-written-row-by-row | 1.00 / 0.78 | 1.00 / 0.93 | 1.00 / 0.78 | 1.00 / 0.78 | 1.00 / 0.78 | 1.00 / 0.82 | 1.00 / 0.78 | 1.00 / 0.78 | 1.00 / 0.96 | 1.00 / 0.93 | 1.00 / 0.96 |
| 27-german-cv-with-photo | 1.00 / 1.00 | 1.00 / 0.90 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.91 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.99 | 1.00 / 0.90 | 0.99 / 0.99 |
| 28-cyrillic-text | 1.00 / 1.00 | 1.00 / 0.93 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.98 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.93 | 1.00 / 1.00 |
| 29-greek-text | 1.00 / 1.00 | 1.00 / 0.95 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 0.99 / 0.99 | 1.00 / 0.95 | 0.90 / 0.90 |
| 30-japanese-cid-font | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | 1.00 / 0.96 | 1.00 / 0.93 |

## What the numbers show

**Plain layouts are solved.** On the single-column control (`01-baseline-single-column`) every extractor reads every word (recall 1.00). Order is 0.95 to 1.00. The traps below are where extraction differs.

**Columns decide reading order, and the winner depends on how the file was written.** In `03-two-equal-columns` the text is written to the file column by column. Extractors that follow file order score 1.00 (pypdf), 1.00 (pypdfium2) and 1.00 (PyMuPDF), while pdfminer.six scores 0.72 and pdfplumber 0.65. In `25-two-columns-written-row-by-row` the same page is written line by line across both columns and the file-order extractors drop to 0.65 each. None of the plain extractors does well on both: pdfminer.six and poppler (default mode) stay at 0.72 to 0.74 on both files. Tesseract OCR, which looks at the picture, scores 0.96 on both. Words are never lost here, only shuffled, which is why a scanner that ignores order can look fine while a reader of the same text cannot.

**Layout analysis helps with columns, but it is not a cure.** PyMuPDF4LLM scores 0.95 on `03` and 0.95 on `25`, the same on both because it looks at where text sits and not at the order it was written, and 0.96 on the sidebar layout (`02`). Its average order is 0.95, the best of any text-based reader here (next is 0.93). It still fails where the layout is a table: on the Word file whose two columns are a table (`21`) it scores 0.69, and on the LaTeX two-column file (`23`) 0.76. pypdf in layout mode scores 0.65 on `03` and `25`, because it reads straight across both columns, but 1.00 on the reversed-order page (`12`) where default pypdf scores 0.54. So pypdf has two modes with opposite strengths. MarkItDown scores the same order as pdfminer.six on every file except the two LaTeX ones.

**A page that looks right can be written in reverse.** In `12-drawing-order-reversed` the page looks normal, but the sections are written to the file bottom-up. File-order extractors score 0.54 (pypdf, pypdfium2, PyMuPDF) while pdfplumber, poppler with -layout, pypdf in layout mode, PyMuPDF4LLM and Tesseract score 1.00.

**A scanned page has no text for a text extractor.** On `09-scanned-image-only` 9 of 10 text readers return recall 0.00. The exception is PyMuPDF4LLM, which notices the image and runs OCR itself and reaches recall 0.88. Its OCR output is lower than calling Tesseract directly (1.00) because some neighbouring words come out joined without a space. The other nine return no words and raise no error, which is the more dangerous behaviour. A name that exists only as an image (`17-name-as-image`) also needs OCR: 0.98 for the other text readers, 1.00 for Tesseract and for PyMuPDF4LLM through its own OCR. OCR is not free of problems: on accented names it scores 0.93 on `15-composed-accents`, where the text extractors score 1.00.

**Small glyph choices cost whole words.**

- Letter-spaced headings (`11`): pdfminer.six, pdfplumber, PyMuPDF, PyMuPDF4LLM and MarkItDown reach recall 0.96 because heading words come out as single letters. pypdf (both modes), pypdfium2 and poppler keep them.
- Ligature characters (`10`): pypdf, pdfminer.six, PyMuPDF, both poppler modes, pypdf in layout mode and MarkItDown return recall 0.96 under strict comparison because words such as `financial` come out with a ligature character. pdfplumber, pypdfium2 and PyMuPDF4LLM expand them and score 1.00.
- Decomposed accents (`14`): every reader scores 0.93 strict and 1.00 lenient, against 1.00 for the composed control (`15`). The extractors did nothing wrong. A tool that matches words without normalising Unicode will miss them.
- Repeated page headers and footers (`13`) add noise of 0.10 for every extractor.

**Links are invisible to text extraction.** In `16-link-label-only` the web address is stored in the file as a link annotation, which the benchmark confirmed by reading the file's annotations, and it is absent from the extracted text for all 11 readers, including the markdown converters, which could have written it as a link and did not. The visible label is read; the address is not.

**The producer matters.** The LaTeX file built with the default fonts (`22`) loses ligature letters for every text extractor (recall 0.96), because the fonts in that build are bitmap Type 3 fonts with no text mapping. pypdf in layout mode does worse (recall 0.86) because it also splits ordinary words inside that font, such as `op` and `erations`. The same text with an embedded Type 1 font and a Unicode map (`24`) scores 1.00 on pypdf, but pdfplumber with default settings reads it at 0.24, because it joins words that the typesetter separated with narrow spaces. Changing pdfplumber's tolerance would change that number. This is a result about default settings, and a reminder that tuning matters.

**Converters can invent structure.** MarkItDown turned the plain single-column LaTeX resume (`22`) into a markdown table and put the email address and the phone number in different cells, so the phone number no longer appears as one string. PyMuPDF4LLM did something similar to the Word file (`20`): it detected a table and split a bold word across cells (`Ex | perience`), so recall fell to 0.93 on a file every plain extractor reads at 1.00. Layout analysis helps on hard pages and can hurt on easy ones.

**Other scripts and second-language headings are not the problem.** On `27` to `30` (a German CV with a photo, then Russian, Greek and Japanese text) every text extractor reads every word (recall 1.00), with one exception: PyMuPDF4LLM split a single Greek word in two on `29` (recall 0.99). Two details matter in practice:

- Poppler needs its separate `poppler-data` package to read the Japanese file, which uses an unembedded CID font. In an earlier run on the same machine without that package, both poppler modes returned recall 0.00 on `30` and no error. With it installed they score 1.00. The version is listed in the table above. A silent empty result is the dangerous part.
- OCR needs to be told the language. It was given the right language pack for each file here, which a real pipeline would have to guess. Even then, Greek scores 0.90 strict and 1.00 lenient, because the OCR returns the micro sign (U+00B5) where the text has the Greek letter mu (U+03BC), so words containing mu fail an exact comparison. Unicode compatibility normalisation fixes it.

**Contact details mostly survive.** The email address and phone number appeared intact in the extracted text for every text-layer resume and every reader except three cases. pdfplumber on `23` and `24` joined words and the phone number lost its spaces. MarkItDown on `22` and `23` split the phone number across table cells. pypdf in layout mode on `22` padded the gaps between words with runs of spaces, so an exact match fails, while a match that ignores extra whitespace passes. Tesseract and PyMuPDF4LLM kept every contact detail, including on the scanned page.

## Limits of this benchmark

- The resumes are synthetic and short. Real files are messier.
- Most generated files write text in reading order, which favours file-order extractors. Resumes `12`, `25` and `26` show the opposite, but the real mix of producers is unknown.
- Recall and order are measured on words, not on sections or fields. They say nothing about whether a system would assign a job title to the right field.
- The markdown converters are scored on words, as the others are. A pipeline that feeds markdown to a language model also depends on how well that model copes with tables and broken words, which this does not measure.
- PyMuPDF4LLM was run without the optional RapidOCR package, so its OCR used Tesseract. Results with other OCR engines may differ.
- These are open-source libraries on default settings. Commercial applicant tracking systems use their own parsers, and nothing here predicts what any of them does.
- One run, one machine, one resume structure, mostly English text, plus one German, one Russian, one Greek and one Japanese file. Scripts that need text shaping, such as Arabic, Devanagari and Thai, are not covered because the generator cannot draw them. No statistical claims are made.
- Two traps depend on the tool that produced the file (the LaTeX installation and the word processor). The PDFs are committed so results can be reproduced, but rebuilding them elsewhere may differ.

## Reproduce

```text
pip install -r benchmark/requirements.txt
python generator/build.py
python benchmark/run_benchmark.py
python benchmark/make_report.py
```

Tesseract with the `deu`, `rus`, `ell` and `jpn` language packs, and poppler (`pdftotext`) with `poppler-data`, must be installed separately. LibreOffice and a LaTeX installation are needed only to rebuild resumes `20` to `24`.
