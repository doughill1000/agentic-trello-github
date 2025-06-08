import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_latest_commit_sha(owner: str, repo: str, base_branch: str = "main") -> str:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/ref/heads/{base_branch}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["object"]["sha"]

def create_branch(owner: str, repo: str, branch_name: str, base_branch: str = "main") -> str:
    sha = get_latest_commit_sha(owner, repo, base_branch)
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/git/refs"
    payload = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return f"Branch '{branch_name}' created successfully."

def create_draft_pr(owner: str, repo: str, branch_name: str, title: str, body: str) -> str:
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    payload = {
        "title": title,
        "head": branch_name,
        "base": "main",
        "body": body,
        "draft": True
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()["html_url"]
