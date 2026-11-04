# Anti-gaming

*Detecting resumes written for the scanner rather than the job, without
punishing honest ones.*

This page covers principles. It does not contain thresholds, ratios, limits
or the list of patterns the system looks for, and the reasons are given
below.

## The problem

The moment a score exists, some people will optimise the number instead of
the resume. The tactics are predictable: repeating terms from the posting,
listing terms with nothing behind them, copying the posting into the resume,
and tuning text mechanically with a language model until it mirrors the
posting.

Doing nothing rewards the people who do this and punishes the people who do
not. Reacting too hard punishes honest resumes that happen to look like a
tactic. Every choice is a trade between those two errors.

## Principles

**Compare against the posting, not against a fixed number.** A fixed limit on
how often a term may appear punishes fields where the posting itself repeats
its key terms. What counts as unusual has to be measured against what is
normal for that posting.

**Limit, do not accuse.** When a pattern looks like optimisation for the
scanner, the response is a ceiling on how high the score can go. It is not a
zero, not a ban and not a label on the person. A limit that turns out to be a
false alarm costs the user some points. An accusation that turns out to be a
false alarm costs them their trust and possibly their application.

**No single signal is proof.** The system looks at different failure modes
with different checks, and treats each as evidence, not a verdict.

**Say what was seen.** If the tool limits a score, it explains the pattern in
plain words. An honest user with an accidental pattern can fix it. A user who
was gaming at least knows it was noticed.

**Same rules for everyone.** The behaviour is deterministic. No individual is
treated differently, and a result can be reproduced and disputed.

**Reward the honest path.** The simplest way to reach a high score should
always be to improve the resume: show real evidence of real work in the places
a reader would expect it.

## Why the exact limits are not published

Publishing precise thresholds turns the system into a recipe. Anyone could
read them and stay just under each one, and the guard rails would stop doing
their job without anyone noticing. The principles above are enough for another
team to design their own, and their numbers would be theirs.

This is a deliberate asymmetry: the reasoning is open, the constants are not.

## Honest limits

- **The false-positive rate has not been measured.** Doing so needs a
  labelled set of genuine and optimised resumes, and that set does not exist.
  The design leans on limits rather than penalties precisely because the
  error rate is unknown.
- **This is an arms race.** Any fixed approach will eventually be worked
  around, and the rules will need to change.
- **Real systems may not care.** A scanner that penalises a pattern cannot
  claim a real employer's software does the same. The aim is to discourage
  resumes that read badly to humans, not to impersonate a vendor.
- **Fields with dense vocabulary are harder.** Honest resumes in
  keyword-heavy fields can look like optimised ones.

## For your own system

Measure against the posting, not a constant. Cap rather than ban. Explain
every limit in plain language. Keep your thresholds out of public view and
your reasoning in it. Write down which error you chose to risk, and measure
it as soon as you can.
