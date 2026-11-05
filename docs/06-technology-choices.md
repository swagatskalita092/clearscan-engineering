# Technology choices

*What was picked, why, and what each choice cost.*

Most technology lists stop at the pick. This page keeps the bill. Every row
below is grounded in something that actually happened.

| Choice | Why it was picked | What it cost |
|---|---|---|
| **FastAPI on Python 3.12** | Typed request validation, async support, and Python's text-processing ecosystem for the scoring work | The API grew by accretion into very large modules, which let the scoring formula be duplicated. See [The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md) |
| **Deterministic rules, TF-IDF and public O*NET data** | Reproducible, explainable, and no per-scan model cost | It cannot learn from data. Occupational data must be curated, and coverage is uneven across fields. See [Scoring philosophy](03-scoring-philosophy.md) and [Occupational data](10-occupational-data.md) |
| **Supabase: PostgreSQL and authentication, EU region** | One managed service for both, with row-level access control and EU residency | Authentication and data are coupled to one vendor. Database access over plain HTTP through an in-house helper hid an outage as emptiness. See [The empty list](../incidents/02-the-empty-list.md) |
| **Netlify and Railway, deploying from main** | No deployment ceremony for a small project | No staging environment, so main is production. The browser security policy must be updated for every new third-party origin |
| **GitHub Actions** | Tests on every push and pull request, scheduled maintenance jobs, and a weekly production check | A red build only helps if someone reads it. CI was red for three commits before anyone noticed, because the failure emails were going unopened |
| **A small language model for two text features** | Writing is the deliverable, so a model fits | Latency and cost had to be measured, reasoning mode was switched off, and an AI verifier was built and removed. See [AI that doesn't invent facts](05-ai-that-doesnt-invent.md) |
| **In-browser PDF generation with a WebAssembly typesetter** | No server-side rendering service to run | A very large one-time download for the user, and a specific allowance in the browser security policy |
| **A local-first job tracker** | Typing never waits for the network | Much more code than a plain save button: sync, conflict merging and storage-failure handling. See [The empty list](../incidents/02-the-empty-list.md) |
| **TypeScript on the data layer only** | Introduced to make one specific bug impossible to repeat | A mixed codebase, and page code that the compiler does not check |
| **Resend for email** | A simple API | Two systems used separate credentials, and one silently failed until it was traced. See [The disabled webhook](../incidents/01-the-disabled-webhook.md) |

## How to use this page

Do not copy the picks. Copy the habit: when you choose a technology, write
down the cost you expect, and come back later to see what it really was.
Your team, scale and constraints will make different choices correct.
