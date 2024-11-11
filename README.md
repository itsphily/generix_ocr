# GenerixOCR - Automated Document Processing AI

GenerixOCR is an intelligent document processing system that leverages multiple vision models to extract text from images. The system uses a combination of open-source and proprietary models to ensure robust text extraction:
- Llama 3.2 Vision (open source)
- MiniCPM Vision (open source)
- GPT-4 Vision (via OpenAI API)

## Key Features

- **Multi-Model Processing**: Uses three different vision models for comprehensive text extraction
- **Local and Cloud Processing**: Combines local (Ollama-based) and cloud (OpenAI) processing
- **Custom Vision Tool**: Implements a custom CrewAI tool for OpenAI vision processing
- **Automated Pipeline**: Processes images through all models sequentially
- **Structured Output**: Saves results from each model in organized output files

## Prerequisites

- Python >=3.10 <=3.13
- [Ollama](https://ollama.ai/) for local vision models
- OpenAI API key for GPT-4 Vision
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

1. Install Ollama:
```bash
# For macOS
curl -fsSL https://ollama.ai/install.sh | sh
```

2. Install required vision models:
```bash
# Install Llama 3.2 Vision
ollama pull llama3.2-vision

# Install MiniCPM Vision
ollama pull minicpm-v
```

3. Clone and install the project:
```bash
git clone https://github.com/yourusername/generix_ocr.git
cd generix_ocr
poetry install
```

4. Environment setup:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your_key_here
     ```

## Project Structure

```
generix_ocr/
├── src/
│   └── generix_ocr/
│       ├── crews/
│       │   └── ocr_crew/         # OCR processing crew
│       ├── tools/
│       │   └── custom_tool.py    # Custom Vision Tool for OpenAI
│       ├── pipelines/            # Processing pipeline
│       └── main.py              # Main execution script
└── Documents_for_processing/     # Input directory for images
```

## Custom Vision Tool

The project implements a custom CrewAI tool for OpenAI Vision processing:

```python
class CustomVisionTool(BaseTool):
    name: str = "Custom Vision Tool"
    description: str = "A tool that processes images using OpenAI's GPT-4 Vision model"

    def _run(self, image_path: str) -> str:
        # Processes image using OpenAI's GPT-4 Vision API
        # Returns extracted text
```

## Usage

1. Place your documents in the `Documents_for_processing` folder
2. Run the OCR pipeline:
```bash
poetry run python -m generix_ocr.main
```

## Output

The system generates three types of output:
1. `outputs/vision_model_outputs.txt` - Results from Llama and MiniCPM models
2. `OCRoutput.txt` - Results from the OCR crew tasks
3. `openAI_output.txt` - Results from GPT-4 Vision processing

## Current Status

The project is currently under development with:
- ✅ Multi-model text extraction
- ✅ Custom Vision Tool implementation
- ✅ Basic pipeline structure
- 🚧 Advanced document processing (in progress)
- 🚧 Result comparison and validation (in progress)

## License

[Your chosen license]

## Support

For support:
- GitHub Issues
- [Documentation](link_to_your_docs)
