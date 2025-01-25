from pathlib import Path
from typing import List, Dict

class MarkdownGenerator:
    def generate(self, concepts: List[Dict], output_path: Path) -> None:
        """Generate a markdown file from the extracted concepts."""
        markdown_content = self._create_markdown_content(concepts)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    
    def _create_markdown_content(self, concepts: List[Dict]) -> str:
        """Create formatted markdown content from concepts."""
        content = ["# Extracted Concepts\n"]
        
        # Add table of contents
        content.append("## Table of Contents\n")
        for i, concept in enumerate(concepts, 1):
            content.append(f"{i}. [{concept['title']}](#{self._create_anchor(concept['title'])})\n")
        content.append("\n---\n")
        
        # Add concept sections
        for concept in concepts:
            # Add title
            content.append(f"## {concept['title']}\n")
            
            # Add summary
            content.append(f"{concept['summary']}\n")
            
            # Add related concepts if any
            if concept['related_concepts']:
                content.append("\n### Related Concepts\n")
                for related in concept['related_concepts']:
                    content.append(f"- {related}\n")
            
            content.append("\n---\n")
        
        return "\n".join(content)
    
    def _create_anchor(self, title: str) -> str:
        """Create a markdown anchor from a title."""
        return title.lower().replace(' ', '-').replace('/', '') 