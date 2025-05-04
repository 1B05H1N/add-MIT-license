# GitHub MIT License Checker

This script checks your GitHub repositories for MIT licenses and adds them where missing.

## Prerequisites

1. Python 3.6 or higher
2. A GitHub Personal Access Token with `repo` scope

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your GitHub Personal Access Token:
   - Go to GitHub Settings -> Developer settings -> Personal access tokens
   - Generate a new token with the `repo` scope
   - Set the token as an environment variable:
     ```bash
     export GITHUB_TOKEN='your_token_here'
     ```

## Usage

Run the script:
```bash
python add_mit_license.py
```

The script will:
1. Fetch all your GitHub repositories
2. Check each repository for an MIT license
3. Add an MIT license file to repositories that don't have one
4. Print the status of each repository

## Notes

- The script will only add MIT licenses to repositories where you have write access
- The license will be added to the default branch of each repository
- The copyright year will be set to the current year
- The copyright holder will be set to your GitHub username 