from typing import Type, Dict
from crewai_tools import BaseTool
from pydantic import BaseModel
import base64
from openai import OpenAI
import os
from generix_ocr.models.document_models import (
    InvoiceData,
    DeliveryNoteData,
    ReceptionNoteData,
    PurchaseOrderData
)

class CustomVisionTool(BaseTool):
    name: str = "Custom Vision Tool"
    description: str = "A tool that processes images using OpenAI's GPT-4 Vision model with base64 encoding"

    def _run(self, image_path: str) -> str:
        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Read and encode the image to base64
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Create the message with base64 encoded image
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all the text from the image and return only the text and nothing else."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error processing image: {str(e)}"


class DocumentModelSelector(BaseTool):
    name: str = "Document Model Selector"
    description: str = "A tool that selects the appropriate Pydantic model based on document classification"

    # Define mapping of document types to their corresponding models
    MODEL_MAPPING: Dict[str, Type[BaseModel]] = {
        "invoice": InvoiceData,
        "delivery_note": DeliveryNoteData,
        "reception_note": ReceptionNoteData,
        "purchase_order": PurchaseOrderData
    }

    def _run(self, document_type: str) -> Type[BaseModel]:
        """
        Returns the appropriate Pydantic model based on the document classification.
        
        Args:
            document_type (str): The type of document (e.g., 'invoice', 'delivery_note')
            
        Returns:
            Type[BaseModel]: The corresponding Pydantic model class
            
        Raises:
            ValueError: If the document type is not recognized
        """
        # Normalize the input string
        normalized_type = document_type.lower().replace(" ", "_")
        
        # Get the corresponding model
        model = self.MODEL_MAPPING.get(normalized_type)
        
        if model is None:
            raise ValueError(
                f"Unknown document type: {document_type}. "
                f"Supported types are: {', '.join(self.MODEL_MAPPING.keys())}"
            )
            
        return model