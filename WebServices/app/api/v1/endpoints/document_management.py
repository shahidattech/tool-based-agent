from fastapi import APIRouter, Depends, HTTPException, Query
from app.service.initMongoClient import MongoDBServiceDocs
import  app.controllers.docCtrl as docCtrl
from typing import Optional
from app.models.backup_schema import CustomerDetails, CustomerDetailsToGenerateDocument
from fastapi.responses import FileResponse
import os


router = APIRouter()

class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceDocs()

@router.post("/")
async def create_document(customer_details: CustomerDetailsToGenerateDocument, mongoDalService: MongoDalService = Depends(MongoDalService)):
    """
    Create a new document
    """
    return await docCtrl.create_document(customer_details, mongoDalService)


@router.get("/download/{file_name}", response_class=FileResponse)
async def download_file(file_name: str):
    """
    Endpoint to download a file saved in the container
    """
    file_base = os.getenv("FILE_BASE_PATH")
    file_path = f"{file_base}/{file_name}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path=file_path, filename=file_name, media_type='application/pdf')
