import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv("POSTGRES_HOST"),
    'port': os.getenv("POSTGRES_PORT"),
    'database': os.getenv("POSTGRES_DATABASE"),
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD")
}

def create_tables():
    
    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS chats (
        id VARCHAR(255) PRIMARY KEY,
        title VARCHAR(500) NOT NULL,
        category VARCHAR(100),
        tags TEXT[],
        last_message TEXT,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        is_pinned BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS messages (
        id VARCHAR(255) PRIMARY KEY,
        chat_id VARCHAR(255) NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
        content TEXT NOT NULL,
        sender VARCHAR(20) NOT NULL CHECK (sender IN ('user', 'agent')),
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS sources (
        id VARCHAR(255) PRIMARY KEY,
        message_id VARCHAR(255) NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
        title VARCHAR(500) NOT NULL,
        url TEXT,
        excerpt TEXT NOT NULL,
        type VARCHAR(50) NOT NULL CHECK (type IN ('document', 'web', 'database'))
    );
    """

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(create_tables_sql)
        conn.commit()
        
        print("Tablas creadas exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_tables()
