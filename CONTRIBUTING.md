# Contributing

*This repository is open to contributions. The ClearScan product source is
not.*

This repository is documentation: field notes about building and running an
ATS resume scanner. Contributions here improve those notes. The product's
source code is private and is not available.

## What is welcome

- **Corrections.** A wrong fact, a broken link or an outdated statement. Open a
  correction issue, or send a small pull request.
- **Your own incident or design lesson.** If you built something similar and
  something broke, the incident template is for you. The best stories may be
  linked from this repository.
- **Improvements to the build-your-own guide**, especially measured results
  from your own system.
- **Questions about the design**, in Discussions.

## What is not accepted

- Requests for weights, thresholds, dictionaries, prompts or any other
  constant. They are deliberately unpublished, and such requests will be closed
  without discussion.
- Instructions for gaming ClearScan or any other scanner.
- Promotion of products or services.
- Customer data, real resumes, credentials or logs.
- Code for ClearScan itself. It is private.

## What to expect

This repository is maintained independently, alongside other commitments.
Replies can take days or weeks. Nobody is owed a response, and nothing is lost
by waiting.

## Pull requests

- Keep each pull request to one change. For anything larger than a correction,
  open an issue first.
- Write plainly and specifically. Avoid marketing language.
- Figures that change over time belong only in [STATUS.md](STATUS.md). Elsewhere
  use durable wording.
- State limits honestly. If something is unmeasured, say so.
- Run `python scripts/check_docs.py` before you open the pull request. The same
  check runs automatically on every pull request. It looks for broken links,
  secrets, em dashes, money amounts and sales wording, and first person, and it
  keeps the scoring and anti-gaming pages free of figures.

## Licensing

By contributing, you agree that your contribution is licensed under
[CC BY 4.0](LICENSE), like the rest of the writing here. Your name stays in the
git history.

## Conduct and security

Please read the [code of conduct](CODE_OF_CONDUCT.md). Report security
concerns as described in the [security policy](SECURITY.md), not in public
issues.
