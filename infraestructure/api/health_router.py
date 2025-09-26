from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy",
            "message": "Legal Tech Backend",
            "timestamp": datetime.now().isoformat()
            }