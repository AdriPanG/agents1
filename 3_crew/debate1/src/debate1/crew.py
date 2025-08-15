from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class Debate1():
    """Debate1 crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config['debater'],
            verbose=True,
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'],
            verbose=True
        )


    @task
    def propose(self) -> Task:
        return Task(
            config=self.tasks_config['propose']
        )

    @task
    def oppose(self) -> Task:
        return Task(
            config=self.tasks_config['oppose']
        )

    @task
    def decide(self) -> Task:
        return Task(
            config=self.tasks_config['decide']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate1 crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
