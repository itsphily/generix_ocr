#!/usr/bin/env python
import asyncio
from pathlib import Path
from generix_ocr.pipelines.pipeline import GenerixOcrPipeline
from PIL import Image
import ollama

def convert_webp_to_png(webp_path):
    """Convert WEBP image to PNG format"""
    # Open the WEBP image
    image = Image.open(webp_path)
    
    # Create output path with PNG extension
    output_path = webp_path.parent / f"{webp_path.stem}.png"
    
    # Save as PNG
    image.save(output_path, 'PNG')
    print(f"Converted {webp_path.name} to {output_path.name}")
    
    return str(output_path)

def get_document_urls():
    """
    Get all document URLs from the Documents_for_processing folder
    """
    # Define supported image formats
    supported_formats = ('.png', '.jpg', '.jpeg')
    convertible_formats = ('.webp',)
    
    # Use the direct path you provided
    docs_path = Path('/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Generix/generix_ocr/Documents_for_processing')
    
    print(f"Looking for documents in: {docs_path}")
    print(f"Directory exists: {docs_path.exists()}")
    print(f"Is directory: {docs_path.is_dir()}")
    
    # List all files in directory
    print("\nAll files in directory:")
    for file in docs_path.iterdir():
        print(f"Found: {file.name} (suffix: {file.suffix})")
    
    # Get all image files
    image_urls = []
    for file_path in docs_path.glob('*'):
        print(f"Checking file: {file_path.name} with suffix: {file_path.suffix}")
        if file_path.suffix.lower() in supported_formats:
            image_urls.append(str(file_path.absolute()))
            print(f"Added file: {file_path.name}")
        elif file_path.suffix.lower() in convertible_formats:
            # Convert WEBP to PNG
            converted_path = convert_webp_to_png(file_path)
            image_urls.append(converted_path)
    
    if not image_urls:
        print("\nWarning: No supported documents found in Documents_for_processing folder")
        print("Supported formats:", supported_formats + convertible_formats)
        
    print(f"\nFound documents: {image_urls}")
    return image_urls


def llama_vision_model(image_path):
    try:
        
        print(f"Using image: {image_path}")
        # Create the message with the image
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': 'Can you extract the text from this image?',
                'images': [image_path]
            }]
        )
        
        return response['message']['content']
        
    except Exception as e:
        print(f"Error: {str(e)}")


async def run():
    """
    Run the pipeline.
    """
    # Get document URLs and prepare input
    image_urls = get_document_urls()
    
    if not image_urls:
        print("Error: No images found")
        return

    # Set up inputs as a single dictionary (like in the working example)
    inputs = {
        "image_path": image_urls[0]  # Take first image for now
    }
    print(f"Inputs: {inputs}")

    # Run the llama3.2-vision model
    text = llama_vision_model(inputs['image_path'])
    print(f"Text: {text}")
    
    # Initialize and run the pipeline
    pipeline = GenerixOcrPipeline()
    results = await pipeline.kickoff([inputs])  # Note: still wrapped in a list as required by pipeline
    
    # Process and print results
    for result in results:
        print(f"Raw output: {result.raw}")
        if result.json_dict:
            print(f"JSON output: {result.json_dict}")
        print("\n")

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()