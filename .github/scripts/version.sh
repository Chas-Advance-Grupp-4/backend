#!/bin/bash
set -e

# Hämta branch name
BRANCH=${GITHUB_REF##*/}

# Hämta befintliga tags
VERSION=$(cat VERSION || echo "1.0")

# Dela upp major och minor
MAJOR=${VERSION%%.*}
MINOR=${VERSION##*.}

if [ "$BRANCH" == "main" ]; then
    # Huvudrelease, major ökar med 1
    NEXT_MAJOR=$((MAJOR + 1))
    IMAGE_TAG="${NEXT_MAJOR}.0"
elif [ "$BRANCH" == "develop" ]; then
    # Minor ökar med 1
    NEXT_MINOR=$((MINOR + 1))
    IMAGE_TAG="${MAJOR}.${NEXT_MINOR}"
else
    IMAGE_TAG="latest"
fi

echo "IMAGE_TAG=$IMAGE_TAG" >> $GITHUB_ENV
echo "Next Docker tag: $IMAGE_TAG"

