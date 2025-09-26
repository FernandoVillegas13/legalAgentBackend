from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
from typing import List, Optional
from application.use_cases.create_chat_use_case import CreateChatUseCase

router = APIRouter()

class ChatCreate(BaseModel):
    title: Optional[str] = "Nueva conversación"
    category: Optional[str] = None
    tags: List[str] = []

class ChatResponse(BaseModel):
    id: str
    title: str
    category: Optional[str] = None
    tags: List[str] = []
    timestamp: datetime
    is_pinned: bool = False

@router.post("/chats", response_model=ChatResponse)
async def create_chat(chat_data: ChatCreate):
    try:
        use_case = CreateChatUseCase()
        chat = await use_case.execute(
            title=chat_data.title,
            category=chat_data.category,
            tags=chat_data.tags
        )
        
        return ChatResponse(
            id=chat.session_id,
            title=chat.title,
            category=chat.category,
            tags=chat.tags,
            timestamp=chat.created_at,
            is_pinned=chat.is_pinned
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chats", response_model=List[ChatResponse])
async def get_all_chats():
    try:
        use_case = CreateChatUseCase()
        chats = await use_case.get_all_chats()
        
        return [
            ChatResponse(
                id=chat.session_id,
                title=chat.title,
                category=chat.category,
                tags=chat.tags,
                timestamp=chat.created_at,
                is_pinned=chat.is_pinned
            )
            for chat in chats
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/chats/{chat_id}", response_model=ChatResponse)
async def update_chat(chat_id: str, chat_data: ChatCreate):
    try:
        use_case = CreateChatUseCase()
        
        # Obtener chat existente
        existing_chat = await use_case.get_chat_by_id(chat_id)
        if not existing_chat:
            raise HTTPException(status_code=404, detail="Chat no encontrado")
        
        # Actualizar campos
        existing_chat.title = chat_data.title or existing_chat.title
        existing_chat.category = chat_data.category
        existing_chat.tags = chat_data.tags
        
        # Guardar cambios
        updated_chat = await use_case.update_chat(existing_chat)
        
        return ChatResponse(
            id=updated_chat.session_id,
            title=updated_chat.title,
            category=updated_chat.category,
            tags=updated_chat.tags,
            timestamp=updated_chat.created_at,
            is_pinned=updated_chat.is_pinned
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))