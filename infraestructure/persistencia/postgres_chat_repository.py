import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from datetime import datetime
from domain.services.chat_repository import ChatRepository
from domain.entities.message import Message
from domain.entities.chat_session import ChatSession
import os
from dotenv import load_dotenv

load_dotenv()

class PostgresChatRepository(ChatRepository):
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv("POSTGRES_HOST"),
            'port': os.getenv("POSTGRES_PORT"),
            'database': os.getenv("POSTGRES_DATABASE"),
            'user': os.getenv("POSTGRES_USER"),
            'password': os.getenv("POSTGRES_PASSWORD")
        }
    
    def _get_connection(self):
        return psycopg2.connect(**self.connection_params)
    
    async def save_chat(self, chat: ChatSession) -> ChatSession:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO chats (id, title, category, tags, last_message, timestamp, is_pinned)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        last_message = EXCLUDED.last_message,
                        timestamp = EXCLUDED.timestamp
                """, (
                    chat.session_id,
                    getattr(chat, 'title', 'Nueva conversación'),
                    getattr(chat, 'category', None),
                    getattr(chat, 'tags', []),
                    getattr(chat, 'last_message', None),
                    datetime.now(),
                    getattr(chat, 'is_pinned', False)
                ))
                conn.commit()
                return chat
        finally:
            conn.close()
    
    async def get_chat_by_id(self, chat_id: str) -> Optional[ChatSession]:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM chats WHERE id = %s", (chat_id,))
                row = cursor.fetchone()
                if row:
                    chat = ChatSession(session_id=row['id'], user_id='default')
                    chat.title = row['title']
                    chat.category = row['category']
                    chat.tags = row['tags'] or []
                    chat.last_message = row['last_message']
                    chat.is_pinned = row['is_pinned']
                    return chat
                return None
        finally:
            conn.close()
    
    async def save_message(self, message: Message) -> Message:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO messages (id, chat_id, content, sender, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    message.id,
                    message.chat_id,
                    message.content,
                    message.sender,
                    message.timestamp
                ))
                # Guardar fuentes si las hay
                for source in message.sources:
                    cursor.execute("""
                        INSERT INTO sources (id, message_id, title, url, excerpt, type)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        source.id,
                        message.id,
                        source.title,
                        source.url,
                        source.excerpt,
                        source.type
                    ))
                conn.commit()
                return message
        except Exception as e:
            print(f"Error al guardar el mensaje: {e}")
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    async def get_messages_by_chat_id(self, chat_id: str) -> List[Message]:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM messages 
                    WHERE chat_id = %s 
                    ORDER BY timestamp ASC
                """, (chat_id,))
                
                messages = []
                for row in cursor.fetchall():
                    message = Message(
                        content=row['content'],
                        sender=row['sender'],
                        timestamp=row['timestamp'],
                        chat_id=row['chat_id']
                    )
                    message.id = row['id']
                    
                    # Cargar sources para este mensaje
                    cursor.execute("""
                        SELECT id, title, url, excerpt, type
                        FROM sources 
                        WHERE message_id = %s
                        ORDER BY id ASC
                    """, (message.id,))
                    
                    sources_rows = cursor.fetchall()
                    
                    # Crear objetos Source y agregarlos al mensaje
                    from domain.entities.agente_response import Source
                    for source_row in sources_rows:
                        source = Source(
                            title=source_row['title'],
                            excerpt=source_row['excerpt'],
                            source_type=source_row['type'],
                            url=source_row['url']
                        )
                        source.id = source_row['id']
                        message.sources.append(source)
                    
                    messages.append(message)
                
                return messages
        finally:
            conn.close()
    
    async def get_all_chats(self) -> List[ChatSession]:
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM chats ORDER BY timestamp DESC")
                
                chats = []
                for row in cursor.fetchall():
                    chat = ChatSession(session_id=row['id'], user_id='default')
                    chat.title = row['title']
                    chat.category = row['category']
                    chat.tags = row['tags'] or []
                    chat.last_message = row['last_message']
                    chat.is_pinned = row['is_pinned']
                    chats.append(chat)
                
                return chats
        finally:
            conn.close()

    async def get_recent_messages(self, chat_id: str, limit: int = 6) -> List[dict]:
        """Obtiene el historial simple para construir el prompt"""
        conn = self._get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT LEFT(content, 300) as content, sender
                    FROM messages 
                    WHERE chat_id = %s 
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (chat_id, limit))
                
                rows = cursor.fetchall()
                # Invertir para orden cronológico y devolver diccionarios simples
                return [{"content": row["content"], "sender": row["sender"]} 
                       for row in reversed(rows)]
                
        finally:
            conn.close()