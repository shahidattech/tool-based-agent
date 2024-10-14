from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.endpoints import ai_assistant as assistant

router = APIRouter()
router.include_router(assistant.router, tags=["Fiancial Assistant"])