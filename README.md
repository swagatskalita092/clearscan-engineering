# ClearScan Engineering
Field notes from building and running a production ATS resume scanner.

[ClearScan](https://clearscan.fyi) is a free tool that scores a resume
against a specific job posting and shows every rule behind the number. It is
operated by one person. This repository is not its source code. It is a
write-up of how the system is built, what broke, and what those failures
taught. The scoring engine is private. The reasoning behind it is not.

## Start here
- [The problem](docs/01-the-problem.md)
- [Architecture](docs/02-architecture.md)
- [Scoring philosophy](docs/03-scoring-philosophy.md)
- [Anti-gaming](docs/04-anti-gaming.md)
- [AI that doesn't invent facts](docs/05-ai-that-doesnt-invent.md)

## Incidents
Real production failures: what it looked like, how it was found, and the
general lesson.
- [The disabled webhook](incidents/01-the-disabled-webhook.md)
- [The empty list](incidents/02-the-empty-list.md)
- [Green tests, broken production](incidents/03-green-tests-broken-production.md)
- [Throwing away the AI verifier](incidents/04-throwing-away-the-ai-verifier.md)

## Reference
- [Technology choices](docs/06-technology-choices.md)
- [Testing and CI](docs/07-testing-and-ci.md)
- [Security and privacy](docs/08-security-and-privacy.md)
- [Engineering decisions](docs/09-engineering-decisions.md)
- [Payment architecture (historical)](docs/10-payment-architecture.md)
- [Build your own](build-your-own/README.md)
- [Current figures](STATUS.md) and [Changelog](CHANGELOG.md)

## In brief
React and Vite frontend, FastAPI backend, PostgreSQL on Supabase, deployed on
Netlify and Railway. The core score is deterministic and rule-based: the same
resume and posting always produce the same number, because a score you cannot
reproduce is not a measurement. No language model is called to produce it.
Two features use a model, both for generating text rather than judging, and
both are checked deterministically against the user's actual resume.

ClearScan charged for a subscription until 31 October 2026 and has been free
for every registered user since.

## What this repository is not
Not the ClearScan source code, which is private. Not open source software.

## License
The writing in this repository is licensed under CC BY 4.0: reuse and build
on it freely with credit. The license covers these documents only, not the
ClearScan software, name or logo.

## Author
Swagat Subhash Kalita designs, builds and operates ClearScan.
[clearscan.fyi](https://clearscan.fyi) and
[LinkedIn](https://www.linkedin.com/company/clearscan-ats/)
