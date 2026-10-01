# Product and Role

## Product

ClearScan is a production résumé-scoring and job-matching platform. It has been live since June 2026 at [clearscan.fyi](https://clearscan.fyi).

The product provides a deterministic, rule-based core scoring engine to every free user. That engine uses:

- TF-IDF keyword extraction
- A custom skills taxonomy
- U.S. Department of Labor O*NET occupational benchmarking data

Score components: Keywords, Skills, Bullet Quality, Sections, Formatting.

The Anthropic Claude API is not used for the core score. It is limited to two gated premium capabilities:

1. AI-assisted bullet rewrite suggestions
2. AI-generated cover letters

## What a user experiences

Scoring is not generic. It is a compatibility score between one résumé and one job description.

The user pastes or uploads a résumé, pastes the actual job description text into a second field, and selects an analysis profile: a domain (for example "Software Engineering") plus an experience level (for example "Entry Level"). Returning users get that profile pre-filled from a saved account preference. Measured end-to-end parse time is under 6 seconds.

The score is not an LLM judgment. It measures how that specific résumé lines up with that specific job description. The chosen domain and level select the matching profile against U.S. Department of Labor O*NET occupational benchmarks. The path still uses TF-IDF extraction, a custom skills taxonomy, and O*NET data. In plain terms: keyword and skill alignment against the pasted posting, not a generated opinion.

A History page stores each result with its score, domain, level, and timestamp. Results persist across sessions. They are not one-off.

### Free tier

Every free user receives the deterministic score, verdict, top issues, a keyword preview, a section check and rule-based suggestions. There is no Claude call on the core score. Full keyword lists, skill analysis, the five-platform ATS details, bullet analysis and interview probability are paid, as are the two Claude-backed generation features.

### Paid tier

A paid subscription adds those full analysis details and the two Claude-backed features. These are the only places the Anthropic Claude API is used:

1. Bullet rewrites. The user selects a résumé bullet, requests an AI rewrite, and receives a suggested improved version grounded in the scan results. It is designed not to invent facts.
2. Cover letters. The user provides résumé text and job description text only. The user receives a tailored draft. It is designed not to invent facts.

## Who it is for

ClearScan is for job seekers who want to evaluate and improve their application materials through résumé scoring and job matching.

## Swagat's role

Swagat Subhash Kalita is ClearScan's solo founder and engineer. He designed and implemented the complete stack himself, including:

- Frontend application
- Backend application and API
- Database
- Payments integration
- Deployment setup and CI/CD
- Ongoing product operation

This is not a team project or a demonstration application. It is a live commercial product that Swagat continues to operate.

## Current operating footprint

- 1000+ résumés parsed
- Under 6 seconds end-to-end parse time
- 38 FastAPI endpoints
- 170+ automated tests with a 100% pass rate
- 220+ commits to production since July 2026

## Operating notes

The 170+ automated tests and 100% pass rate sit on the GitHub Actions pipeline. Stripe handles upgrades, renewals, and downgrades, so subscription state is part of ongoing operation rather than a manual checklist.

There is no public-facing changelog or release notes page. GitHub Actions runs the automated tests on every push and pull request to main. Production deploys happen automatically from the main branch: the frontend on Netlify and the backend on Railway.

A documented example of treating user-found defects as product defects is in [engineering-decisions.md](engineering-decisions.md).
