from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.message import Message
from domain.entities.chat_session import ChatSession

class ChatRepository(ABC):
    
    @abstractmethod
    async def save_chat(self, chat: ChatSession) -> ChatSession:
        pass
    
    @abstractmethod
    async def get_chat_by_id(self, chat_id: str) -> Optional[ChatSession]:
        pass
    
    @abstractmethod
    async def save_message(self, message: Message) -> Message:
        pass
    
    @abstractmethod
    async def get_messages_by_chat_id(self, chat_id: str) -> List[Message]:
        pass
    
    @abstractmethod
    async def get_all_chats(self) -> List[ChatSession]:
        pass