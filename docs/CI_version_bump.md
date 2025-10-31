# Version Bump Workflow – Backend

This document describes the **GitHub Actions workflow** for automatically bumping the version of the backend repository.  
It detects changes in the `VERSION` file, increments it if needed, and creates a pull request with the new version.

---

## Purpose

- Automatically check if the `VERSION` file needs to be bumped on pushes to `develop` or `main`  
- Prevent duplicate version bumps by checking if the last commit already updated `VERSION`  
- Generate a GitHub App token to perform version bump commits and create pull requests securely  
- Ensure consistent versioning in the repository and reduce manual errors

---

## Workflow Triggers

- **Automatic:** On push to `develop` or `main`  
- **Manual:** Trigger via `workflow_dispatch` in GitHub Actions  

---

## Workflow Steps

1. **Checkout repository** – Fetch full history (`fetch-depth: 0`) to allow comparison with previous commits  
2. **Check if VERSION file changed** –  
   - Runs `git diff HEAD~1 --name-only` to check if `VERSION` was modified  
   - Sets `bump_needed` to `true` if a bump is required  
   - Exits early if `bump_needed` is `false`  
3. **Generate GitHub App token** – Runs only if a bump is needed; token has permissions to create commits and PRs  
4. **Make script executable** – `.github/scripts/bump_version.sh`  
5. **Bump version** – Executes `.github/scripts/bump_version.sh` to increment the version  
6. **Log new version** – Prints updated version to workflow logs  
7. **Commit and create PR** –  
   - Creates a branch `version-bump-<branch>-<run_number>`  
   - Commits updated `VERSION` file  
   - Pushes branch and creates pull request with title `Bump version to <VERSION>`

---

## Environment Variables & Secrets

- **APP_ID** & **PRIVATE_KEY** – GitHub App credentials  
- **GITHUB_TOKEN** – Used to authorize git push and pull request creation  

---

## Best Practices

- Ensure `VERSION` file is correctly formatted  
- Review PR created by workflow before merging  
- Keep secrets safe in GitHub Actions settings; do not expose them in code  

---

## Notes

- Workflow runs only on non-forked repositories (`if: github.event.repository.fork == false`)  
- Merging the PR updates the `VERSION` file and triggers downstream workflows  
- `.github/scripts/bump_version.sh` determines the next version automatically  
