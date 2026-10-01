# Testing and CI/CD

## Automated testing

ClearScan has 170+ automated tests with a current reported pass rate of 100%.

## CI/CD

GitHub Actions runs the automated tests on every push and pull request to main. Production deploys happen automatically from the main branch: the frontend on Netlify and the backend on Railway, which builds the backend from a Dockerfile. ClearScan has made 220+ commits to production since July 2026.
