#!/bin/bash

#.github/scripts/tests.sh
set -e

# Argument 1 = image name
IMAGE_NAME=$1

# Clean up containers och nätverk oavsett vad som händer
trap 'docker stop backend_test ci_postgres || true; \
      docker rm backend_test ci_postgres || true; \
      docker network rm ci_network || true' EXIT

# Skapa nätverk
docker network create ci_network||true

# Starta tillfällig Postgres container
docker run -d --name ci_postgres --network ci_network \
  -e POSTGRES_USER="${TEST_DB_USER}" \
  -e POSTGRES_PASSWORD="${TEST_DB_PASSWORD}" \
  -e POSTGRES_DB="${TEST_DB_NAME}" \
  -p "${TEST_DB_PORT}":5432 \
  postgres:15

# Vänta tills Postgres är redo
until docker exec ci_postgres pg_isready -U "${TEST_DB_USER}" -d "${TEST_DB_NAME}"; do
  echo "Waiting for Postgres..."
  sleep 2
done

# Installera jq för JSON-parsing
sudo apt-get update && sudo apt-get install -y jq

# Starta backend container
docker run -d --name backend_test --network ci_network -p 8000:8000 \
  -e DATABASE_URL="postgresql+psycopg://${TEST_DB_USER}:${TEST_DB_PASSWORD}@ci_postgres:5432/${TEST_DB_NAME}" \
  -e SECRET_KEY="${SECRET_KEY_TEST}" \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=30 \
  $IMAGE_NAME

# Vänta lite
sleep 5

# Health check
HEALTH_CHECK_PASSED=false
for i in {1..10}; do
  RESPONSE=$(curl -s http://localhost:8000/health)
  if echo "$RESPONSE" | jq -e '.status=="ok"' > /dev/null; then
    echo "Health check passed!"
    HEALTH_CHECK_PASSED=true
    break
  else
    echo "Waiting for the container to start..."
    sleep 5
  fi
done

if [ "$HEALTH_CHECK_PASSED" = false ]; then
  echo "Health check failed after 10 attempts"
  exit 1
fi