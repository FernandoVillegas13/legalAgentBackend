# BackendLegalAgent

Intelligent legal assistant backend built with Python, FastAPI, and LangChain/LangGraph, 
specialized in Peruvian law. It provides automated legal advice, case law retrieval, 
legal document generation via WhatsApp, and queries to external sources 
(DuckDuckGo, legal APIs).  

## Key Features
- **Architecture:** FastAPI + PostgreSQL + LangChain + LangGraph  
- **Main Agent:** ReAct agent with GPT-4o-mini optimized for Peruvian legal domain  
- **Integrated Tools:**
  - `search_jurisprudencia`: query external case law API  
  - `envio_documento_whatsapp_pdf`: generate & send legal PDFs via WhatsApp  
  - `buscar_web_duckduckgo`: search for updated legal regulations  
  - `buscar_noticias_duckduckgo`: fetch relevant legal news  
- **Persistence:** PostgreSQL for sessions and source management  
- **External Integrations:** OpenAI, AWS S3, Twilio, DuckDuckGo  

## Status
Project under development as part of a **Technical Report on AI Specialization**.
