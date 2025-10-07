## CI v1 Tests, build, runs and pushes docker image to Dockerhub – Backend ##  
This document describes the GitHub Actions workflow for the backend, which automates tests, builds Docker images, runs a health check, and pushes the image to Docker Hub.

### Purpose ### 
Runs backend tests automatically on pushes to develop or main.  

Build Docker images for both AMD64 and ARM64 for health testing.  

Test the Docker images with a health check before pushing.  

Push  multi-architecture Docker images to Docker Hub if tests and health checks passes.  

Ensure consistent and reproducible environments across local development and CI.  

#### Workflow Triggers #### 
Automatic: On push to develop or main.  

Manual: Trigger via workflow_dispatch in GitHub Actions.  

#### Steps ####  
1. Tests
Checkout repository – Fetches code from the current branch.  

Set up Python environment – Installs Python 3.13 using setup-python@v6.  

Install dependencies – Upgrades pip and installs all packages from requirements.txt.  

Run tests – Executes pytest -v to run all backend tests; full output is printed for debugging.  

All tests passed – Prints "All tests passed!" if tests succeed.  

2. Docker - builds and Tests docker images
Checkout repository

Build AMD64 Docker image for testing
Builds an AMD64 image tagged as backend_test_amd64 using docker buildx --platform linux/amd64.

Test Docker image
Runs a health check test using .github/scripts/tests.sh with the AMD64 image. Checks /health endpoint.

Build ARM64 Docker image for testing:
Builds an ARM64 image tagged as backend_test_arm64 using docker buildx --platform linux/arm64.

Test Docker image
Runs .github/scripts/tests.sh with the ARM64 image to ensure it starts and /health endpoint responds.

3. Docker Push - Build & Push Multi-arch Docker image 
   
Checkout Repository

Determine next Docker tag

Set Docker image tag
Reads VERSION file, increases minor version for develop and major version for main, eg:
main 1.0, 2.0, ...
develop 1.1, 1.2, ... 

Log in to Docker Hub 
Uses GitHub secrets for username and access token.  

Build and Push multi-architecture Docker image to Docker Hub  
Uses docker buildx build --platform linux/amd64,linux/arm64 --push to push a single multi-arch image to Docker Hub.
develop gets taged with accurate VERSION number and a latest tag
main gets tagged with accurate VERSION number. Uses --build arg VERSION=${IMAGE_TAG} to set correct version in docker-image and present it when container starts.

#### Environment Variables & Secrets ####  
TEST_DB_USER, TEST_DB_PASSWORD, TEST_DB_NAME, TEST_DB_PORT: Used by the test script to configure the temporary Postgres database.

SECRET_KEY_TEST: Secret key used in the backend container during tests.

DOCKER_HUB_USERNAME & DOCKER_HUB_ACCESS_TOKEN: Docker Hub credentials for login and push.

All secrets are stored in GitHub Actions secrets. 

#### Best Practices #### 

Test locally first in a virtual environment before pushing.  

Keep Python version consistent between local and CI (3.13).  

Pin dependency versions in requirements.txt for reproducibility.  

Keep secrets (database credentials, Docker Hub token) safe in GitHub Actions secrets.  

Use the health check endpoint to validate that the container runs before pushing.  

Version handling is maintained manually via the VERSION file, remember to update that file after push to develop or main! 

#### Notes #### 
CI runs on ubuntu-latest; behavior may differ slightly from Windows or macOS.  

Multi-arch image ensures compatibility for both AMD64 and ARM64 platforms.

Health check uses the /health endpoint.  

Docker images for develop and main are independent and pushed with different tags.  

Docker images for develop and main is pushed with different tags (1.1, 1.2, ... and 2.0, 3.0, ...)

Version number in docker image is maintained MANUALLY in VERSIONFILE, and the latest image number should be entered in the file after push to docker hub. Just replace the exisiting number with the new. The version number is used when the container is build and makes shore you know what version you are running by presenting it at container start. 