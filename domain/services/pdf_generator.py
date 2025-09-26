from abc import ABC, abstractmethod
from typing import Dict, Any
from io import BytesIO

class PDFGenerator(ABC):
    """Abstract service for PDF generation"""
    
    @abstractmethod
    def generate_legal_document(self, content: str, title: str = "Agente Legal Tech") -> bytes:
        """Generate a PDF document with legal content"""
        pass

class PDFGeneratorService:
    """Domain service for PDF generation business logic"""
    
    def __init__(self, pdf_generator: PDFGenerator):
        self.pdf_generator = pdf_generator
    
    def create_legal_document(self, content: str, document_name: str = "documento_legal") -> Dict[str, Any]:
        """Create a legal document with proper formatting and metadata"""
        # Business logic for document creation
        formatted_title = "Agente Legal Tech - Documento Jurídico"
        
        # Generate PDF bytes
        pdf_bytes = self.pdf_generator.generate_legal_document(content, formatted_title)
        
        return {
            "pdf_bytes": pdf_bytes,
            "filename": f"{document_name}.pdf",
            "title": formatted_title,
            "content_length": len(pdf_bytes)
        }
