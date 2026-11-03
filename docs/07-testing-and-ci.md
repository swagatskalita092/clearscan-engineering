# Testing and CI

*How automated tests and deployment relate to the main branch.*

## Automated testing

ClearScan has hundreds of automated tests across the backend and frontend. GitHub Actions runs the backend suite; the frontend tests are not part of CI. Exact current counts live in [STATUS.md](../STATUS.md).

## CI/CD

GitHub Actions runs the backend tests on every push and pull request to main. Production deploys happen automatically from the main branch: the frontend on Netlify and the backend on Railway, which builds the backend from a Dockerfile.
