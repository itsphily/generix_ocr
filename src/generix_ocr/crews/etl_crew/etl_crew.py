from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
import os
from dotenv import load_dotenv
# After load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


@CrewBase
class ETLCrew():
	"""ETL Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self):
		load_dotenv()
		if not os.getenv("OPENAI_API_KEY"):
			raise ValueError("OPENAI_API_KEY not found in environment variables")
		os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

	@agent
	def data_extractor(self) -> Agent:
		llm = LLM(model="gpt-4o")
		return Agent(
			config=self.agents_config['data_extractor'],
			verbose=True,
			llm=llm
		)

	@task
	def data_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_extraction_task'],
			output_file='test.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ETL crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)