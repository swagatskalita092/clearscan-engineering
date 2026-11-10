# Changelog

All notable changes to this documentation repository are recorded here.

## [2026-11-10]

- Added a short screen recording of the searchable site to the top of the README, with a description for readers who cannot see it.
- Release v1.1.0. It adds the eleven-reader parser benchmark, the three diagrams, the ATS myths page and the searchable website to the archived version.
- Extended the research folder to 33 resumes: Arabic (right to left), Hindi (Devanagari) and Thai, made through a word processor because they need text shaping. The benchmark found that most text extractors lose most words in Hindi and Thai files from this producer, and that the cause is how the producer stores shaped text. Added a test of that explanation, a scoring rule that keeps combining marks inside words, and the producer versions to the record.
- The README badge and the citation file now use the DOI that always points to the latest version. Each release also has its own version DOI on Zenodo.

## [2026-11-09]

- Rewrote the engineering decisions page in the house style, with limits and a closing section.
- Added a documentation index with reading paths, a citation file, and a proposal form.
- Extended the documentation check to enforce the house rules automatically.
- Removed an empty placeholder folder and replaced "one person" wording with neutral wording.
- Added a research folder with 26 invented resumes built around parsing traps, ground truth for each, and a first benchmark of eight text extractors. Data is CC0 and code is MIT.
- Extended the research folder to 30 resumes: a German-language CV with a photo, and Russian, Greek and Japanese resumes. The benchmark now records the poppler-data dependency and how OCR language is handled.
- Added three diagrams (system overview, a scan end to end, and the layers around generated text) to the architecture and generated-text pages.
- Added "ATS myths and the evidence": six common claims graded against public sources, with a short note on the EU AI Act dates.
- Extended the parser benchmark from eight to eleven readers: pypdf in layout mode, PyMuPDF4LLM and MarkItDown, which are what people use to feed documents to language models. New findings include layout analysis helping on columns, markdown converters inventing tables, and one converter running OCR on its own.
- Added a searchable website built from the Markdown by scripts/build_site.py and published with GitHub Pages. It has full-text search across every section, works in light and dark mode, and makes no requests to other domains. It is live at swagatskalita092.github.io/clearscan-engineering. The documentation check workflow now also builds the site, so a broken link fails a pull request.

## [2026-11-05]

- Added: occupational data (O*NET and ESCO, limits and licence) and resume conventions around the world.
- Linked the new pages from the README, scoring philosophy, technology choices and the build-your-own guide.
- Simplified the architecture, security and decisions pages. Payment incidents now describe the provider in general terms.

## [2026-11-04]

- Switched the repository visuals to the ClearScan brand theme: new banner, orange icon set and diagram colours.
- Opened the repository to contributions: contributing guide, code of conduct, security policy, issue and pull request templates, and an automatic documentation check.
- Rewrote security and privacy, replaced a bare GDPR compliance claim with accurate wording, and wrote the build-your-own guide.
- Rewrote architecture, technology choices, and testing pages. Corrected the claim that frontend tests are not part of CI.
- Added: scoring philosophy and anti-gaming principles.
- Redesigned the README with a custom banner and icon set.

## [2026-11-03]

- Added: the problem, AI that doesn't invent facts, and an incident write-up on the tests that tested a copy. Redesigned the README.
- Added incident write-up: the empty list.
- Added incident write-ups: the disabled webhook, green tests with broken production, and the AI verifier decision.

- Restructured the repository as engineering field notes.
- Moved changing figures to STATUS.md.
- Added LICENSE (CC BY 4.0).
- Recorded that ClearScan is free.
