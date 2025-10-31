
---

### 1️⃣ CI v3 / Docker Build Workflow

**Filenamn:** `docs/ci_docker_build.md`

```markdown
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
```

---

### 2️⃣ Running the Backend Docker Container Locally

**Filenamn:** `docs/running_backend_locally.md`

````markdown
# Running the Backend Docker Container Locally

This guide explains how to run the backend Docker container on your local machine for development and testing.

## Prerequisites

- Docker installed on your machine.
- `.env` file in project root with required environment variables:

```text
DATABASE_URL=<your-database-url>
SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV=development
FRONTEND_URL=<frontend-url>
````

> Do not commit `.env` to GitHub. Keep it local or use secrets.

## Running the Container

Each image is tagged with a semantic version (e.g., 1.2, 2.0) from the `VERSION` file.

### Latest Develop Build

```bash
docker run -d \
  --name backend_local \
  -p 8000:8000 \
  --env-file .env \
  chasadvancegroup4/chas_advance_backend:<develop-version>
```

### Latest Main Build

```bash
docker run -d \
  --name backend_local \
  -p 8000:8000 \
  --env-file .env \
  chasadvancegroup4/chas_advance_backend:<main-version>
```

### Tips

* `-d` → run in detached mode.
* `--name backend_local` → container name for easy reference.
* `-p 8000:8000` → map container port to host port.
* `--env-file .env` → provide environment variables.

### Check Version

```bash
docker run --rm --env-file .env chasadvancegroup4/chas_advance_backend:latest --version
docker logs backend_local  # in detached mode
```

### Access the API

* URL: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health check: [http://localhost:8000/health](http://localhost:8000/health)

Expected response:

```json
{"status": "ok", "message": "API is running"}
```

### Stop & Remove Container

```bash
docker stop backend_local
docker rm backend_local
```

### Notes

* Multi-arch images work on AMD64 and ARM64.
* Local container is not exposed to the internet via localhost.
* Container is not in reload mode; restart after code changes.
* Use health endpoint to ensure startup is correct.


