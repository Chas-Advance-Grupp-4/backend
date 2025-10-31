
---

```markdown
# CI/CD Pipeline – Backend

This document describes the **GitHub Actions CI/CD workflow** for the Chas Advance backend.  
The pipeline automates tests, Docker image builds, health checks, and deployment to Docker Hub and Azure.

---

## Purpose

- Run backend tests automatically on pushes to **develop** or **main**.  
- Build Docker images for **AMD64** and **ARM64** architectures.  
- Test Docker images using a health check before pushing.  
- Push multi-architecture Docker images to Docker Hub if tests pass.  
- Ensure consistent and reproducible environments between local development and CI.

---

## Workflow Triggers

- **Automatic:** On push to `develop` or `main`  
- **Manual:** Trigger via `workflow_dispatch` in GitHub Actions  

---

## Steps Overview

### 1. Check if VERSION file changed
- Checkout repository (fetch all history)  
- Check if `VERSION` file was modified in the last commit  
- Skip downstream jobs if no version change

### 2. Tests
- Checkout repository  
- Set up Python environment (Python 3.13)  
- Install dependencies (`requirements.txt`)  
- Run tests using `pytest`  
- Only continue if all tests pass and version change detected

### 3. Docker Build & Test
- **AMD64**:
  - Build Docker image (`docker buildx --platform linux/amd64`)  
  - Run health check (`/health` endpoint)
- **ARM64**:
  - Build Docker image (`docker buildx --platform linux/arm64`)  
  - Run health check

### 4. Docker Push
- Login to Docker Hub (using GitHub secrets)  
- Push multi-architecture Docker image to Docker Hub  
- Tag images according to `VERSION` file  
- `develop` branch → tagged with version and `latest`  
- `main` branch → tagged with version only

---

## Environment Variables & Secrets

- **TEST_DB_USER**, **TEST_DB_PASSWORD**, **TEST_DB_NAME**, **TEST_DB_PORT** – for test database  
- **SECRET_KEY_TEST** – secret key for tests  
- **DOCKER_HUB_USERNAME** & **DOCKER_HUB_ACCESS_TOKEN** – Docker Hub credentials  
- All secrets are stored in GitHub Actions secrets

---

## Best Practices

- Test locally in a virtual environment before pushing  
- Keep Python version consistent between local and CI (3.13)  
- Pin dependency versions for reproducibility  
- Use health check endpoint to validate container before push  
- Merge PRs that update the `VERSION` file to ensure correct Docker tagging

---

## Notes

- CI runs on `ubuntu-latest`; behavior may differ on Windows or macOS  
- Multi-arch image ensures compatibility for both AMD64 and ARM64  
- Docker images for `develop` and `main` are independent and pushed with separate tags  
```

---
