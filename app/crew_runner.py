from crewai import Crew, Task
from crew.agents import SupervisorAgent, PlannerAgent, GitOpsAgent, PRAgent, TestAgent, CardAgent
from app.services.aiContentGenerator import generate_pr_and_tests

def run_workflow_from_card(title: str, description: str, card_id: str):
    from crewai import Crew, Task
    from crew.agents import SupervisorAgent, PlannerAgent, GitOpsAgent, PRAgent, TestAgent, ReviewerAgent, CardAgent
    from app.services.openai_llm import generate_pr_and_tests

    # Step 1: PlannerAgent generates a plan
    plan = generate_pr_and_tests(trello_card["title"], trello_card["description"])

    # Step 2: Inject the plan as context to downstream agents
    tasks = [
        Task(
            agent=PlannerAgent,
            description="Create a development plan from the Trello card",
            expected_output=str(plan)
        ),
        Task(
            agent=GitOpsAgent,
            description="Create a GitHub branch",
            expected_output="Feature branch created successfully",
            context=[plan["branch_name"]],
            input={
                "owner": "doughill1000",
                "repo": "agentic-trello-github"
            }
        ),
        Task(
            agent=PRAgent,
            description="Draft a pull request",
            expected_output="PR drafted",
            context=[plan["branch_name"], plan["pr_title"], plan["pr_body"]]
        ),
        Task(
            agent=TestAgent,
            description="Generate comprehensive acceptance tests",
            expected_output="List of test cases",
            context=plan["acceptance_tests"]
        ),
        Task(
            agent=CardAgent,
            description="Update Trello card with PR details",
            expected_output="Trello card updated",
            context=["card_id_placeholder", "https://github.com/your-org/repo/pull/123", plan["acceptance_tests"]]
        )
    ]

    # Create and run the crew
    crew = Crew(
        agents=[
            SupervisorAgent, PlannerAgent, GitOpsAgent, PRAgent, TestAgent, CardAgent
        ],
        tasks=tasks,
        verbose=True
    )

    crew.kickoff()
