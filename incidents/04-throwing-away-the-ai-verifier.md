# Throwing away the AI verifier

*Built a second model to catch the first one's lies. Measured it. Deleted it from the path.*

| | |
|---|---|
| Date | 24 and 25 October 2026 |
| Feature | AI-generated cover letters |
| Decision | The AI verifier is off in production |
| Replaced by | Deterministic checks that highlight, plus a better writing model |

## The problem

A language model writing a cover letter from a resume will sometimes invent:
a tool the candidate never used, a "production" system that was a prototype,
a number that is not in the resume, a sentence copied from the job posting
and presented as experience. For a job application, an invented claim is not
a cosmetic flaw.

## The idea

Add a second model call that checks every claim in the draft against the
resume, requiring a quoted piece of evidence for each, and a repair step that
rewrites anything unsupported. It is an obvious design, and it was built.

## What the measurement showed

The verifier was evaluated on letters containing eight claims known to be
wrong.

- It caught about half of them, four or five of the eight.
- It raised false alarms when its own quotations of the resume were slightly
  inaccurate.
- A single letter took 29 to 62 seconds and five or six model calls.
- The repaired letters were worse: gutted and generic, and often still
  flagged.
- On a newer model with extended thinking, each verifier call took 30 to 45
  seconds and sometimes ran out of its token budget.

The cost was a few cents per letter with the verifier, against a fraction of
a cent for a single draft.

## Why that outcome is worse than it looks

A verifier that misses half the problems is not a safety net, it is false
assurance. Showing a "verified" badge on a letter that still contains an
invented claim is more dangerous than showing no badge, because the user
stops reading carefully.

## What replaced it

- A newer, small writing model that produced faithful drafts on its own: it
  kept "prototype" as "prototype" and did not borrow phrases from the posting.
- Fast deterministic checks that compare numbers, tools and certain phrases
  against the resume, and highlight what they find.
- Highlights, never silent deletion. The user sees what was flagged and
  decides.
- Honest wording on the result: the letter is checked automatically, and the
  user should still read it once before sending.

The verifier code was kept behind a flag for offline experiments, and it is
off by default.

## What is less certain

A later review found that the evaluation script's defaults had differed from
production during earlier tuning rounds. Treat the quality comparisons above
as indicative rather than exact. The time cost was large enough that the
decision did not depend on them.

## Lessons

- **Measure your clever idea.** It looked obviously right and was not worth
  shipping.
- **Latency is a feature.** A check that takes a minute is a different
  product.
- **Prefer the cheap fix upstream.** A better writer prevented more problems
  than a second model catching them afterwards.
- **Do not claim more assurance than you have.** The interface says the
  letter was checked automatically and asks the reader to check again.
- **Verify the thing you measured is the thing you run.** Check the
  evaluation configuration against production before trusting results.
