from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infraestructure.api.message_router import router as message_router
from infraestructure.api.health_router import router as health_router
from infraestructure.api.chat_router import router as chat_router
import uvicorn

def create_app():
    app = FastAPI(
        title="Chatbot Legal API",
        version="1.0.0",
        description="API for the Chatbot Legal",
        docs_url="/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(message_router, prefix="/api")
    app.include_router(chat_router, prefix="/api")  # NUEVA LÍNEA
    app.include_router(health_router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)