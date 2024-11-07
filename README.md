# GenerixOCR - Automated Document Processing AI

GenerixOCR is an intelligent document processing system powered by [crewAI](https://crewai.com) that automates the extraction and classification of text from business documents. Our AI-powered crew handles the complete document processing pipeline, from initial scanning to structured data output.

## What It Does

Our automated document processing AI specializes in:
- Automated text extraction from document images
- Intelligent document type classification
- Data structuring and validation
- Processing of various business documents including:
  - Invoices (Factures)
  - Delivery Notes (Bons de livraison)
  - Reception Notes (Bons de reception)
  - Purchase Orders
  - And other business documents

## Key Features

- **Automated Document Processing**: Full automation of document handling workflow
- **Intelligent OCR**: High-accuracy text extraction using advanced AI models
- **Smart Classification**: Automatic identification of document types and content
- **Multi-Language Support**: Process documents in multiple languages
- **Structured Output**: Convert unstructured document data into structured formats
- **Quality Assurance**: Built-in validation checks for extracted data
- **Scalable Architecture**: Process multiple documents simultaneously

## Installation

### Prerequisites

- Python >=3.10 <=3.13
- [Poetry](https://python-poetry.org/) for dependency management

### Setup

1. Install Poetry if you haven't already:
```bash
pip install poetry
```

2. Clone and install:
```bash
git clone https://github.com/yourusername/generix_ocr.git
cd generix_ocr
poetry install
```

3. Environment setup:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

## Usage

Start the automated processing:

```bash
poetry run crewai run
```

### Supported Input Formats

The AI crew can process:
- PNG images
- JPEG images
- PDF documents
- TIFF files
- Scanned documents

### Output Formats

The system generates:
- Structured text extraction
- Document classification results
- Validated data in processable format
- Optional: JSON/CSV exports

## System Architecture

```
generix_ocr/
├── src/
│   └── generix_ocr/
│       ├── crews/
│       │   ├── ocr_crew/         # Document processing agents
│       │   └── write_x_crew/     # Data formatting agents
│       ├── pipelines/            # Processing workflows
│       └── tools/                # Specialized processing tools
└── config/                       # AI crew configurations
```

## Configuration

Customize your AI crew:
- `src/generix_ocr/crews/ocr_crew/config/agents.yaml` - Agent roles and capabilities
- `src/generix_ocr/crews/ocr_crew/config/tasks.yaml` - Processing workflow definitions

## Contributing

We welcome contributions to improve the automated document processing capabilities!

## License

[Your chosen license]

## Support

Get help:
- GitHub Issues
- [crewAI documentation](https://docs.crewai.com)
- [crewAI Discord](https://discord.com/invite/X4JWnZnxPb)

## Acknowledgments

Built with [crewAI](https://crewai.com) - Empowering AI agent orchestration for automated document processing.
