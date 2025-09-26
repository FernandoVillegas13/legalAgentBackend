from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel

class AgentResponse:
    def __init__(self, content: str, sources: Optional[List['Source']] = None):
        self.content = content
        self.sources = sources or []
        self.created_at = datetime.now()
        self.response_id = str(uuid.uuid4())

class Source:
    def __init__(self, title: str, excerpt: str, source_type: str, url: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.excerpt = excerpt
        self.type = source_type
        self.url = url
