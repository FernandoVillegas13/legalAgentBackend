import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from .tools.search_jurisprudencia import get_jurisprudencia_sources, clear_jurisprudencia_sources
from domain.entities.agente_response import AgentResponse, Source
from .tools.search_jurisprudencia import search_jurisprudencia
from .tools.envio_documento import envio_documento_whatsapp_pdf
from .tools.duckduckgo_search import buscar_web_duckduckgo, buscar_noticias_duckduckgo
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent

class LangchainAgent:
    def __init__(self, chat_repository=None):
        load_dotenv()
        
        with open("infraestructure/ai/prompt/system_prompt_agente.txt", "r") as file:
            self.system_prompt = file.read()
        
        # Inyectar dependencia del repositorio
        self.chat_repository = chat_repository
        
        # Crear agente sin memoria persistente
        self.agente = self.crear_agente_sin_memoria()

    async def process_message(self, message_content: str, session_id: str) -> AgentResponse:
        try:
            clear_jurisprudencia_sources()
            
            # 1. Obtener historial de conversación
            historial = await self.get_chat_history(session_id)
            
            # 2. Construir prompt con historial
            full_prompt = self.build_prompt_with_history(historial, message_content)
            
            print(f"Full prompt: {full_prompt}")
            # 3. Procesar mensaje
            resultado = self.agente.invoke({
                "messages": [HumanMessage(content=full_prompt)]
            })

            respuesta_final = resultado["messages"][-1].content
            sources = self.get_sources_from_tools()
            print(f"Sources: {sources}")
            
            return AgentResponse(content=respuesta_final, sources=sources)

        except Exception as e:
            clear_jurisprudencia_sources()
            print(f"Error al procesar el mensaje: {e}")
            return AgentResponse(content="Error al procesar el mensaje:" + str(e), sources=[])

    async def get_chat_history(self, session_id: str) -> List[dict]:
        if not self.chat_repository:
            return []
        try:
            return await self.chat_repository.get_recent_messages(session_id, limit=6)
        except Exception as e:
            print(f"Error obteniendo historial: {e}")
            return []

    def build_prompt_with_history(self, history: List[dict], current_message: str) -> str:
        
        prompt_parts = [self.system_prompt]
        
        if history:
            prompt_parts.append("\n<conversation_history>")
            prompt_parts.append("[")
            for i, msg in enumerate(history):
                role = "user" if msg["sender"] == "user" else "assistant"
                content = msg["content"].replace('"', '\\"')  # Escapar comillas
                prompt_parts.append(f'  {{"role": "{role}", "content": "{content}"}},')
            # Remover la última coma
            if prompt_parts[-1].endswith(','):
                prompt_parts[-1] = prompt_parts[-1][:-1]
            prompt_parts.append("]")
            prompt_parts.append("</conversation_history>")
            prompt_parts.append("\nUsa esta conversación pasada como contexto de referencia. Responde al mensaje actual. Si pregunta sobre el historial, consulta la conversación previa proporcionada.")
        
        prompt_parts.append(f"\nMensaje actual del usuario: {current_message}")
        
        return "\n".join(prompt_parts)

    def crear_agente_sin_memoria(self):        
        model = ChatOpenAI(model="gpt-4.1", temperature=0)
        herramientas = [
            search_jurisprudencia, 
            envio_documento_whatsapp_pdf,
            buscar_web_duckduckgo,
            buscar_noticias_duckduckgo
        ]
        
        # Sin checkpointer (sin memoria)
        return create_react_agent(model, herramientas)
    
    def get_sources_from_tools(self) -> List[Source]:
        sources = []

        jurisprudencia_sources = get_jurisprudencia_sources()
        for source_data in jurisprudencia_sources:
            source = Source(
                title=source_data["title"],
                excerpt=source_data["excerpt"],
                source_type=source_data["type"],
                url=source_data.get("url")
            )
            sources.append(source)
        return sources