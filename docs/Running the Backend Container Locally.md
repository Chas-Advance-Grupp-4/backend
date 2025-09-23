## Running the Backend Docker Container Locally ##
This guide explains how to run the backend Docker container on your local machine for development and testing purposes.  

### Prerequisites ###  

Docker installed on your machine.  

.env file in your project root with the necessary environment variables:  

DATABASE_URL=<your-database-url>  
SECRET_KEY=<your-secret-key>  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
ENV=development   
FRONTEND_URL=<frontend-url>    

Note: Do not commit your .env file to GitHub. Keep it local or use secrets.  

### Building the Docker Image ### 

From the project root, run:  
for develop image with latest updates:  
docker build -t annaschwartzchas/chas_advance_backend:develop-latest .  
for main image with latest stable version: 
docker build -t annaschwartzchas/chas_advance_backend:main-latest .    

### Running the Container ### 

Use the following command to start the container locally:   

for develop image:   
docker run -d \
  --name backend_local \
  -p 8000:8000 \
  --env-file .env \
  annaschwartzchas/chas_advance_backend:develop-latest

for main image:  
  docker run -d \
  --name backend_local \
  -p 8000:8000 \
  --env-file .env \
  annaschwartzchas/chas_advance_backend:main-latest

-d runs the container in detached mode.

--name backend_local names your container for easy reference.

-p 8000:8000 maps port 8000 in the container to port 8000 on your host.

--env-file .env passes environment variables from your local .env file.

### Accessing the API### 

Open your browser or use a tool like curl or Postman to access the API:
http://localhost:8000  

Swagger UI documentation is available at:  
http://localhost:8000/docs  

Health check endpoint:
http://localhost:8000/health
Should return:

{"status": "ok", "message": "API is running"}

### Stopping the Container ### 

When finished, stop and remove the container:

docker stop backend_local
docker rm backend_local

### Notes ### 

Running the container locally does not expose your backend to the internet as long as you access it via localhost.

Ensure your .env has correct database and secret credentials for local development.

Use the health endpoint to verify the container started correctly.

The container is not runned in reload mode, which means you have to restart the container if you make changes in the code. 