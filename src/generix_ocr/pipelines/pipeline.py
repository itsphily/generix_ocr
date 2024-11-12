# Common imports for both examples
from crewai import Pipeline
from generix_ocr.crews.ocr_crew.ocr_crew import OCRCrew
from generix_ocr.crews.etl_crew.etl_crew import ETLCrew

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
        # Extract values from pydantic model
        document_type = results[0].pydantic.document_type
        aggregated_output = results[0].pydantic.aggregated_output

        return results, document_type, aggregated_output


class GenerixETLPipeline:
    def __init__(self):
        # Initialize crews
        self.etl_crew = ETLCrew().crew()
    
    def create_pipeline(self):
        return Pipeline(
            stages=[
                self.etl_crew,
            ]
        )
    
    async def kickoff(self, inputs):
        pipeline = self.create_pipeline()
        print(inputs)
        results = await pipeline.kickoff(inputs)

        return results
