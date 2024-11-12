#!/usr/bin/env python
from crewai import Pipeline
from generix_ocr.crews.ocr_crew.ocr_crew import OCRCrew
from generix_ocr.pipelines.pipeline import GenerixOcrPipeline

try:
    pipeline = GenerixOcrPipeline()
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    print(traceback.format_exc()) 