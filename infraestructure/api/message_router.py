from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from application.use_cases.send_message_use_case import SendMessageUseCase

router = APIRouter()

class MessageCreate(BaseModel):
    content: str
    attachments: List[str] = []

class Source(BaseModel):
    id: str
    title: str
    url: Optional[str] = None
    excerpt: str
    type: str

class Message(BaseModel):
    id: str
    content: str
    sender: str
    timestamp: datetime
    sources: Optional[List[Source]] = None

class MessageResponse(BaseModel):
    message: Message

@router.post("/chats/{chat_id}/messages", response_model=MessageResponse)
async def send_message(chat_id: str, message_data: MessageCreate):
    try:
        response_data = await generate_agent_response(message_data.content, chat_id)
        agent_message = Message(
            id=str(uuid.uuid4()),
            content=response_data["content"],
            sender="agent",
            timestamp=datetime.now(),
            sources=[
                Source(
                    id=source["id"],
                    title=source["title"],
                    excerpt=source["excerpt"],
                    type=source["type"],
                    url=source.get("url")
                )
                for source in response_data["sources"]
            ]
        )
        print(f"Agent response: {agent_message.content}")
        return MessageResponse(message=agent_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chats/{chat_id}/messages")
async def get_chat_messages(chat_id: str):
    try:
        # Importar aquí para evitar imports circulares
        from infraestructure.persistencia.postgres_chat_repository import PostgresChatRepository
        
        repository = PostgresChatRepository()
        messages = await repository.get_messages_by_chat_id(chat_id)
        
        # Convertir a formato que espera el frontend
        formatted_messages = []
        for message in messages:
            # Convertir sources a formato dict
            sources = [
                {
                    "id": source.id,
                    "title": source.title,
                    "url": source.url,
                    "excerpt": source.excerpt,
                    "type": source.type
                }
                for source in message.sources
            ]
            
            msg_dict = {
                "id": message.id,
                "content": message.content,
                "sender": message.sender,
                "timestamp": message.timestamp.isoformat(),
                "sources": sources
            }
            
            formatted_messages.append(msg_dict)
        
        return {"messages": formatted_messages}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def generate_agent_response(user_message: str, chat_id: str) -> str:
    use_case = SendMessageUseCase()
    agent_response = await use_case.execute(user_message, chat_id)
    return {
        "content": agent_response.content,
        "sources": [
            {
                "id": source.id,
                "title": source.title,
                "excerpt": source.excerpt,
                "type": source.type,
                "url": source.url
            }
            for source in agent_response.sources
        ]
    }
