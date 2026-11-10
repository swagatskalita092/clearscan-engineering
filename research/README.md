# Research

*Things that can be run, measured and reused, kept apart from the written
notes in [docs](../docs/README.md).*

The notes in this repository are licensed CC BY 4.0. This folder is different
on purpose: it holds data and code that other people will want to build on, so
it uses licences with fewer conditions.

| What | Licence | File |
|---|---|---|
| Data: resumes, ground truth, results | CC0 1.0, public domain | [LICENSE-DATA](LICENSE-DATA) |
| Code: generator and benchmark scripts | MIT | [LICENSE-CODE](LICENSE-CODE) |

## What is here

| Project | What it is |
|---|---|
| [Synthetic resumes](synthetic-resumes/README.md) | 33 invented resumes, each built around one parsing trap, with ground truth and a benchmark of eleven readers, from plain extractors to layout-aware converters and OCR |

## Rules for everything in this folder

- Nothing here contains a real person's data. Every name, employer, address
  and number is invented.
- Nothing here describes how ClearScan scores a resume. These are general
  tools for anyone building or evaluating a resume reader.
- Results say what was run, with versions, on what, and what the numbers do
  not show.

## Contributing

Add a trap, a producer or an extractor by following the steps in the
[synthetic resumes README](synthetic-resumes/README.md). Related open issues:
[parsing traps catalogue](https://github.com/swagatskalita092/clearscan-engineering/issues/7)
and [layout-aware parsing benchmark](https://github.com/swagatskalita092/clearscan-engineering/issues/12).
