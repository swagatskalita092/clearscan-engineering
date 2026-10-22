# ClearScan Engineering

ClearScan is a production résumé-scoring and job-matching platform launched publicly in July 2026 (development since April 2026) and operated by Swagat Subhash Kalita.

Swagat is the software engineer who designed and implemented the frontend, backend, database schema, payments integration, deployment, and ongoing operation of the product.

## Current scale

- Over 1000 scans run
- 39 FastAPI routes (38 besides the health check)
- 238 automated tests (215 backend, 23 frontend); the backend suite runs on GitHub Actions
- 500+ commits on main since April 2026

Visit the live product: [clearscan.fyi](https://clearscan.fyi)

## AI Features

Both generative features are live in production. They are not placeholders. They are powered by Anthropic: the core score remains deterministic and does not call a model.

- **AI Cover Letter Generator** — Anthropic produces a tailored cover letter from the résumé and the job posting. It is designed not to invent facts.
- **AI Rewrite Suggestions** — Anthropic suggests rewrite wording grounded in the scan results. It is designed not to invent facts.

## Scoring Engine

The core score is deterministic and rule-based, using O*NET data. The same résumé and job description should produce the same number.

- TF-IDF keyword extraction, with O*NET (U.S. Department of Labor) occupation data across 62 industry profiles
- Keyword matching includes synonym recognition with partial credit
- Scoring includes safeguards against keyword stuffing
- Score components: Keywords, Skills, Bullet Quality, Sections, Formatting
- ATS formatting checks across five platforms (Workday, Taleo, Greenhouse, Lever, iCIMS)

## Security and privacy

- GDPR compliance
- EU hosting
- Encryption in transit
- Row-level access control
- Payments handled by Stripe; no card data stored
- 238 automated tests

## Why the source is private

ClearScan is an actively operated commercial product. Its production source code is therefore private. This public dossier documents the product's architecture, engineering decisions, technology choices, operating evidence, and Swagat's role without exposing proprietary source code, customer data, credentials, or sensitive implementation details.

The dossier includes only verified product facts and general architectural context. It omits unverified implementation detail rather than filling gaps with inferred claims.

## Dossier

- [Product and role](docs/product-and-role.md)
- [Architecture](docs/architecture.md)
- [Request and payment flows](docs/request-and-payment-flows.md)
- [Engineering decisions](docs/engineering-decisions.md)
- [Testing and CI/CD](docs/testing-and-observability.md)
- [Security and privacy](docs/security-and-privacy.md)
- [Technology choices](docs/technology-choices.md)
- [Metrics and evidence](docs/metrics-and-evidence.md)
- [Future evidence policy](evidence/README.md)
