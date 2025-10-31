
---

````markdown
# Local Installation – Backend

This guide explains how to set up and run the **Chas Advance backend** locally for development or testing.

---

## Prerequisites

Make sure you have installed:

- Python 3.11+  
- Docker (for containerized setup)  
- Git  

Optional but recommended:

- `virtualenv` for isolated Python environments  

---

## Clone Repository

```bash
git clone https://github.com/<your-org>/ChasAdvance_new.git
cd ChasAdvance_new
````

---

## Python Virtual Environment Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment file and configure variables:

```bash
cp .env.example .env
```

Make sure to update `.env` with your local database credentials and secret keys.

---

## Database Setup

1. Run migrations:

```bash
alembic upgrade head
```

2. Ensure the database is running and accessible according to your `.env` configuration.

---

## Running Backend Locally with Python

```bash
uvicorn app.main:app --reload
```

API will be available at [http://localhost:8000](http://localhost:8000).

---

## Running Backend Locally with Docker

Pull the latest dev image:

```bash
docker pull chasadvancegroup4/chas_advance_backend:dev
```

Run the container:

```bash
docker run -d \
  --name backend_local \
  -p 8000:8000 \
  --env-file .env \
  chasadvancegroup4/chas_advance_backend:dev
```

Stop and remove the container when done:

```bash
docker stop backend_local
docker rm backend_local
```

---

## Testing

Run all tests locally:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Notes

* Multi-architecture Docker images work on AMD64 or ARM64 without rebuilding.
* The `.env` file should never be committed to GitHub.
* If you make code changes, you need to restart the Docker container unless running via `uvicorn --reload`.



