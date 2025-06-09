from app.card_requirements_crew.tools.tools import update_trello_card
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class CardRequirementsCrew():
    """ Update Trello card based on title with description, test cases and AC """

    agents: List[BaseAgent]
    tasks: List[Task]

    ### AGENTS ###

    # @agent
    # def project_planner(self) -> Agent:
    #     try:
    #         print(self.agents_config['project_planner'])
    #         print(self.tasks_config['project_planner_task'])
    #         return Agent(
    #             config=self.agents_config['project_planner'],
    #             verbose=True,
    #             allow_delegation=True
    #         )
    #     except Exception as e:
    #         print(e)
    
    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'],
            verbose=True,
        )
    
    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],
            verbose=True
        )
    
    # @agent
    # def review(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['reviewer'],
    #         verbose=True,
    #         allow_delegation=True
    #     )
    
    @agent
    def card_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['card_writer'],
            verbose=True,
            tools=[update_trello_card],
        )
    
    ### TASKS ###

    # @task
    # def project_planner_task(self) -> Task:
    #     try:
    #         print(self.tasks_config['project_planner_task'])
    #         return Task(
    #             config=self.tasks_config['project_planner_task']
    #         )
    #     except Exception as e:
    #         print(e)

    @task
    def ac_task(self) -> Task:
        return Task(
            config=self.tasks_config['ac_task']
        )
    
    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task']
        )

    @task
    def card_task(self) -> Task:
        return Task(
            config=self.tasks_config['card_task']
        )
    
    ### CREW ###

    @crew
    def crew(self) -> Crew:
        """ Create and run the crew """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            memory=True,
            process=Process.sequential,
            # max_reruns=0
        )

