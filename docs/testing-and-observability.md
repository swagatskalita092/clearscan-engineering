# Testing and CI/CD

## Automated testing

ClearScan has 238 automated tests (215 backend, 23 frontend). A local run on 2026-10-22 passed all of them. GitHub Actions runs the backend suite; the frontend tests are not part of CI.

## CI/CD

GitHub Actions runs the backend tests on every push and pull request to main. Production deploys happen automatically from the main branch: the frontend on Netlify and the backend on Railway, which builds the backend from a Dockerfile. ClearScan has 500+ commits on main since April 2026.
