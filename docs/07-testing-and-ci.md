# Testing and CI

*What the tests cover, what they miss, and the checks that run without anyone
asking.*

ClearScan has hundreds of automated tests across the backend and the
frontend. Exact current counts live in [STATUS.md](../STATUS.md).

## What runs on every change

GitHub Actions runs the backend suite and the frontend suite on every push and
every pull request to the main branch. Production deploys automatically from
main only after that, the frontend on Netlify and the backend on Railway.

## The kinds of test

- **Unit and pipeline tests** for scoring components and for the full path
  from a resume and posting to a result.
- **A golden-master test** that pins the real scoring endpoint's output on
  real inputs, so a refactor cannot quietly move scores.
- **Regression tests for user-found defects.** A problem found by a real
  person on a real resume is a product defect, and it gets a test.
- **Tests built from real library objects** for anything crossing a boundary
  the project does not control, after dictionary mocks hid a production
  failure.
- **A test that pins the committed production configuration**, so an
  evaluation setting cannot drift from what production runs.

## Evaluation outside CI

Quality checks on the AI features run locally against the real model with real
resumes. They are not part of CI, because they cost money, take time and use
private inputs, which stay out of version control.

## Checks that run without anyone asking

- Scheduled CI jobs perform daily account maintenance by calling protected
  internal endpoints.
- A weekly job runs a health check against production using a dedicated test
  account.

## Lessons

- **Green is not the same as correct.** See
  [Green tests, broken production](../incidents/03-green-tests-broken-production.md)
  and [The tests that tested a copy](../incidents/05-the-tests-that-tested-a-copy.md).
- **Read the failure email.** CI was red for three consecutive commits and
  nobody noticed, because the notifications were being ignored.
- **Pin your runtimes.** A frontend test script needed a newer Node version
  than the workflow used, and CI failed until the versions were aligned.
  Local, CI and the host should agree.
- **Do not mock what you do not control.** Build the real object.

## What is not covered

- Page-level code in the job tracker is checked by a live test, not by
  automated ones.
- Two browsers editing at once and real storage-quota failures have not been
  exercised against the real database.
- There is no dedicated error-monitoring service yet. Production errors
  surface in hosting logs and in what users report.
