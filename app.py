import streamlit as st
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import os

from src.pdf_processor import PDFProcessor
from src.concept_extractor import ConceptExtractor
from src.markdown_generator import MarkdownGenerator

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="PDF Concept Extractor",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 PDF Concept Extractor")
st.markdown("""
Upload a PDF document and get a wiki-style summary of the key concepts contained within.
Each concept will be extracted and presented in an easy-to-read format with related concepts linked.
""")

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API key not found! Please set it in your .env file.")
    st.stop()

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = Path(tmp_file.name)
        
        try:
            # Initialize components
            pdf_processor = PDFProcessor()
            concept_extractor = ConceptExtractor()
            markdown_generator = MarkdownGenerator()
            
            # Process PDF
            with st.status("Reading PDF...") as status:
                text_content = pdf_processor.extract_text(tmp_path)
                status.update(label="Extracting concepts...", state="running")
                concepts = concept_extractor.extract_concepts(text_content)
                status.update(label="Generating summary...", state="running")
                
                # Create output directory if it doesn't exist
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                
                # Generate and save markdown
                output_path = output_dir / f"{uploaded_file.name.replace('.pdf', '')}_concepts.md"
                markdown_generator.generate(concepts, output_path)
                status.update(label="Done!", state="complete")
            
            # Display results
            st.success(f"✅ Successfully processed PDF and extracted {len(concepts)} concepts!")
            
            # Display concepts in expandable sections
            for concept in concepts:
                with st.expander(f"📖 {concept['title']}", expanded=True):
                    st.markdown(concept['summary'])
                    if concept['related_concepts']:
                        st.markdown("### Related Concepts")
                        for related in concept['related_concepts']:
                            st.markdown(f"- {related}")
            
            # Download button for markdown file
            with open(output_path, 'r') as f:
                markdown_content = f.read()
                st.download_button(
                    label="📥 Download Markdown Summary",
                    data=markdown_content,
                    file_name=output_path.name,
                    mime="text/markdown"
                )
        
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            tmp_path.unlink()

# Add helpful instructions in the sidebar
with st.sidebar:
    st.markdown("""
    ### Instructions
    1. Make sure you have set your OpenAI API key in the `.env` file
    2. Upload a PDF document using the file uploader
    3. Wait for the processing to complete
    4. View the extracted concepts in the expandable sections
    5. Download the complete markdown summary if desired
    
    ### About
    This tool uses:
    - LangChain for document processing
    - GPT-4 for concept extraction
    - Streamlit for the user interface
    """) 