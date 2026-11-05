# Security and privacy

*What is protected, what third parties see, and what this page does not
claim.*

A resume is personal data. These are the practices ClearScan follows. They are
practices, not a certification.

## Where data lives

- Accounts and data are stored in an EU-region database, in Frankfurt.
- Data is encrypted in transit.
- Row-level access control limits what a signed-in user's requests can reach.
- Authentication is handled by a managed service rather than custom code.

## What the browser holds

Only public keys. Every secret stays on the API.

## Who sees a user's text

- **A language model provider** receives the resume and posting text, and only
  when a user invokes one of the two text features. The core score is computed
  inside ClearScan's own backend and does not go to a model provider.
- **An email provider** receives the address of the person being emailed.

## Data on the device

The job tracker keeps a copy on the user's device so it keeps working
offline. That copy is removed when the user signs out.

## Development hygiene

Real resumes used to evaluate the AI features stay on the developer's
machine and out of version control. This repository contains no customer
information, uploaded resumes, credentials, private source code or unredacted
logs.

## What this page does not claim

It does not claim a certification or a third-party audit. Personal data is
handled with the principles of the GDPR in mind, but this page is not a
statement of legal compliance.

## Reporting a concern

Use the contact details on [clearscan.fyi](https://clearscan.fyi). Please do
not post security problems in public issues.
