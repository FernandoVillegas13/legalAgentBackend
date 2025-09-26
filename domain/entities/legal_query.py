from datetime import datetime
import uuid
from pydantic import BaseModel

class LegalQuery:
    def __init__(self, query: str, legal_area: str):
        self.query = query
        self.legal_area = legal_area  # "laboral", "civil", "penal", "comercial"
        self.keywords = []
        self.complexity_level = "basic"  # "basic", "intermediate", "complex"
        self.requires_tools = []  # ["jurisprudencia", "codigo_civil", etc.]
        self.timestamp = datetime.now()