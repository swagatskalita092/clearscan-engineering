# The disabled webhook

*Six real bugs fixed in one day, and the cause was none of them.*

| | |
|---|---|
| Date | 4 October 2026 |
| Impact | One real customer charged and left on the free plan |
| Root cause | The payment provider's webhook endpoint was switched off |
| Found by | Walking through the provider's dashboard after every code fix had shipped |

## What happened

ClearScan took payments through Stripe Checkout. When a payment succeeds,
Stripe sends a webhook event to the backend, which marks the payment complete
and upgrades the account. Two fallbacks exist: the success page checks the
payment directly with Stripe, and a manual "sync" button repeats that check.

A friend bought the plan live, on a screen share, a day after a round of
billing hardening shipped. The charge succeeded in Stripe. The success page
said it could not verify the payment, and the sync button failed too. The
payment record in the database was stuck as pending.

## The investigation

The first suspect was the code that had just shipped, and the first fixes were
genuine:

- The success page swallowed every exception into one generic message, which
  made a real failure look like a declined card. It now says what went wrong.
- The sync button refused any record not already marked complete, so it could
  never rescue a pending one. It now asks Stripe and accepts pending records
  that Stripe confirms as paid.

Each fix exposed the next problem. A refund check was added because Stripe
does not change a payment's status when it is refunded; the refund is
recorded separately on the charge. That check shipped a regression, described
in [the next incident](03-green-tests-broken-production.md). When the webhook
finally started delivering again, the handler crashed on an unexpected empty
metadata field. After that, it wrote a plan name that the other code paths
normalised first, and the database rejected it. A scheduled reconciliation
job turned out to be blind to refunds. Alert emails to the operator had been
failing silently because the backend shared an email credential with a
different system.

That is six distinct bugs, all real and all worth fixing.

## The actual cause

After all six were fixed, a brand new test account still needed the manual
sync button to get upgraded. That should not happen when the webhook works.
Opening the Stripe dashboard showed the webhook endpoint was disabled, with
zero deliveries for the entire week on the chart.

The primary path had been dead the whole time. Every payment depended on the
fallbacks, and the fallbacks were the thing that kept breaking. Re-enabling
the endpoint made a fresh signup upgrade instantly with no manual step.

## What was never found

Why the endpoint was disabled is still unknown. It may have been switched off
by hand, or disabled automatically after earlier failures that scrolled out
of view. The only safeguard since is a manual look at the dashboard.

## Lessons

- **Silence looks like health.** A webhook that never fires produces no
  errors, no logs and no failed requests. The absence of events is invisible
  unless something is counting them.
- **A working fallback hides a dead primary path.** Once the manual sync
  worked, nothing complained, so nothing pointed at the real problem.
- **Many bugs can share one cause.** Six symptoms in a row is a signal to
  step back and check the plumbing, not only the code.
- **Verify the real flow.** The incident closed only when a new signup paid
  and was upgraded with no manual action, not when unit tests passed.
- **Know your dedup trade-off.** Webhook handling records each event before
  acting on it and removes the record if the action fails, so the provider
  retries. If that removal itself failed, a retry would be skipped as a
  duplicate and a failed upgrade would be masked. It did not happen here, but
  the failure mode is worth knowing.

## For your own system

Alert on the absence of events when you expect them. If checkouts are being
created and no webhook has arrived for a few hours, something is wrong, and
you want to hear about it before a customer does.
