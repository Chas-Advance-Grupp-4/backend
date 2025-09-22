## CI v1 Tests – Backend ##

This document describes the CI v1 Tests workflow for the backend, powered by GitHub Actions. The pipeline ensures that tests run automatically on pull requests and can also be triggered manually.

### Purpose ### 

Run backend tests automatically on all changes before merging into develop or main.  
Enable manual execution via GitHub Actions “Run workflow” button.  
Ensure a reproducible environment with pinned Python and dependency versions.   

#### Workflow Triggers ####
Automatic: Pull requests targeting develop or main.  
Manual: Trigger via workflow_dispatch from GitHub Actions.  

#### Steps ####
Checkout repository – fetches code from the current branch.  
Set up Python environment – installs the specified Python version (3.13).  
Install dependencies – upgrades pip and installs packages from requirements.txt.  
Run tests – executes pytest on backend tests; full output is shown for debugging.  
All tests passed – if tests succeed, a message is printed in the log: " All tests passed!".  

#### Best Practices ####
Test locally first in a virtual environment before pushing.  
Keep the Python version consistent between local and CI (3.13).  
Pin dependency versions in requirements.txt for reproducibility.  
Use workflow_dispatch for manual test runs without opening a PR.  

#### Notes ####
CI runs on Ubuntu-latest, which may differ from Windows or macOS local environments.  
Some dependencies may require different patch versions on different OSes.  
Always check the full log in Actions for failing tests.  