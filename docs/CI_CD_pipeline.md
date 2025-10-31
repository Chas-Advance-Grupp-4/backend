# CI/CD Pipeline – Backend

This document describes the **GitHub Actions CI/CD workflow** for the Chas Advance backend.  
It provides an overview of the full pipeline, from tests to deployment.

---

## Purpose

- Automate backend tests on pushes to **develop** or **main**  
- Build Docker images for **AMD64** and **ARM64** architectures  
- Run health checks on Docker images  
- Push multi-arch images to Docker Hub  
- Deploy the latest image to Azure  
- Ensure consistent and reproducible environments

---

## Workflow Triggers

- **Automatic:** On push to `develop` or `main`  
- **Manual:** Trigger via `workflow_dispatch` in GitHub Actions  

---

## Pipeline Overview

1. **Check VERSION file** – Skip steps if no change  
2. **Run Tests** – Unit and integration tests using pytest  
3. **Docker Build & Test** – Build AMD64/ARM64 images and run health checks  
4. **Docker Push** – Push multi-arch images to Docker Hub  
5. **Azure Deployment** – Update the Azure Web App to use the latest image

> For detailed step-by-step instructions, see `CI_docker_build.md`
