from datetime import datetime
from typing import List, Optional
import uuid

class Message:
    def __init__(self, content: str, sender: str, timestamp: datetime, chat_id: str):
        self.id = str(uuid.uuid4())
        self.content = content
        self.sender = sender
        self.chat_id = chat_id
        self.timestamp = timestamp
        self.sources = []  # Lista de fuentes para mensajes del agente

