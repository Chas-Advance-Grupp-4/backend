# CI v3 – Tests, Build, and Docker Push Workflow (Backend)

This document describes the **GitHub Actions workflow** for the backend. It automates tests, builds Docker images, runs health checks, and pushes the images to Docker Hub.

## Purpose

- Automatically run backend tests on pushes to **develop** or **main**.
- Build Docker images for **AMD64** and **ARM64**.
- Test Docker images using the `/health` endpoint before pushing.
- Push multi-architecture Docker images to Docker Hub if tests pass.
- Ensure reproducible environments between local development and CI.

## Workflow Triggers

- **Automatic:** On push to `develop` or `main`.
- **Manual:** Trigger via `workflow_dispatch` in GitHub Actions.

## Workflow Steps

### 1. Check VERSION file
- Checkout repository (`fetch-depth: 0`) to compare with previous commit.
- Check if the `VERSION` file changed.
  - If `version_changed == false`, skip downstream jobs.

### 2. Run Tests
- Checkout repository.
- Setup Python 3.13 environment.
- Install dependencies (`requirements.txt`).
- Run tests using `pytest -v`.
- Only runs if `version_changed == true`.

### 3. Build & Test Docker Images
**AMD64**
- Build image with `--platform linux/amd64`.
- Run health check using `.github/scripts/tests.sh`.

**ARM64**
- Build image with `--platform linux/arm64`.
- Run health check using `.github/scripts/tests.sh`.

### 4. Docker Push – Multi-Arch
- Validate `VERSION`.
- Set `IMAGE_TAG` from `VERSION`.
- Login to Docker Hub (credentials stored in GitHub Secrets).
- Build & push multi-arch image (`--platform linux/amd64,linux/arm64 --push`).
- `develop` tagged with VERSION + `latest`.
- `main` tagged with VERSION.

### 5. Update image version on Azure
- Login to Azure (credentials stored in Github Secrets).
- Update Azure Web App so it runs the latest docker image

## Environment Variables & Secrets

- `TEST_DB_USER`, `TEST_DB_PASSWORD`, `TEST_DB_NAME`, `TEST_DB_PORT` – temporary test database.
- `SECRET_KEY_TEST` – secret key for backend container during tests.
- `DOCKER_HUB_USERNAME` & `DOCKER_HUB_ACCESS_TOKEN` – Docker Hub credentials.
- All secrets are stored in GitHub Actions secrets.

## Best Practices

- Test locally before pushing.
- Keep Python version consistent (3.13).
- Pin dependency versions for reproducibility.
- Keep secrets safe in GitHub Actions.
- Use `/health` endpoint to validate container.
- Merge PR from BOT to update `VERSION` before building.

## Notes

- CI runs on `ubuntu-latest`; behavior may differ from Windows/macOS.
- Multi-arch image ensures AMD64 & ARM64 compatibility.
- Health check uses `/health`.
- Docker images for `develop` and `main` are independent.
- Version number is automatically maintained via the version bump workflow.
