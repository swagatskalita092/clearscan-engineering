# The empty list

*One return value that meant two different things deleted real user data.*

| | |
|---|---|
| Dates | 23 October 2026 (first fix), 28 to 30 October 2026 (real fix) |
| Feature | The job application tracker |
| Impact | Rows lost job links, descriptions, titles or dates on weak connections |
| Root cause | A failed database read was reported as an empty result |
| Found by | The operator, using the tracker on a slow connection |

## What happened

The tracker is a spreadsheet-like page where a user keeps the jobs they are
applying to. It saves automatically. On a weak connection, deleting a row
could also wipe the job link and description of other rows, and later the
title and date as well.

## First cause, first fix

The login state object handed to the page was recreated on every
authentication update. The tracker's load logic depended on it, so a late
background login check made the page download the server's copy again and
write it over edits that had not been saved yet. The next autosave then made
the loss permanent.

The fix loaded data once per user, saved one request at a time with the
latest state queued behind it, showed a visible "not saved yet, retrying"
status, and warned before the tab was closed with unsaved changes.

The same symptom came back on a weak connection a few days later. Fixing one
cause had not fixed the symptom.

## Second cause

Reading the code, not the logs, found it. The database helper used by the
tracker returned an empty list on any failure. A timeout, a dropped
connection or a database error all looked identical to a user with no data.

So when the database hiccuped, the read endpoint answered with success and an
empty tracker. The page treated that as the truth and showed default columns
and one blank row. Autosave then wrote that blank state over the user's real
data.

There were two more weaknesses underneath:

- Saves were last-write-wins with no version check. An old tab or another
  device could overwrite newer data with an older copy.
- Requests had no timeout, so a hung request could block saving, and a failed
  first load had no retry.

## The fix

Three layers, built in order, each merged separately:

1. **Safe reads and writes.** A strict read helper that returns a distinct
   failure signal. The read endpoint now answers with a server error instead
   of an empty success. Saves carry a version, use compare-and-swap, and
   reject stale writes with a conflict response. Requests have timeouts and
   the first load retries.
2. **Local-first.** The product direction was to behave like a spreadsheet:
   typing never waits for the network. Edits are saved on the device first,
   sync happens quietly in the background with retries, and each cell is its
   own operation, so two tabs editing different cells merge instead of one
   wiping the other.
3. **Storage failures.** If the device cannot store data, the page says so
   honestly and warns before the tab is closed.

A copy of the table was taken before the rebuild went live as a safety net.

## The type system as a fix

The last step was making the mistake impossible to repeat. A local-store read
used to return null both when nothing was stored and when parsing failed. It
now returns one of two explicit shapes: ok with the data, or not ok with an
error. A caller cannot touch the data without first checking which case it
got.

This was a deliberate use of TypeScript on the data layer only, motivated by
this exact bug.

## What is still not proven

- The page code that calls the new shape is plain JavaScript, so the compiler
  does not check it, and the automated tests cover the library code, not the
  page. Four call sites there were updated by hand. A live check by the
  operator is the only verification they work.
- Two real browser tabs editing at once, typing with the network off then
  reloading, and a real storage-quota failure have not been exercised
  against the real database. The merge logic is covered by tests that mock
  the database.

## Lessons

- **Never let "empty" and "failed" share a return value.** A function that
  returns an empty list on error converts an outage into data loss.
- **A write that trusts a failed read is a delete.** Autosave plus a read that
  lies is the whole bug.
- **Fail loudly.** A server error would have shown a retry button. A quiet
  success deleted data.
- **Fixing one cause is not fixing the symptom.** The first fix was correct
  and the bug returned. When a symptom comes back, assume a second cause.
- **Last-write-wins is a decision, not a default.** If an old client can erase
  newer data, it eventually will.
- **Make the type refuse the ambiguity.** Where a bug lives in a return value,
  change the return type, so the compiler or the tests catch the next one.
- **Be honest about the gaps.** The unverified call sites are listed here
  because pretending the fix is fully proven would repeat the original sin:
  reporting success without checking.
