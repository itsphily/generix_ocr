from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
import os
from dotenv import load_dotenv
from generix_ocr.tools.custom_tool import AirtableWriterTool
# After load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


@CrewBase
class ETLCrew():
	"""ETL Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	airtable_writer_tool = AirtableWriterTool()

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

	@agent
	def transform_load_specialist(self) -> Agent:
		llm = LLM(model="gpt-4o")
		return Agent(
			config=self.agents_config['transform_load_specialist'],
			verbose=True,
			tools=[self.airtable_writer_tool],
			llm=llm
		)

	@task
	def data_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_extraction_task'],
			output_file='test.md'
		)

	@task
	def transform_load_task(self) -> Task:
		return Task(
			config=self.tasks_config['transform_load_task'],
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