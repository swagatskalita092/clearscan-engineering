# Green tests, broken production

*Every test passed while every live payment check was failing.*

| | |
|---|---|
| Date | 4 October 2026, same day as the webhook incident |
| Impact | All live payment verification failed from deploy until the fix |
| Real customers affected | None. Only the operator's own test account was in flight |
| Root cause | Tests mocked a library's objects with a type that behaves differently |
| Found by | Testing the change live with a fresh account |

## What happened

A refund check was added to payment verification. It needed a small helper
that reads a field from a Stripe response. The helper was written to accept
either a plain dictionary or a Stripe SDK object, and it decided which one it
had by checking for a get method.

Every test passed. The tests built fake Stripe responses as plain
dictionaries, and dictionaries have a get method.

Real Stripe SDK objects do not. Reading that attribute on a real object
raised an error inside the library. The helper caught the error and returned
nothing. In production, the payment status and the paid flag always read back
as empty, whatever Stripe actually said. Every live verification and every
manual sync was failing, not only the refund case it was written for.

## How it was found

Not by the test suite, and not by monitoring. The operator tested the refund
fix live with a fresh account. The upgrade failed with "Stripe does not show
this payment as paid" and the sync button returned errors repeatedly.

## Blast radius

Checked rather than assumed. Only two live checkout sessions existed on that
day. One predated the broken change and was correctly blocked for being
refunded. The other was the operator's own test account. Nobody else could
have been affected.

## The fix

- The helper now handles each object type correctly.
- The refund lookup runs only after the paid check has already passed, and an
  error in the refund lookup can no longer turn a good payment into a
  "not paid" result.
- New tests construct responses from the real SDK classes, which is exactly
  what the dictionary mocks could not catch.

## Lessons

- **A mock encodes your assumption.** If the test double behaves differently
  from the real object, the test proves only that your assumption agrees with
  itself.
- **A helper that swallows errors turns a crash into a wrong answer.** A loud
  failure would have been caught in seconds. Returning an empty value made
  the system quietly wrong.
- **Build test data from the real library.** Most SDKs can construct real
  objects from a dictionary. Use that for anything that crosses a boundary
  you do not control.
- **Exercise payment changes with a real flow.** Unit tests had no way to
  surface this. One live transaction did, within minutes.
- **Check the blast radius before panicking.** Looking at the actual records
  turned a possible incident into a contained one.
