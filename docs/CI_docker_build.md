# CI v3 – Tests, Docker Build & Push Workflow (Backend)

This document describes the **detailed GitHub Actions workflow** for building, testing, and pushing Docker images.

---

## Steps

### 1. Check VERSION file
- Checkout repository with full history (`fetch-depth: 0`)  
- Check if `VERSION` changed  
- Skip downstream jobs if `version_changed == false`

### 2. Run Tests
- Checkout repository  
- Setup Python 3.13 environment  
- Install dependencies (`requirements.txt`)  
- Run tests with `pytest -v`  
- Continue only if tests pass and version changed

### 3. Docker Build & Test
**AMD64**
- Build image: `docker buildx --platform linux/amd64`  
- Run health check: `.github/scripts/tests.sh`  

**ARM64**
- Build image: `docker buildx --platform linux/arm64`  
- Run health check

### 4. Docker Push – Multi-Arch
- Validate `VERSION`  
- Set `IMAGE_TAG` from `VERSION`  
- Login to Docker Hub (GitHub Secrets)  
- Build & push multi-arch image: `--platform linux/amd64,linux/arm64 --push`  
- `develop` → tag with VERSION + `latest`  
- `main` → tag with VERSION only

### 5. Update Azure
- Login to Azure (Secrets stored in GitHub Actions)  
- Update Azure Web App to run the latest Docker image

---

## Environment Variables & Secrets

- `TEST_DB_USER`, `TEST_DB_PASSWORD`, `TEST_DB_NAME`, `TEST_DB_PORT` – test database  
- `SECRET_KEY_TEST` – secret for container during tests  
- `DOCKER_HUB_USERNAME` & `DOCKER_HUB_ACCESS_TOKEN` – Docker Hub credentials  

All secrets are stored in GitHub Actions secrets.

---

## Best Practices

- Test locally in a virtual environment before pushing  
- Keep Python version consistent (3.13)  
- Pin dependency versions for reproducibility  
- Use `/health` endpoint to validate container  
- Merge PRs that update `VERSION` before building  

---

## Notes

- CI runs on `ubuntu-latest`; may differ from Windows/macOS  
- Multi-arch images ensure AMD64 & ARM64 compatibility  
- Docker images for `develop` and `main` are independent  
- Version number is automatically maintained via the version bump workflow
