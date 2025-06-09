from app.clients.github_client import create_branch as gh_create_branch, create_draft_pr as gh_create_draft_pr
from app.clients.trello_client import add_checklist_to_card, update_card_description
from crewai.tools import tool

# GitHub wrappers
@tool("Create Github Branch")
def create_branch(branch_name: str) -> str:
    """ Create a github branch """
    return gh_create_branch(branch_name=branch_name)

@tool("Create Github Pull Request")
def create_draft_pr(branch_name: str, title: str, body: str) -> str:
    """ Create a draft pull request from the newly created github branch """
    return gh_create_draft_pr(branch_name=branch_name, title=title, body=body)

# Trello wrapper (stub)
@tool("Update Trello Card")
def update_trello_card(card_id: str, story_description: str, test_cases: list, acceptance_criteria: list) -> str:
    """ Add checklists for acceptance criteria. Add a card description which includes a story description and the test cases """ 
    add_checklist_to_card(card_id, "Acceptance Criteria", acceptance_criteria)

    # Step 2: Format updated description (original description + test cases)
    test_case_text = "\n\n🧪 **Test Cases**\n" + '\n'.join([f"- {item}\n" for item in test_cases])
    full_description = f"{story_description.strip()}{test_case_text}"

    # Step 3: Update card description
    update_card_description(card_id, full_description)
