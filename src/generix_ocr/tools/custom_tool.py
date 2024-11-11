from typing import Type
from crewai_tools import BaseTool
import base64
from openai import OpenAI
import os

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
