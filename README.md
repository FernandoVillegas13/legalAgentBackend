# BackendLegalAgent

Intelligent legal assistant backend built with Python, FastAPI, and LangChain/LangGraph, 
specialized in Peruvian law. It provides automated legal advice, case law retrieval, 
legal document generation via WhatsApp, and queries to external sources 
(DuckDuckGo, legal APIs).  

## Key Features
- **Architecture:** FastAPI + PostgreSQL + LangChain + LangGraph  (Hexagonal!!!!!)
- **Main Agent:** ReAct agent with GPT-4o-mini optimized for Peruvian legal domain  
- **Integrated Tools:**
  - `search_jurisprudencia`: query external case law API  
  - `envio_documento_whatsapp_pdf`: generate & send legal PDFs via WhatsApp  
  - `buscar_web_duckduckgo`: search for updated legal regulations  
  - `buscar_noticias_duckduckgo`: fetch relevant legal news  
- **Persistence:** PostgreSQL for sessions and source management  
- **External Integrations:** OpenAI, AWS S3, Twilio, DuckDuckGo  

## API Endpoints

### 💬 Chat Management
- `POST /api/chats` - Create new chat session
- `GET /api/chats` - Get all chat sessions
- `PUT /api/chats/{chat_id}` - Update chat session

### 📝 Message Management
- `POST /api/chats/{chat_id}/messages` - Send message to agent
- `GET /api/chats/{chat_id}/messages` - Get chat message history

### 🏥 Health Check
- `GET /health` - API health status

## 🚀 Deployment Instructions

### 📋 Prerequisites
- 🐍 Python 3.8+
- 🐳 Docker & Docker Compose
- 🔑 API Keys: OpenAI, AWS, Twilio, LangChain

### 🛠️ Step 1: Environment Setup

1. **Configure environment variables in `.env`:**
   ```env
   # API Configuration
   FASTAPI_HOST=0.0.0.0
   FASTAPI_PORT=8000
   DEBUG=True

   # OpenAI API
   OPENAI_API_KEY=your_openai_api_key_here

   # Database
   POSTGRES_DB=chatbot_legal_db
   POSTGRES_USER=chatbot_user
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   DATABASE_URL=postgresql://chatbot_user:your_secure_password@localhost:5432/chatbot_legal_db

   # AWS S3
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=us-east-1
   AWS_BUCKET_NAME=your_bucket_name

   # Twilio (for WhatsApp)
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token

   # CORS

   # Security
   SECRET_KEY=your_super_secret_key_here
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

### 🐳 Step 2: Database Setup

2. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d postgres
   ```

3. **Create database tables:**
   ```bash
   python create_tables.py
   ```

### 🐍 Step 3: Python Environment

4. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🔥 Step 4: Run the Application

**Option A: Direct Python execution**
```bash
python main.py
```

**Option B: Using uvicorn**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Option C: Using Docker Compose (Full Stack)**
```bash
docker-compose up -d --build
```

### 🌐 Step 5: Verify Deployment

1. **Check API health:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 🔒 Security Considerations

- 🔐 Use strong passwords for database
- 🛡️ Keep API keys secure and never commit them
- 🌐 Configure CORS origins appropriately for production
- 🔑 Use environment-specific secrets management

### 📊 Monitoring & Logs

- 📈 LangChain tracing enabled for debugging
- 📋 Console logs for request/response tracking
- 🐳 Docker logs: `docker-compose logs -f`


## 📁 Project Structure

```
legalAgentBackend/
├── 🐳 docker-compose.yml          # Container orchestration
├── 🐍 main.py                     # FastAPI application entry
├── 🗄️ create_tables.py            # Database schema setup
├── 📦 requirements.txt            # Python dependencies
├── 🔧 env.example                 # Environment template
├── 📚 application/                # Use cases layer
│   └── use_cases/
├── 🏛️ domain/                     # Business logic layer
│   ├── entities/                  # Domain models
│   └── services/                  # Domain services
└── 🏗️ infraestructure/            # Infrastructure layer
    ├── 🌐 api/                    # REST API routes
    ├── 🤖 ai/                     # LangChain agent & tools
    ├── 🔗 external/               # External service integrations
    └── 💾 persistencia/           # Database repositories
```
