import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

OWNER = "doughill1000"
REPO = "agentic-trello-github"

def get_latest_commit_sha(base_branch: str = "master") -> str:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/git/ref/heads/{base_branch}"
    logging.info("Get Sha")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["object"]["sha"]

def create_branch(branch_name: str, base_branch: str = "master") -> str:
    sha = get_latest_commit_sha(base_branch)
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/git/refs"
    payload = {
        "ref": f"refs/heads/{branch_name}",
        "sha": sha
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return f"Branch '{branch_name}' created successfully."

def create_draft_pr(branch_name: str, title: str, body: str) -> str:
    url = f"{GITHUB_API_URL}/repos/{OWNER}/{REPO}/pulls"
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
