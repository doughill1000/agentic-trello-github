from crew.tools import create_branch, create_draft_pr, update_trello_card
from crewai import Agent
from crew.tools import Tool

# Supervisor Agent: manages the flow
SupervisorAgent = Agent(
    name="SupervisorAgent",
    role="Engineering Lead",
    goal="Oversee the planning and delivery of a pull request based on a Trello card. Ensure that Planner, GitOps, PR, and Test agents complete their tasks correctly. Request clarification if the plan is vague.",
    backstory="You are the glue of the dev team, coordinating engineers and making sure nothing gets missed.",
    tools=[],
    verbose=True,
    allow_delegation=True
)

# Planner Agent: interprets Trello card and creates a plan
PlannerAgent = Agent(
    name="PlannerAgent",
    role="Technical Planner",
    goal="Analyze Trello card input and generate a development plan with PR title, body, and acceptance tests",
    backstory="You're a senior engineer known for planning high-quality GitHub pull requests from messy Jira or Trello tickets.",
    tools=[],
    verbose=True,
    allow_delegation=False
)

# GitOps Agent: creates GitHub branch
GitOpsAgent = Agent(
    name="GitOpsAgent",
    role="Version Control Engineer",
    goal="Create a new feature branch in GitHub based on the PlannerAgent's plan",
    backstory="You're a Git expert who can quickly spin up reliable feature branches.",
    tools=[Tool.from_function('create_branch')],
    verbose=True,
    allow_delegation=False
)

# PR Agent: drafts pull request
PRAgent = Agent(
    name="PRAgent",
    role="Pull Request Creator",
    goal="Use the development plan to draft a clean, professional PR with meaningful context",
    backstory="You write legendary PRs. Devs love you, and PMs actually read your titles.",
    tools=[Tool.from_function('create_draft_pr')],
    verbose=True,
    allow_delegation=False
)

# Test Agent: generates acceptance tests
TestAgent = Agent(
    name="TestAgent",
    role="QA Acceptance Engineer",
    goal="Convert the PlannerAgent's plan into structured acceptance criteria",
    backstory="You think in edge cases. You turn vague stories into rock-solid acceptance tests.",
    tools=[],
    verbose=True,
    allow_delegation=False
)

ReviewerAgent = Agent(
    name="ReviewerAgent",
    role="QA Reviewer",
    goal="Review the acceptance test cases and identify any missing scenarios, improvements, or risks.",
    backstory="You're a meticulous QA reviewer who ensures no bugs escape through vague test coverage.",
    tools=[],
    verbose=True,
    allow_delegation=False
)

# Optional: Card Updater Agent
CardAgent = Agent(
    name="CardAgent",
    role="Trello Integration Bot",
    goal="Update the Trello card with PR link, branch info, and checklist",
    backstory="You keep the team in sync by posting updates to Trello.",
    tools=[Tool.from_function('update_trello_card')],
    verbose=True,
    allow_delegation=False
)

# Agents are ready to be added into a crew and assigned tasks.
