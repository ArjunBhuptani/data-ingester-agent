# PDF Concept Extractor

An AI-powered tool that processes PDF documents and generates wiki-style concept summaries in markdown format. It uses LangChain and OpenAI to extract and summarize distinct concepts from PDF documents.

## Features

- PDF text extraction and processing
- Concept identification and separation
- Wiki-style markdown summaries
- OpenAI-powered content analysis
- Modern web interface for easy uploads
- Downloadable markdown summaries
- Modular and extensible design

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface (Recommended)

Run the Streamlit app:
```bash
streamlit run app.py
```

This will open a web interface where you can:
1. Upload your PDF files
2. View extracted concepts in real-time
3. Download the markdown summary

### Command Line Interface

Alternatively, you can use the command line interface:
```bash
python main.py path/to/your/pdf
```

The output will be saved in the `output` directory as markdown files, with each concept separated into its own section. 