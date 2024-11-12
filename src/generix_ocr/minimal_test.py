#!/usr/bin/env python
import asyncio
from pathlib import Path
from PIL import Image
import ollama

async def test_vision():
    try:
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': 'Hello',
            }]
        )
        return response['message']['content']
    except Exception as e:
        print(f"Vision model error: {str(e)}")

async def run():
    await test_vision()

def main():
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 