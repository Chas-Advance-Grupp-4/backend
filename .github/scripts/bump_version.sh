#!/bin/bash
set -e

###############################################################################
## @file bump_version.sh
## @brief Automatically increments the VERSION file based on the current branch.
##
## Branch rules:
## - main: increment major version (e.g., 1.0 → 2.0)
## - develop: increment minor version (e.g., 1.0 → 1.1)
## - other branches: no version bump
##
## @usage ./bump_version.sh
## @dependencies git, bash
## @author Anna Schwartz
## @date 2025-10-17
###############################################################################


BRANCH=${GITHUB_REF##*/}

VERSION=$(cat VERSION 2>/dev/null || echo "0.0")

BASE_VERSION=$(git show HEAD~1:VERSION 2>/dev/null || echo "0.0")

BASE_MAJOR=${BASE_VERSION%%.*}
BASE_MINOR=${BASE_VERSION##*.}
HEAD_MAJOR=${VERSION%%.*}
HEAD_MINOR=${VERSION##*.}

if [ "$BRANCH" = "main" ]; then 
    NEW_VERSION="$((HEAD_MAJOR+1)).0"
elif [ "$BRANCH" = "develop" ]; then
    NEW_VERSION="$HEAD_MAJOR.$((HEAD_MINOR+1))"
else
    echo "No version bump on branch $BRANCH"
    exit 0
fi

echo $NEW_VERSION > VERSION
echo "Bumped version to $NEW_VERSION"

echo "VERSION=$NEW_VERSION" >> $GITHUB_ENV