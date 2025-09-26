from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
import os
import re

from domain.services.pdf_generator import PDFGenerator

class ReportLabPDFGenerator(PDFGenerator):
    
    def _convert_markdown_to_reportlab(self, text: str) -> str:
        # Convert **bold** to <b>bold</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Convert *italic* to <i>italic</i>
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        
        # Convert # Header to larger text (optional)
        text = re.sub(r'^# (.*?)$', r'<b><font size="14">\1</font></b>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*?)$', r'<b><font size="12">\1</font></b>', text, flags=re.MULTILINE)
        
        # Convert numbered lists
        text = re.sub(r'^\d+\.\s+(.*)$', r'• \1', text, flags=re.MULTILINE)
        
        # Convert bullet points
        text = re.sub(r'^-\s+(.*)$', r'• \1', text, flags=re.MULTILINE)
        
        return text
    
    def generate_legal_document(self, content: str, title: str = "Agente Legal Tech") -> bytes:
        buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica'
        )
        
        content_style = ParagraphStyle(
            'CustomContent',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=14
        )
        
        # Build PDF content
        story = []
        
        # Header/Logo space (you can add a logo here later)
        story.append(Spacer(1, 12))
        
        # Title
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Subtitle with date
        current_date = datetime.now().strftime("%d de %B de %Y")
        subtitle = f"Documento generado el {current_date}"
        story.append(Paragraph(subtitle, subtitle_style))
        story.append(Spacer(1, 24))
        
        # Content - Convert markdown and split into paragraphs
        markdown_content = self._convert_markdown_to_reportlab(content)
        paragraphs = markdown_content.split('\n\n')
        
        for paragraph in paragraphs:
            if paragraph.strip():
                # Handle line breaks within paragraphs
                formatted_paragraph = paragraph.strip().replace('\n', '<br/>')
                story.append(Paragraph(formatted_paragraph, content_style))
                story.append(Spacer(1, 12))
        
        # Footer space
        story.append(Spacer(1, 24))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica-Oblique'
        )
        
        footer_text = "Documento generado por Agente Legal Tech"
        story.append(Paragraph(footer_text, footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
