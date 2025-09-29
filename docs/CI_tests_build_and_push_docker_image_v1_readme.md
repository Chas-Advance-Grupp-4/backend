## CI v1 Tests, build, runs and pushes docker image to Dockerhub – Backend ##  
This document describes the GitHub Actions workflow for the backend, which automates tests, builds Docker images, runs a health check, and pushes the image to Docker Hub.

### Purpose ### 
Runs backend tests automatically on pushes to develop or main.  

Build Docker images for develop (develop-latest) and main (main-latest).  

Test the Docker image with a health check before pushing.  

Push Docker images to Docker Hub if tests and health check pass.  

Ensure consistent and reproducible environments across local development and CI.  

#### Workflow Triggers #### 
Automatic: On push to develop or main.  

Manual: Trigger via workflow_dispatch in GitHub Actions.  

#### Steps ####  
Checkout repository – Fetches code from the current branch.  

Set up Python environment – Installs Python 3.13 using setup-python@v6.  

Install dependencies – Upgrades pip and installs all packages from requirements.txt.  

Run tests – Executes pytest -v to run all backend tests; full output is printed for debugging.  

All tests passed – Prints "All tests passed!" if tests succeed.  

Log in to Docker Hub – Uses GitHub secrets for username and access token.  

Build Docker image – Builds the image and tags it according to the branch:  

develop-latest for the develop branch  

main-latest for the main branch  

Test Docker image with health check – Runs the image in a container, waits for it to be ready, checks /health endpoint, stops and removes container.  

Push Docker image to Docker Hub – Pushes the image if the health check succeeds.  

#### Environment Variables & Secrets ####  
DATABASE_URL – URL to the database. Stored as a GitHub secret.  

DOCKERHUB_USERNAME – Docker Hub username. Stored as a GitHub secret.  

DOCKERHUB_ACCESS_TOKEN – Docker Hub access token. Stored as a GitHub secret.  

#### Best Practices #### 

Test locally first in a virtual environment before pushing.  

Keep Python version consistent between local and CI (3.13).  

Pin dependency versions in requirements.txt for reproducibility.  

Keep secrets (database URL, Docker Hub token) safe in GitHub Actions secrets.  

Use the health check endpoint to validate that the container runs before pushing.  

#### Notes #### 
CI runs on ubuntu-latest; behavior may differ slightly from Windows or macOS.  

Health check uses the /health endpoint.  

Docker images for develop and main are independent and pushed with different tags.  

Versions numbers will be implemented later on, for now, *-latest tags are used.  