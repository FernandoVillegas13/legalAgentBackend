from domain.entities.chat_session import ChatSession
from domain.services.chat_repository import ChatRepository
from infraestructure.persistencia.postgres_chat_repository import PostgresChatRepository
from typing import List, Optional
import uuid

class CreateChatUseCase:
    def __init__(self):
        self.chat_repository: ChatRepository = PostgresChatRepository()

    async def execute(self, title: str = "Nueva conversación", category: Optional[str] = None, tags: List[str] = []) -> ChatSession:
        # Crear nuevo chat con UUID único
        chat_id = str(uuid.uuid4())
        
        chat = ChatSession(session_id=chat_id, user_id="default")
        chat.title = title
        chat.category = category
        chat.tags = tags
        chat.is_pinned = False
        
        # Guardar en base de datos
        saved_chat = await self.chat_repository.save_chat(chat)
        
        return saved_chat
    
    async def get_all_chats(self) -> List[ChatSession]:
        return await self.chat_repository.get_all_chats()

    async def get_chat_by_id(self, chat_id: str) -> Optional[ChatSession]:
        return await self.chat_repository.get_chat_by_id(chat_id)

    async def update_chat(self, chat: ChatSession) -> ChatSession:
        return await self.chat_repository.save_chat(chat)