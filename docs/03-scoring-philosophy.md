# Scoring philosophy

*How to reason about a score when there is no ground truth.*

This page explains why the score behaves the way it does. It deliberately
contains no weights, thresholds or formulas. Those are private, and the
reasoning stands without them.

## What a score is for

A score answers one question: how well does this document present evidence
for this posting? It does not answer whether the person will be hired, and it
should never be read that way.

Treating it as a measurement of presentation, not a prediction of outcome,
keeps the tool honest. It also gives a clear test for any new rule: does this
help the reader improve how their real experience is shown?

## Deterministic on purpose

The same resume and the same posting produce the same score every time. No
model is involved in producing it.

Reasons this was worth the loss of flexibility:

- **A number you cannot reproduce is not a measurement.** If it changes
  between runs, the user cannot tell whether their edit helped.
- **It can be debugged.** When a score looks wrong, there is a specific cause
  that can be found and fixed. A model's judgement offers no such handle.
- **It can be tested.** Behaviour can be pinned with regression tests, so a
  future change cannot quietly move scores.
- **It is cheap and fast.** The main product does not wait on an external
  service.

The cost is real. A deterministic system cannot learn from data and cannot
capture nuance a person would catch. That trade was made knowingly.

## Evidence, not mentions

A skill that appears only in a list is weaker evidence than a skill shown in
the description of work that used it. The scoring reflects that difference.
This is also what good resume advice says anyway, so the rule rewards a
better resume rather than a trick.

## Borrow expectations instead of inventing them

A scorer needs some idea of what a role typically involves. Inventing that
from opinion would bake one person's guess into every result. Instead, the
engine draws on public occupational data from the U.S. Department of Labor's
O*NET programme as an external reference, and combines it with what the
specific posting asks for.

Using a public benchmark does not make the result correct. It makes the
assumption inspectable and open to argument. What that data gives you, and
what it cannot, is covered in
[Occupational data](10-occupational-data.md).

## Context changes the weighing

A recent graduate and an experienced engineer should not be judged on the
same balance of evidence. A posting that is mostly a list of tools is different
from one that is mostly about collaboration. The weighing adapts to career
stage, field and the emphasis of the posting. A single fixed rubric produces
confident nonsense for most people.

## Partial credit is better than none

People describe the same experience in different words. Near matches earn
partial credit, always less than an exact match. Crediting nothing punishes
honest variation. Crediting equally rewards guesswork. The aim is a point
between them, and the right point differs by field.

## One formula, one implementation

The scoring logic exists once. At one point it existed in three places, and
the test suite was exercising the wrong ones. That story is in
[The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md).
Behaviour is now pinned by snapshot tests taken through the real entry point.

## Calibration without ground truth

There is no external measure of correctness to calibrate against. The score
was shaped by judgement, checked against real cases, and then frozen with
regression tests so that every later change is deliberate.

That is a defensible engineering position. It is not a validated one, and it
should not be described as validated.

## Honest limits

- The score is only as good as the text the parser extracts.
- The relationship between this score and any real employer's system is
  unknown.
- Field coverage is uneven. Fields that are well represented in public
  occupational data are served better.
- No false-positive or false-negative rate has been measured for the scoring
  or its guard rails.

## For your own system

Decide first whether the score is a measurement or a prediction, and say so.
Make it reproducible before making it clever. Use a public benchmark for
assumptions so they can be argued with. Keep one implementation of the
formula, and test the code users actually run. Say what you have not
validated.
