# Engineering decisions

*Four product decisions that were meant to last, and what each one cost.*

These decisions shape what ClearScan does and what it refuses to do. They are
written down because they are easy to undo by accident when a new feature seems
to call for an exception.

## 1. Keep the core score deterministic

The core scoring engine is rule-based, not model-based. It uses TF-IDF keyword
extraction, a skills taxonomy and public occupational benchmarks from the U.S.
Department of Labor's O*NET programme.

**Why.** The same resume should score the same way every time. The path every
user depends on should not wait on a model call, and a model in that loop would
add output that cannot be repeated or debugged.

**Why O*NET.** It gives the skills taxonomy an external, public benchmark
instead of an invented list of what a role "should" look like, and people can
recognise the source. That is a choice about transparency. It is not a claim
that the score is an official assessment. See
[Occupational data](10-occupational-data.md).

**What it cost.** A deterministic system cannot learn from data. For the same
reason, ClearScan does not describe its score as AI-powered. See
[Scoring philosophy](03-scoring-philosophy.md).

## 2. Use a language model only where text is the deliverable

A language model provider is used for two features:

- AI-assisted bullet rewrite suggestions.
- AI-generated cover letters.

Both are generative writing tasks. The user is asking for new prose, so the
model's output is the deliverable. Scoring is the opposite problem: it should
be fast, repeatable and stable, and mixing the two would put a model in charge
of a number that needs to be stable.

A rewrite starts from a bullet the user selects and is grounded in the scan
results. A cover letter is built from the resume text and job text only. Both
are designed not to invent facts, and neither changes the score. See
[AI that doesn't invent facts](05-ai-that-doesnt-invent.md).

**What it cost.** Each call has a real cost and a variable delay, and a model
can still be wrong, which is why the checks exist.

## 3. Keep variable-cost work apart from the core score

Every registered user receives the deterministic score, verdict, top issues, a
keyword preview, a section check and rule-based suggestions, with no model call
on the core score. The two generation features sit apart from it.

The split matters for two reasons. Each generated result carries a cost and a
delay that the core score does not. And users should always be able to tell
which results are deterministic and which were generated.

**What it cost.** A boundary that has to be defended. A feature that blurs it
needs a strong reason.

## 4. Treat user-found defects as product defects

When a real resume exposes a problem, it is treated as a defect in the product,
not as a user mistake. It is fixed and pinned with an automated test so that it
cannot quietly return. See [Testing and CI](07-testing-and-ci.md) and
[The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md).

**What it cost.** A growing suite that has to stay trustworthy, because a test
that checks the wrong code is worse than no test.

## Honest limits

- Determinism makes the score reproducible. It does not make it correct or
  validated.
- Checks on generated text reduce invented facts. They do not remove them.

## For your own system

Decide where a model is allowed before you add one, and write the boundary
down. Treat every defect a real user finds as a missing test.
