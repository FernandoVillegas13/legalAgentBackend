from datetime import datetime
from typing import List, Optional

class ChatSession:
    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.messages = []
        self.created_at = datetime.now()
        # Campos para la persistencia
        self.title = "Nueva conversación"
        self.category = None
        self.tags = []
        self.last_message = None
        self.is_pinned = False