from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class Concept(BaseModel):
    title: str = Field(description="The title of the concept")
    summary: str = Field(description="A detailed summary of the concept")
    related_concepts: List[str] = Field(description="List of related concepts mentioned in the text")

class ConceptExtractor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=300,
            length_function=len
        )
        self.parser = PydanticOutputParser(pydantic_object=Concept)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at identifying and extracting distinct concepts from text.
            For the given text, identify a single main concept and create a wiki-style summary.
            Focus on making the concept atomic and self-contained.
            
            {format_instructions}"""),
            ("user", "{text}")
        ])
    
    def extract_concepts(self, text: str) -> List[Dict]:
        """Extract distinct concepts from the text."""
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        concepts = []
        
        # Process each chunk to extract concepts
        for chunk in chunks:
            try:
                messages = self.prompt.format_messages(
                    text=chunk,
                    format_instructions=self.parser.get_format_instructions()
                )
                response = self.llm.invoke(messages)
                concept = self.parser.parse(response.content)
                concepts.append(concept.model_dump())
            except Exception as e:
                print(f"Error processing chunk: {e}")
                continue
        
        # Remove duplicate concepts based on title similarity
        unique_concepts = self._deduplicate_concepts(concepts)
        return unique_concepts
    
    def _deduplicate_concepts(self, concepts: List[Dict]) -> List[Dict]:
        """Remove duplicate concepts based on title similarity."""
        seen_titles = set()
        unique_concepts = []
        
        for concept in concepts:
            title = concept["title"].lower()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_concepts.append(concept)
        
        return unique_concepts 