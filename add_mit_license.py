import requests
import os
import base64
from datetime import datetime

# GitHub API configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # You'll need to set this environment variable

def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def get_user_repos():
    """Fetch all repositories for the authenticated user"""
    url = f"{GITHUB_API_URL}/user/repos"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()

def check_license_exists(repo):
    """Check if a repository has an MIT license"""
    url = f"{GITHUB_API_URL}/repos/{repo['full_name']}/license"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            license_data = response.json()
            return license_data.get("license", {}).get("key") == "mit"
    except requests.exceptions.RequestException:
        return False
    return False

def create_mit_license(repo):
    """Create an MIT license file in the repository"""
    current_year = datetime.now().year
    license_content = f"""MIT License

Copyright (c) {current_year} {repo['owner']['login']}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    # Create the license file
    url = f"{GITHUB_API_URL}/repos/{repo['full_name']}/contents/LICENSE"
    data = {
        "message": "Add MIT License",
        "content": base64.b64encode(license_content.encode()).decode('utf-8'),
        "branch": repo.get("default_branch", "main")
    }
    
    try:
        response = requests.put(url, headers=get_headers(), json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error creating license for {repo['name']}: {str(e)}")
        return False

def main():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable is not set")
        print("Please set your GitHub personal access token as an environment variable")
        return

    try:
        repos = get_user_repos()
        for repo in repos:
            if not check_license_exists(repo):
                print(f"Adding MIT license to {repo['name']}...")
                if create_mit_license(repo):
                    print(f"Successfully added MIT license to {repo['name']}")
                else:
                    print(f"Failed to add MIT license to {repo['name']}")
            else:
                print(f"{repo['name']} already has an MIT license")

    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 