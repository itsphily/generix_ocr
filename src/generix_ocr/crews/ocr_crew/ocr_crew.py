from pydantic import BaseModel
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileWriterTool
from generix_ocr.tools.custom_tool import CustomVisionTool  # Import our custom tool
import os
from dotenv import load_dotenv
from pathlib import Path
from crewai import LLM

# After load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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

    # Use our custom vision tool instead of the built-in one
    vision_tool = CustomVisionTool()
    file_writer_tool = FileWriterTool()

    def __init__(self):
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

    @agent
    def image_text_extractor(self) -> Agent:
        llm = LLM(model="gpt-4o")
        return Agent(
            config=self.agents_config['image_text_extractor'],
            verbose=True,
            tools=[self.vision_tool],
            llm=llm
        )

    @agent
    def document_classifier(self) -> Agent:
        llm = LLM(model="gpt-4o")
        return Agent(
            config=self.agents_config['document_classifier'],
            verbose=True,
            llm=llm
        )
    
    @agent
    def ocr_output_comparator(self) -> Agent:
        llm = LLM(model="gpt-4o")
        return Agent(
            config=self.agents_config['ocr_output_comparator'],
            verbose=True,
            llm=llm
        )

    @task
    def text_extraction_task(self) -> Task:
        # Create output directory if it doesn't exist
        output_dir = Path.cwd() / 'outputs'
        output_dir.mkdir(exist_ok=True)
        output_file = 'OCRoutput.txt'
        
        return Task(
            config=self.tasks_config['text_extraction_task'],
            output_file=str(output_file)  # Convert Path to string
        )

    @task
    def ocr_output_comparison(self) -> Task:
        return Task(
            config=self.tasks_config['ocr_output_comparison'],
            #output_pydantic=OCRevaluation,
            output_file='openAI_output.txt'
        )
    
    @task
    def document_classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['document_classification_task'],
            output_pydantic=OCRClassification,
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