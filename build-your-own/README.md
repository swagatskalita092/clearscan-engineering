# Build your own

*What you would need to build an ATS resume scanner, in the order that hurts
least.*

This is not a recipe for copying ClearScan. It leaves out the numbers on
purpose, because yours should be your own. It is the order of work and the
mistakes worth avoiding.

## Decide three things before any code

1. **Is the score a measurement or a prediction?** A measurement says how well
   a document presents evidence for a posting. A prediction says what will
   happen to the candidate. You can honestly build the first. Say which one
   you built.
2. **Who is it for, and what will they do with the number?** A score someone
   uses to decide what to edit is different from one they use to decide
   whether to apply.
3. **What will you refuse to claim?** Write it down now, before marketing
   writes it for you.

## The build order

1. **Parsing first.** Collect real, messy files: columns, tables, odd
   bullets, scanned pages. Measure what your parser reads wrongly. Every later
   stage inherits its mistakes, and many "scoring bugs" are parsing bugs. If
   your users are in several countries, see
   [Resume conventions around the world](../docs/11-resume-conventions-around-the-world.md).
2. **A small, legible baseline score.** A handful of components you can each
   explain in one sentence. Make it reproducible before making it clever. See
   [Scoring philosophy](../docs/03-scoring-philosophy.md).
3. **Pin it.** Capture the output of the real entry point on real inputs
   before you refactor anything. Keep exactly one implementation of the
   formula. See
   [The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md).
4. **Explanations.** For every deduction, say in plain words what happened and
   what to change. Decide what each explanation reveals.
5. **External benchmarks.** Use public occupational data for assumptions
   about what roles involve, so the assumptions can be argued with. Pin the
   version, review every update, and read the licence. See
   [Occupational data](../docs/10-occupational-data.md).
6. **Guard rails.** Assume gaming from the first day. Compare against the
   posting, cap rather than ban, and say what was seen. See
   [Anti-gaming](../docs/04-anti-gaming.md).
7. **Accounts and storage**, only when you need them. Anything users type
   should survive a bad connection.
8. **Generated text, last.** If you add a language model, constrain it and
   check it. See
   [AI that doesn't invent facts](../docs/05-ai-that-doesnt-invent.md).
9. **Payments, last or never.** If you take them, verify with the provider,
   deduplicate webhook events, and alert on the absence of events. See
   [The disabled webhook](../incidents/01-the-disabled-webhook.md).

## Decisions that are expensive to reverse

- **Never let "empty" and "failed" look the same.** See
  [The empty list](../incidents/02-the-empty-list.md).
- **Evaluate the configuration you run.** A test that measures a different
  setup than production proves nothing about production.
- **Decide where private test resumes live** before you have any.
- **Decide how you will stage changes.** ClearScan has no staging
  environment, and it shows.
- **Treat every third-party call as a policy change** for the browser's
  security rules.

## Traps, with the incidents that taught them

| Trap | Read |
|---|---|
| Fixing symptoms when the primary path is dead | [The disabled webhook](../incidents/01-the-disabled-webhook.md) |
| A read that fails looking like an empty result | [The empty list](../incidents/02-the-empty-list.md) |
| Mocks that behave unlike the real thing | [Green tests, broken production](../incidents/03-green-tests-broken-production.md) |
| A second model checking the first | [Throwing away the AI verifier](../incidents/04-throwing-away-the-ai-verifier.md) |
| Tests that exercise a copy of the code | [The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md) |

## What to measure from the start

- A labelled set of resumes and postings with human judgements. ClearScan does
  not have one, and its guard rails are weaker for it. Yours can be better.
- Parse accuracy on real files.
- Agreement between your ranking and human reviewers.
- The false-positive rate of every guard rail.
- Time and cost per scan, and per generated text.

## What to skip at first

- Machine-learned scoring, until you have data to justify it.
- Generated text, until the core score is trusted.
- Tuning for dozens of fields. Start with one you understand.
- Trackers, builders and extras.

## Use it responsibly

- A resume is personal data. Say plainly who sees it.
- Do not imply a score predicts hiring.
- Do not promise to match a named vendor's behaviour.

## What you will not find here

Weights, thresholds, dictionaries or prompts. That is deliberate, and they
would not transfer anyway: your field, your users and your data differ. Build
yours, and measure it.

## A one-page checklist

- [ ] The score is described as a measurement or a prediction, and users are
      told which
- [ ] Parsing is tested on real, messy files
- [ ] One implementation of the formula
- [ ] Golden-master snapshots through the real entry point
- [ ] Every deduction has a plain-language explanation
- [ ] Guard rails cap rather than ban, and explain themselves
- [ ] Failed reads cannot look like empty results
- [ ] Evaluation configuration equals production configuration
- [ ] Generated text is checked against the source resume
- [ ] There is an alert for the absence of expected events
- [ ] Private test data stays out of version control
