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
        print('got here')
        pipeline = self.create_pipeline()
        print(inputs)
        print('test')
        results = await pipeline.kickoff(inputs)
        return results
