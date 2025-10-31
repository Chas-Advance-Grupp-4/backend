### Running the Backend Docker Container Locally

**Filenamn:** `docs/running_backend_locally.md`

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
CONTROL_UNIT_SECRET_KEY=<your-secret-key-for-control-unit>
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


