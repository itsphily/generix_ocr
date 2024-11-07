# Common imports for both examples
from crewai import Pipeline

from ..crews.ocr_crew.ocr_crew import OcrCrew
from ..crews.write_x_crew.write_x_crew import WriteXCrew

class GenerixOcrPipeline:
    def __init__(self):
        # Initialize crews
        self.ocr_crew = OcrCrew().crew()
    
    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.ocr_crew,
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        results = await pipeline.kickoff(inputs)
        return results
