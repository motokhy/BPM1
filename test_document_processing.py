import os
from backend.document_processor import DocumentProcessor
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_document_processing():
    try:
        # Initialize document processor
        processor = DocumentProcessor()
        logger.info("DocumentProcessor initialized successfully")

        # Test file path
        test_file = os.path.join(os.path.dirname(__file__), 'test_docs', 'sample_process.txt')
        
        # Convert text file to PDF for testing
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        with open(test_file, 'r') as file:
            for line in file:
                pdf.cell(200, 10, txt=line.strip(), ln=True)
        
        pdf_path = os.path.join(os.path.dirname(__file__), 'test_docs', 'sample_process.pdf')
        pdf.output(pdf_path)
        logger.info(f"Created test PDF at: {pdf_path}")

        # Process the PDF
        logger.info("Starting document processing test")
        result = processor.process_document(pdf_path, 'pdf')
        logger.info("Document processed successfully")
        logger.info(f"Result: {result}")
        
        return True

    except Exception as e:
        logger.error(f"Test failed: {str(e)}", exc_info=True)
        return False

if __name__ == "__main__":
    test_document_processing()
