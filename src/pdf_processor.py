from pathlib import Path
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def extract_text(self, pdf_path: Path) -> str:
        """Extract text from PDF and split into manageable chunks."""
        reader = PdfReader(str(pdf_path))
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        
        # Clean the text
        text = self._clean_text(text)
        
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove multiple newlines
        text = "\n".join(line.strip() for line in text.split("\n") if line.strip())
        # Remove multiple spaces
        text = " ".join(text.split())
        return text 