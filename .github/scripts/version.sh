#!/bin/bash
set -e

echo "Running version validation and tag generation..."

BRANCH=${GITHUB_REF##*/}

# Read the VERSION file, default to "0.0" if not found
VERSION=$(cat VERSION 2>/dev/null || echo "0.0")

# Control that VERSION is in correct format, e.g. 1.0, 2.1 etc
if ! echo "$VERSION" | grep -qE '^[0-9]+\.[0-9]+$'; then
  echo "ERROR: VERSION must be in format 'major.minor' (e.g. '1.1', '2.0')."
  echo "Current value: $VERSION"
  exit 1
fi

# Fetch the commit before to compare against
BASE_VERSION=$(git show HEAD~1:VERSION 2>/dev/null || echo "none")

echo "Branch: $BRANCH"
echo "Base VERSION: $BASE_VERSION"
echo "New VERSION:  $VERSION"

# If no previous version found, allow initial version
if [ "$BASE_VERSION" = "none" ]; then
  echo "No previous VERSION found on $BRANCH — allowing initial version."
else
  # Split up version numbers into major and minor parts
  BASE_MAJOR=${BASE_VERSION%%.*}
  BASE_MINOR=${BASE_VERSION##*.}
  HEAD_MAJOR=${VERSION%%.*}
  HEAD_MINOR=${VERSION##*.}

  #Check that Current Version is bigger than earlier(Base) Version
  if [ "$HEAD_MAJOR" -lt "$BASE_MAJOR" ] || { [ "$HEAD_MAJOR" -eq "$BASE_MAJOR" ] && [ "$HEAD_MINOR" -le "$BASE_MINOR" ]; }; then
    echo "ERROR: VERSION must be greater than previous version ($BASE_VERSION)."
    exit 1
  fi
fi

echo "VERSION is valid and newer than previous!"

if [ "$BRANCH" == "main" ]; then
    
    IMAGE_TAG="${HEAD_MAJOR}.0"
elif [ "$BRANCH" == "develop" ]; then
    IMAGE_TAG="${HEAD_MAJOR}.${HEAD_MINOR}"
else
    IMAGE_TAG="latest"
fi

echo "IMAGE_TAG=$IMAGE_TAG" >> $GITHUB_ENV
echo "Next Docker tag: $IMAGE_TAG"

