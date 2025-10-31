
```markdown
# Chas Advance – Backend

This repository contains the **backend service** for **Chas Advance**, a logistics platform enabling climate-controlled and fully traceable delivery of specialized goods.  
The backend handles data management, authentication, sensor communication, vehicle integration, and provides REST APIs for both the frontend and IoT systems.

---

## Repository Structure (Top-Level)

```

.
├── alembic.ini
├── app/                     # FastAPI application
├── Dockerfile
├── docs/                    # Documentation and guides
├── requirements.txt
├── tests/                   # Unit and integration tests
├── VERSION                  # Project version file
└── readme.md

````

> For a detailed file structure, see `app/` and `tests/` folders.

---

## Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI + Uvicorn
- **Database:** PostgreSQL (Azure SQL in production)
- **ORM & Migrations:** SQLAlchemy + Alembic
- **Authentication:** JWT (PyJWT), Passlib + Bcrypt
- **Rate Limiting:** SlowAPI
- **Testing:** Pytest + pytest-asyncio + pytest-cov
- **Linting & Formatting:** Flake8 + Black
- **Containerization:** Docker
- **Hosting:** Azure Web App via App Service
- **CI/CD:** GitHub Actions
- **Monitoring & Observability:** Azure Monitor + Application Insights
- **Documentation:** Docstrings + Doxygen

---

## Docker Images

We maintain **latest dev and main images** on Docker Hub:

- Repository: [chasadvancegroup4/chas_advance_backend](https://hub.docker.com/repository/docker/chasadvancegroup4/chas_advance_backend/general)

```bash
# Pull latest dev image
docker pull chasadvancegroup4/chas_advance_backend:dev

# Pull latest main image
docker pull chasadvancegroup4/chas_advance_backend:main
````

---

## Documentation Overview

Detailed documentation is stored in the [`docs/`](docs/) folder:

| Doc File | Description |
| -------- | ----------- |
| [`install.md`](docs/install.md) | Installation instructions for local dev |
| [`running_backend_locally.md`](docs/running_backend_locally.md) | Running the backend Docker container locally |
| [`azure_server_guide.md`](docs/azure_server_guide.md) | Azure App Service deployment and server guide |
| [`CI_tests.md`](docs/CI_tests.md) | CI workflow for running backend tests |
| [`CI_docker_build.md`](docs/CI_docker_build.md) | CI workflow for building and pushing Docker images |
| [`CI_version_bump.md`](docs/CI_version_bump.md) | CI workflow for automatic version bumping |
| [`CI_CD_pipeline.md`](docs/CI_CD_pipeline.md) | Overview of full CI/CD pipeline from test to deployment |

> Open these files for step-by-step instructions, commands, and best practices.


---

## API Documentation

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Contributors

**Backend Team – Chas Advance**

* [Fredrik Rappich](https://github.com/Rappich) – Backend Developer
* [Anna Schwartz](https://github.com/AnnaSchwartzChas) – Backend Developer

---

## Future Improvements

* Expand logging and metrics for better observability.
* Optimize database queries and connection pooling.
* Increase unit and integration test coverage.
* Improve CI/CD with automated rollback for failed deployments.
* Extend docstrings and Doxygen comments for all services and models.
* Introduce stricter rate limiting and advanced authentication flows.
* Introduce environment-specific configs for staging and production.

```

---
