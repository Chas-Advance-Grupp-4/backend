# Azure Backend Server Guide — Team 4

## Overview

This document explains how our **FastAPI backend** is deployed and managed in **Azure App Service** using **Docker containers**.
It includes how to run, update, and troubleshoot the development server.

---

## Requirements

To manage the server, make sure you have:

* **Azure CLI** installed
     [Install guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
* Access to our **Azure subscription**
* **Docker Hub** credentials for `chasadvancegroup4`
* Access to:

  * **Resource group:** `team_4`
  * **Web App name:** `grupp4AWA`

Login once in Azure:

```bash
az login
az account set --subscription "Chas Academy Team 4"
```

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

Azure listens to port **8000** automatically because of:

```
WEBSITES_PORT=8000
```

---

## Continuous Deployment (CD)

We have **Continuous Deployment** enabled between **Docker Hub** and **Azure**.

That means:

* Whenever a new image is pushed to Docker Hub with the same tag (e.g.,`2.1`,`latest`)
* → Azure automatically pulls that image and restarts the container.
* We are currently using the latest tag, but when we move to production we will use the correct version


---

## Manual Commands

If you need to control the app manually from your terminal:

### Restart the app

```bash
az webapp restart -g team_4 -n grupp4AWA
```

### Stream logs

```bash
az webapp log tail -g team_4 -n grupp4AWA
```

### Check which image is currently running

```bash
az webapp config container show -g team_4 -n grupp4AWA
```

---

## 🧱 Environment Variables

To **list** all app settings:

```bash
az webapp config appsettings list -g team_4 -n grupp4AWA
```

To **set or update** a variable:

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
| `FRONTEND_URL` | Used for environment logic      |
| `ENV`          | `development` or `production`   |

---

## 🧭 Server Runtime Guidelines

Azure App Service is designed to **keep your app running continuously**.
You normally don’t need to start or stop it manually — it automatically handles restarts, scaling, and deployment updates.

Here’s how to handle it in our workflow:

| Situation                                 | What to Do                                             | Notes                                                      |
| ----------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------- |
| You push a new Docker image to Docker Hub |  Nothing more to do                                   | Azure automatically redeploys                              |
| The app doesn’t update after a push       |  Run `az webapp restart`                             | Forces container reload                                    |
| You need to test a different version      |  Change image tag in Azure or push under another tag | Good for staging/testing                                   |
| You’re done with testing                  |  Leave it running                                    | Azure pauses inactive apps automatically (no cost for CPU) |
| You need to stop it temporarily           |  Use the “Stop” button in the Azure Portal           | Not required during normal dev                             |

**Summary:**

> Treat Azure as a “always-on dev server.”
> Just push new images — Azure will handle uptime, HTTPS, and automatic restarts.

---

##  Security

Azure automatically manages:

* HTTPS certificates and SSL renewal
* Load balancing
* Port exposure (`8000` only)
* Isolation between apps

You don’t need to set up Nginx or handle certificates manually — it’s all managed by Azure App Service.

---

## Useful Health Check

To verify the API is live:

```bash
curl https://grupp4awa.azurewebsites.net/health
```

Expected response:

```json
{"status": "ok", "message": "API is running"}
```

---

**In short:**

> Build → Push to Docker Hub → Azure auto-deploys → App restarts → Ready to test.
