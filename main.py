#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from rich.progress import Progress

from src.pdf_processor import PDFProcessor
from src.concept_extractor import ConceptExtractor
from src.markdown_generator import MarkdownGenerator

def main():
    load_dotenv()
    
    if len(sys.argv) != 2:
        print("[red]Please provide a PDF file path as an argument[/red]")
        sys.exit(1)
    
    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists() or pdf_path.suffix.lower() != '.pdf':
        print("[red]Invalid PDF file path[/red]")
        sys.exit(1)
    
    console = Console()
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    with Progress() as progress:
        # Initialize components
        pdf_processor = PDFProcessor()
        concept_extractor = ConceptExtractor()
        markdown_generator = MarkdownGenerator()
        
        # Process PDF
        task1 = progress.add_task("[cyan]Reading PDF...", total=1)
        text_content = pdf_processor.extract_text(pdf_path)
        progress.update(task1, completed=1)
        
        # Extract concepts
        task2 = progress.add_task("[green]Extracting concepts...", total=1)
        concepts = concept_extractor.extract_concepts(text_content)
        progress.update(task2, completed=1)
        
        # Generate markdown
        task3 = progress.add_task("[yellow]Generating markdown...", total=1)
        output_path = output_dir / f"{pdf_path.stem}_concepts.md"
        markdown_generator.generate(concepts, output_path)
        progress.update(task3, completed=1)
    
    print(f"[green]✓[/green] Successfully processed PDF and generated concepts at: {output_path}")

if __name__ == "__main__":
    main() 