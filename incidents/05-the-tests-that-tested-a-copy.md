# The tests that tested a copy

*A green test suite that never touched the code users run.*

| | |
|---|---|
| Date | Found 10 October 2026, resolved 23 October 2026 |
| Impact | None observed. The copies matched when found |
| Risk | Any change to the production path could pass every test unnoticed |
| Root cause | The scoring formula existed in three places |
| Found by | An audit that read the code and traced who calls what, not a test run |

## What happened

The scoring formula lived in three places.

1. An inline implementation inside the endpoint that every real user hits.
2. A second, near-identical function that only the end-to-end tests called.
   Nothing reachable from the API used it.
3. A third, simplified version inside a test file, with no anti-gaming logic
   at all, used for score-band assertions.

The tests that exercised scoring were testing copies two and three. The two
tests that did call the real endpoint used a mocked score, so they checked
permissions, not arithmetic.

## Why it mattered

A change made only inside the production block could pass every test while
silently altering what users saw. Equally, a deliberate change had to be
remembered in all three places, or a test would go stale or fail for the
wrong reason. The safety net was testing the wrong parachute.

## What the audit did and did not find

Comparing the production block against the tested copy line by line showed
they matched. Nothing was wrong with the live score. The risk was structural.

The audit also found two smaller problems of the same family. Two project
documents disagreed with the code, and with each other, about the value of a
tuning constant. And a number of exceptions were being swallowed silently,
none of them inside the score maths, but each one a place where a real
failure would look identical to "nothing to report".

## The fix

- The production endpoint now calls the single pipeline function. One formula,
  one implementation, and the existing end-to-end tests cover what users run.
- Before changing anything, a golden-master test captured the output of the
  real endpoint on a set of real inputs. The same snapshots passed unchanged
  after the refactor, which proves the numeric score did not move.
- The simplified copy in the test file was deleted along with the few tests
  that depended on it alone. Each was covered by an equivalent test elsewhere.

## What the safety net does not cover

The golden-master cases all come from a single field, and results are compared
as sorted lists, so a pure change in ordering would not be caught. A manual
check remained: re-run an old scan and confirm the score matches.

## Lessons

- **A test proves only what it calls.** Search for who calls the function
  under test. If production never does, the test is decoration.
- **One formula, one implementation.** Duplicated logic drifts, and the
  drift hides in the tested copy.
- **Take the golden master first.** Record behaviour through the real entry
  point before refactoring, then refactor until the snapshots still match.
- **Mocking the answer tests the plumbing, not the maths.** A mocked score
  fixture cannot catch a wrong score.
- **Read the code, not only the results.** The audit found this by tracing
  callers. A run of the test suite would have shown only green.
- **Documentation is a copy too.** Written constants drift from the code that
  holds the truth.
- **Swallowed errors make failure look like silence.** Log at least a warning.
