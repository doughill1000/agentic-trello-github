from github_client import create_branch as gh_create_branch, create_draft_pr as gh_create_draft_pr
from trello_client import update_card as trello_update_card  # assuming you have or will define this

# GitHub wrappers

def create_branch(branch_name: str, owner: str, repo: str) -> str:
    return gh_create_branch(owner=owner, repo=repo, branch_name=branch_name)

def create_draft_pr(owner: str, repo: str, branch_name: str, title: str, body: str) -> str:
    return gh_create_draft_pr(owner=owner, repo=repo, branch_name=branch_name, title=title, body=body)

# Trello wrapper (stub)
def update_trello_card(card_id: str, pr_url: str, test_summary: str) -> str:
    return trello_update_card(card_id, pr_url, test_summary)  # Implement this in trello_client.py
