# CI v1 Tests – Backend

This document describes the **CI v1 tests workflow** for the backend, powered by GitHub Actions.  
The workflow ensures tests run automatically on pull requests and can also be triggered manually.

---

## Purpose

- Automatically run backend tests on all changes before merging into `develop` or `main`.  
- Enable manual execution via GitHub Actions “Run workflow” button.  
- Ensure a reproducible environment with pinned Python and dependency versions.

---

## Workflow Triggers

- **Automatic:** Pull requests targeting `develop` or `main`  
- **Manual:** Trigger via `workflow_dispatch` in GitHub Actions  

---

## Workflow Steps

1. **Checkout repository** – fetch the current branch  
2. **Set up Python environment** – install Python 3.13  
3. **Install dependencies** – upgrade pip and install `requirements.txt`  
4. **Run tests** – execute `pytest`; full output is shown for debugging  
5. **All tests passed** – message printed: "All tests passed!"  

---

## Best Practices

- Test locally first in a virtual environment before pushing  
- Keep Python version consistent between local and CI (3.13)  
- Pin dependency versions in `requirements.txt` for reproducibility  
- Use `workflow_dispatch` for manual test runs without opening a PR  

---

## Notes

- CI runs on `ubuntu-latest`; behavior may differ slightly from Windows or macOS  
- Some dependencies may require different patch versions on different OSes  
- Always check the full GitHub Actions log for failing tests  
