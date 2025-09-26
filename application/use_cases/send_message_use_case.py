from domain.entities.agente_response import AgentResponse
from domain.entities.message import Message
from domain.services.chat_repository import ChatRepository
from infraestructure.ai.langchain_agent import LangchainAgent
from infraestructure.persistencia.postgres_chat_repository import PostgresChatRepository
from datetime import datetime

class SendMessageUseCase:
    def __init__(self):
        self.chat_repository: ChatRepository = PostgresChatRepository()
        self.langchain_agent = LangchainAgent(chat_repository=self.chat_repository)

    async def execute(self, message_content: str, session_id: str) -> AgentResponse:
        # 1. Generar respuesta del agente (ANTES de guardar el mensaje del usuario)
        agent_response = await self.langchain_agent.process_message(message_content, session_id)
        
        # 2. Guardar mensaje del usuario
        user_message = Message(
            content=message_content,
            sender="user",
            timestamp=datetime.now(),
            chat_id=session_id
        )
        await self.chat_repository.save_message(user_message)
        
        # 3. Guardar mensaje del agente
        agent_message = Message(
            content=agent_response.content,
            sender="agent",
            timestamp=datetime.now(),
            chat_id=session_id
        )
        # Agregar fuentes al mensaje
        agent_message.sources = agent_response.sources
        await self.chat_repository.save_message(agent_message)
        
        return agent_response