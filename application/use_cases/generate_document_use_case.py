from domain.services.pdf_generator import PDFGeneratorService
from infraestructure.external.pdf_generator_impl import ReportLabPDFGenerator
from infraestructure.external.aws_services import S3Client
from infraestructure.external.twilio import Twilio
from typing import Dict, Any
import uuid
import traceback
import os

class GenerateDocumentUseCase:    
    def __init__(self):
        pdf_generator = ReportLabPDFGenerator()
        self.pdf_service = PDFGeneratorService(pdf_generator)
        self.s3_client = S3Client()
        self.twilio = Twilio()
    
    async def execute(self, content: str, document_name: str = None) -> Dict[str, Any]:
        try:
            # 1. Generate document name if not provided
            if not document_name:
                document_name = f"documento_legal_{uuid.uuid4().hex[:8]}"
            
            # 2. Generate PDF document
            document_data = self.pdf_service.create_legal_document(content, document_name)
            
            # 3. Upload to S3
            filename = f"legal_docs/{document_data['filename']}"
            public_url = self.s3_client.upload_file(
                file=document_data['pdf_bytes'],
                file_name=filename
            )
            
            # 4. Send via WhatsApp
            message = f"Documento legal generado: {document_data['title']}"
            self.twilio.send_message(message, public_url)
            
            result = {
                "success": True,
                "document_url": public_url,
                "filename": document_data['filename'],
                "title": document_data['title'],
                "message": "Documento generado y enviado correctamente"
            }
            return result
            
        except Exception as e:
            
            error_result = {
                "success": False,
                "error": str(e),
                "message": "Error al generar o enviar el documento"
            }
            return error_result
