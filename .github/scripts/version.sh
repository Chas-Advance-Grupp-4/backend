#!/bin/bash
set -e

# Hämta branch name
BRANCH=${GITHUB_REF##*/}

# Hämta befintliga tags
TAGS=$(git ls-remote --tags origin | awk -F/ '{print $3}' | sort -V)

# Debug output
echo "Branch: $BRANCH"
echo "Available tags: $TAGS"

# Filtrera tags
MAIN_TAGS=$(echo "$TAGS" | grep -E '^[0-9]+\.0$' || true)
DEVELOP_TAGS=$(echo "$TAGS" | grep -E '^[0-9]+\.[0-9]+$' || true)

# Hitta senaste main version
LAST_MAIN=$(echo "$MAIN_TAGS" | sort -V | tail -n1)
if [ -z "$LAST_MAIN" ]; then
  LAST_MAIN=1
else
  LAST_MAIN=${LAST_MAIN%%.*}
fi

# Bestäm nästa version
if [ "$BRANCH" == "main" ]; then
  NEXT_MAJOR=$((LAST_MAIN + 1))
  IMAGE_TAG="${NEXT_MAJOR}.0"
elif [ "$BRANCH" == "develop" ]; then
  LAST_DEV=$(echo "$DEVELOP_TAGS" | grep "^$LAST_MAIN\." | sort -V | tail -n1)
  if [ -n "$LAST_DEV" ]; then
    MINOR=$(echo "$LAST_DEV" | cut -d. -f2)
    NEXT_MINOR=$((MINOR + 1))
  else
    NEXT_MINOR=1
  fi
  IMAGE_TAG="${LAST_MAIN}.${NEXT_MINOR}"
elif [ "$BRANCH" == "77-7126-refactor-workflow-that-publishes-docker-image" ]; then
  LAST_DEV=$(echo "$DEVELOP_TAGS" | grep "^$LAST_MAIN\." | sort -V | tail -n1)
  if [ -n "$LAST_DEV" ]; then
    MINOR=$(echo "$LAST_DEV" | cut -d. -f2)
    NEXT_MINOR=$((MINOR + 1))
  else
    NEXT_MINOR=1
  fi
  IMAGE_TAG="${LAST_MAIN}.${NEXT_MINOR}"
else
  IMAGE_TAG="latest"
fi

echo "Generated version: $IMAGE_TAG"

# Sätt output för GitHub Actions
if [ -n "$GITHUB_ENV" ]; then
  echo "IMAGE_TAG=$IMAGE_TAG" >> $GITHUB_ENV
fi

# Output för lokala tester
echo "$IMAGE_TAG"