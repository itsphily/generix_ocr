# Common imports for both examples
from crewai import Pipeline
from generix_ocr.crews.ocr_crew.ocr_crew import OCRCrew

class GenerixOcrPipeline:
    def __init__(self):
        # Initialize crews
        self.ocr_crew = OCRCrew().crew()
    
    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.ocr_crew,
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        print(inputs)
        results = await pipeline.kickoff(inputs)
        return results
