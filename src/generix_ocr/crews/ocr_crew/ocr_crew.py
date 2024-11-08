from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import VisionTool
import os
from dotenv import load_dotenv
import ollama


class OCRClassification(BaseModel):
	"""Classification of the OCR result"""
	document_type: str
	content: str


class OCRevaluation(BaseModel):
	"""Evaluation of the OCR result"""
	evaluation: str


@CrewBase
class OCRCrew():
	"""OCR Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# Class-level attributes
	# THIS IS NOT WORKING NEED TO FIX
	ollama_vision = LLM(
		model='ollama/llama3.2-vision',
		base_url='http://localhost:11434'
	)

	vision_tool = VisionTool()  # Moved to class level

	def __init__(self):
		# Load environment variables
		load_dotenv()
		
		# Verify API key is loaded
		if not os.getenv("OPENAI_API_KEY"):
			raise ValueError("OPENAI_API_KEY not found in environment variables")
		
		os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

	@agent
	def image_text_extractor(self) -> Agent:
		'''
		Agent that extracts text from an image
		'''
		return Agent(
			config=self.agents_config['image_text_extractor'],
			verbose=True,
			tools=[self.vision_tool]  
		)

	@agent
	def document_classifier(self) -> Agent:
		return Agent(
			config=self.agents_config['document_classifier'],
			verbose=True
		)
	
	@agent
	def ocr_output_comparator(self) -> Agent:
		return Agent(
			config=self.agents_config['ocr_output_comparator'],
			verbose=True
		)

	@task
	def text_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['text_extraction_task'],
		)

	@task
	def ocr_output_comparison(self) -> Task:
		return Task(
			config=self.tasks_config['ocr_output_comparison'],
			output_pydantic=OCRevaluation
		)
	
	@task
	def document_classification_task(self) -> Task:
		return Task(
			config=self.tasks_config['document_classification_task'],
			output_pydantic=OCRClassification
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the OCR Classification Crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)