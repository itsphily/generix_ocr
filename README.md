# GenerixOCR - Automated Document Processing AI

GenerixOCR is an intelligent document processing system that leverages multiple vision models to extract text from images and processes it through a pipeline for data extraction and storage.

## Key Features

- **Multi-Model Text Extraction**: Uses three different vision models:
  - Llama 3.2 Vision (open source)
  - MiniCPM Vision (open source)
  - GPT-4 Vision (via OpenAI API)

- **Intelligent Processing Pipeline**:
  1. OCR Crew:
     - Text extraction from multiple models
     - Output aggregation
     - Document classification
  2. ETL Crew (in development):
     - Data formatting and validation
     - Airtable integration for data storage

- **Automated Data Storage**: Integrates with Airtable for structured data storage

## Prerequisites

- Python >=3.10 <=3.13
- [Ollama](https://ollama.ai/) for local vision models
- OpenAI API key for GPT-4 Vision
- Airtable account and API credentials
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
   Copy `.env.example` to `.env` and add your credentials:
   ```
   OPENAI_API_KEY=your_key_here
   AIRTABLE_TOKEN=your_token_here
   AIRTABLE_BASE_ID=your_base_id
   AIRTABLE_TABLE_ID=your_table_id
   ```

## Project Structure

```
generix_ocr/
├── src/
│   └── generix_ocr/
│       ├── crews/
│       │   ├── ocr_crew/       # OCR processing crew
│       │   └── etl_crew/       # ETL processing crew
│       ├── tools/
│       │   └── custom_tool.py  # Custom tools including AirtableWriterTool
│       ├── pipelines/          # Processing pipelines
│       └── main.py            # Main execution script
├── Documents_for_processing/   # Input directory for images
└── outputs/                   # Output directory for processed data
```

## Usage

1. Place your documents in the `Documents_for_processing` folder
2. Run the OCR pipeline:
```bash
poetry run python -m generix_ocr.main
```

## Output Files

The system generates several output files:
1. `outputs/vision_model_outputs.txt` - Raw outputs from each vision model
2. `OCRoutput.txt` - Processed text from OCR crew
3. `aggregated_output.txt` - Consolidated text output
4. Airtable database entries for structured data

## Current Status

- ✅ Multi-model text extraction
- ✅ Document classification
- ✅ Text aggregation
- ✅ Airtable integration
- ✅ ETL processing (in development)

## Support

For support:
- GitHub Issues
- [Documentation](link_to_your_docs)

## License

[Your chosen license]
