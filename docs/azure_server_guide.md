
---

````markdown
# Azure Backend Server Guide – Team 4

This document explains how our **FastAPI backend** is deployed and managed in **Azure App Service** using **Docker containers**.  
It includes how to run, update, and troubleshoot the development server.

---

## Requirements

To manage the server, make sure you have:

- **Azure CLI** installed  
  [Install guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)  
- Access to our **Azure subscription**  
- **Docker Hub** credentials for `chasadvancegroup4`  
- Access to:

  - **Resource group:** `team_4`  
  - **Web App name:** `grupp4AWA`  

Login to Azure:

```bash
az login
az account set --subscription "Chas Academy Team 4"
````

---

## How the Server Works

We deploy our FastAPI backend as a **Docker container**.
The container image is hosted on **Docker Hub**, and Azure automatically pulls and runs it.

### Architecture

```
Docker Hub → Azure App Service (Web App for Containers) → FastAPI (via Uvicorn)
```

### Startup Command (set in Azure)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Azure listens to port **8000** automatically due to:

```
WEBSITES_PORT=8000
```

---

## Continuous Deployment (CD)

We have **Continuous Deployment** enabled between **Docker Hub** and **Azure**:

* Whenever a new image is pushed to Docker Hub (same tag, e.g., `latest`)
* → Azure automatically pulls the image and restarts the container.

Currently, `latest` is used for development. Production will use specific version tags.

---

## Manual Commands

### Restart the app

```bash
az webapp restart -g team_4 -n grupp4AWA
```

### Stream logs

```bash
az webapp log tail -g team_4 -n grupp4AWA
```

### Check running image

```bash
az webapp config container show -g team_4 -n grupp4AWA
```

---

## Environment Variables

List all app settings:

```bash
az webapp config appsettings list -g team_4 -n grupp4AWA
```

Set or update variables:

```bash
az webapp config appsettings set \
  -g team_4 \
  -n grupp4AWA \
  --settings DATABASE_URL=postgresql+psycopg://user:password@server:5432/dbname
```

Common variables:

| Variable       | Description                     |
| -------------- | ------------------------------- |
| `DATABASE_URL` | Connection string to PostgreSQL |
| `FRONTEND_URL` | Frontend base URL               |
| `ENV`          | `development` or `production`   |

---

## Server Runtime Guidelines

| Situation                     | Action                                        |
| ----------------------------- | --------------------------------------------- |
| Push a new Docker image       | Nothing – Azure redeploys automatically       |
| App doesn’t update after push | Run `az webapp restart`                       |
| Test a different version      | Change image tag in Azure or push another tag |
| Stop temporarily              | Use “Stop” button in Azure Portal             |

> Treat Azure as a “always-on dev server.” Push images → Azure handles deployment.

---

## Security

Azure automatically manages:

* HTTPS certificates and SSL renewal
* Load balancing
* Port exposure (`8000`)
* Isolation between apps

No need for manual Nginx or SSL setup.

---

## Health Check

Verify the API is live:

```bash
curl https://grupp4awa.azurewebsites.net/health
```

Expected response:

```json
{"status": "ok", "message": "API is running"}
```

---

```

---
