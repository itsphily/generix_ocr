from typing import Type, Dict
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import base64
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

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

class AirtableWriterTool(BaseTool):
    name: str = "Airtable Writer Tool"
    description: str = "A tool that writes invoice data to Airtable"
    api_token: str = Field(default_factory=lambda: os.getenv('AIRTABLE_TOKEN'))
    base_id: str = Field(default_factory=lambda: os.getenv('AIRTABLE_BASE_ID'))
    table_id: str = Field(default_factory=lambda: os.getenv('AIRTABLE_TABLE_ID'))
    headers: dict = Field(default_factory=lambda: {
        'Authorization': f'Bearer {os.getenv("AIRTABLE_TOKEN")}',
        'Content-Type': 'application/json'
    })

    def _run(self, data: Dict) -> str:
        """Write data to Airtable"""
        try:
            # The data should be passed directly, not wrapped in another dict
            airtable_data = {
                "records": [{
                    "fields": {
                        "invoice_number": data["invoice_number"],
                        "invoice_date": data["invoice_date"],
                        "invoice_total": data["invoice_total"]  # Convert to float for Airtable
                    }
                }]
            }

            url = f'https://api.airtable.com/v0/{self.base_id}/{self.table_id}'
            response = requests.post(url, headers=self.headers, json=airtable_data)

            if response.status_code == 200:
                return f"Successfully wrote data to Airtable: {response.json()}"
            else:
                return f"Error writing to Airtable: {response.text}"

        except Exception as e:
            return f"Error in AirtableWriterTool: {str(e)}"
