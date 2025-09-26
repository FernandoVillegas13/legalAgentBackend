from langchain.tools import tool
from application.use_cases.generate_document_use_case import GenerateDocumentUseCase
import asyncio
import traceback

@tool
def envio_documento_whatsapp_pdf(texto_documento: str, nombre_documento: str = None) -> str:
    """
    Función para generar un PDF con el texto proporcionado
    Args:
        texto_documento: Contenido del documento que se convertirá en PDF
        nombre_documento: Nombre opcional para el documento (sin extensión)  
    Returns:
        str: Mensaje de resultado de la operación
    """
    print("---------" * 20)
    
    try:
        # Limpiar nombre del documento (sin espacios ni caracteres especiales)
        if nombre_documento:
            nombre_limpio = nombre_documento.replace(" ", "_").replace("-", "_")
            # Remover caracteres especiales
            import re
            nombre_limpio = re.sub(r'[^a-zA-Z0-9_]', '', nombre_limpio)
            print(f"Nombre limpio: '{nombre_limpio}'")
        else:
            nombre_limpio = None
            print("No se proporcionó nombre, se generará automáticamente")
        
        # Initialize use case
        generate_doc_use_case = GenerateDocumentUseCase()
        
        # Execute document generation and sending
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            generate_doc_use_case.execute(texto_documento, nombre_limpio)
        )
        loop.close()
        print(f"Resultado: {result}")
        print("---------" * 20)

        if result["success"]:
            return f"{result['message']}\n📄 Documento: {result['title']}\n🔗 URL: {result['document_url']}"
        else:
            return f"Error: {result['message']} - {result.get('error', '')}"
            
    except Exception as e:
        print(f"Traceback completo: {traceback.format_exc()}")
        return f"Error inesperado al generar el documento: {str(e)}"