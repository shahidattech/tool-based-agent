from fastapi import APIRouter, Depends, HTTPException

from app.api.v1.endpoints import deals
from app.api.v1.endpoints import verify
from app.api.v1.endpoints import payment
from app.api.v1.endpoints import document_management as document_router

router = APIRouter()

router.include_router(deals.router, tags=["Deals"], prefix="/deals")
router.include_router(verify.router, tags=["Verification"], prefix="/verify")
router.include_router(payment.router, tags=["Loan Management"], prefix="/loan-package")
router.include_router(document_router.router, tags=["Document Management"], prefix="/document-management")