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
    
    docs_path = Path('/Users/phili/Library/CloudStorage/Dropbox/Phil/LeoMarketing/Marketing/Generix/generix_ocr/Documents_for_processing')
    
    print(f"Looking for documents in: {docs_path}")
    
    image_urls = []
    for file_path in docs_path.glob('*'):
        if file_path.suffix.lower() in supported_formats:
            image_urls.append(str(file_path.absolute()))
            print(f"Added file: {file_path.name}")
        elif file_path.suffix.lower() in convertible_formats:
            # Convert WEBP to PNG
            converted_path = convert_webp_to_png(file_path)
            image_urls.append(converted_path)
    
    if not image_urls:
        print("\nWarning: No supported documents found")
        print("Supported formats:", supported_formats + convertible_formats)
        
    return image_urls

def llama_vision_model(image_path, prompt):
    try:
        print(f"Processing image with Llama model: {image_path}")
        response = ollama.chat(
            model='llama3.2-vision',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }]
        )
        
        content = response['message']['content']
        
        # Write only the model output to file
        output_dir = Path.cwd() / 'outputs'
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / 'vision_model_outputs.txt'
        
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("\n\n=== Llama Vision Model Output ===\n")
            f.write(f"{content}\n")
            f.write("="*50 + "\n")
            
        return content
        
    except Exception as e:
        print(f"Error in llama_vision_model: {str(e)}")
        return None

def minicpm_vision_model(image_path, prompt):
    try:
        print(f"Processing image with MiniCPM model: {image_path}")
        response = ollama.chat(
            model='minicpm-v',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_path]
            }]
        )
        
        content = response['message']['content']
        
        # Write only the model output to file
        output_dir = Path.cwd() / 'outputs'
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / 'vision_model_outputs.txt'
        
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write("\n\n=== MiniCPM Vision Model Output ===\n")
            f.write(f"{content}\n")
            f.write("="*50 + "\n")
            
        return content
        
    except Exception as e:
        print(f"Error in minicpm_vision_model: {str(e)}")
        return None

async def run():
    """Run the pipeline."""
    # Get document URLs
    image_urls = get_document_urls()
    
    if not image_urls:
        print("Error: No images found")
        return
    
    # Define prompts
    prompt = '''
    Extract all the text from the image and return only the text and nothing else.
    '''

    # Process first image with Llama and MiniCPM
    first_image_path = image_urls[0]
    extracted_text = llama_vision_model(first_image_path, prompt)
    minicpm_extracted_text = minicpm_vision_model(first_image_path, prompt)
    
    # Set up inputs
    inputs = {
        "image_path": first_image_path,
        "llama_ocr_output": extracted_text,
        "minicpm_ocr_output": minicpm_extracted_text
    }
    print(f"Inputs: {inputs}")

    # Initialize pipeline
    pipeline = GenerixOcrPipeline()
    results = await pipeline.kickoff([inputs])


    for result in results:
        print(f"Raw output: {result.raw}")
        if result.json_dict:
            print(f"JSON output: {result.json_dict}")
        if result.pydantic:
            print(f"Pydantic output: {result.pydantic}")
        print("\n")
    

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()