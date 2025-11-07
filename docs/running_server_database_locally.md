### Running the Backend locally (Both server and Database)

**Filenamn:** `docs/running_server_database_locally.md`

# Running the Backend locally via Docker (Both server and database)

This guide explains how to run the backend on your local machine via Docker for development and testing.

## Prerequisites

- Docker installed on your machine.
- Files can be found at [The backend repo](https://github.com/Chas-Advance-Grupp-4/backend) branch running localy
- docker-compose.yml file downloaded and placed in the same folder as the .env file
- db_dump.sql downloaded and placed in the same folder as the .env file
- `.env` file in project root with required environment variables:
S
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

Open a terminal window in the same folder as the files above are located in. 
 
Type in: 
```bash
docker compose up --build
```
To add existing data in database:
Open another terminal window (Not Powershell, Must be a bash terminal!) in the same folder and type: 
```bash
docker compose exec -T database psql -U user -d logistics_db < db_dump.sql 
```
If you add data and want to let other teammates have access to it run: 
```bash
docker compose exec database pg_dump -U user -d logistics_db > db_dump.sql  
```
and share the db_dump.sql file with them. Make shore to save the sql file as UTF-8 by clicking at the encoding in the lower right corner in VSCode and save it as UTF-8, otherwise it will be problematic to enter the data back in the database!

## Stop containers 
```bash
docker compose down
```

Next time you run the containers with docker compose up --build you will have the entered data saved in the volume. You only need to run the pg_dump commands if you want to export or import data from the sql file. 

### Access the API

* URL: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* Health check: [http://localhost:8000/health](http://localhost:8000/health)

Expected response:

```json
{"status": "ok", "message": "API is running"}
```


### Notes

* Multi-arch images work on AMD64 and ARM64.
* Local container is not exposed to the internet via localhost.
* Container is not in reload mode; restart after code changes.
* Use health endpoint to ensure startup is correct.