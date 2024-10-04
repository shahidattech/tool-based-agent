
from app.models.backup_schema import CustomerDetails
from app.service.initMongoClient import MongoDBServiceDocs
from app.service.docs.prepare_dmv_docs import generate_contract_pdf
file_path='customer_contract.pdf'
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.logging import logger
import os


class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceDocs()

async def create_document(customer_details: CustomerDetails, mongoDalService: MongoDBServiceDocs) -> JSONResponse:
    """
    Create a new document
    """
    try:
        logger.info(f"=====Creating document====={customer_details.dict()}")
        customer_details_dict = customer_details.dict()
        file_base = os.getenv("FILE_BASE_PATH")
        # Remove spaces from full name to create file name and make it lowercase
        removed_space_fullname  = customer_details_dict["full_name"].replace(" ", "").lower()
        file_name = f"{removed_space_fullname}_contract.pdf"
        file_path = f"{file_base}{file_name}"

        document_path =  await generate_contract_pdf(customer_details_dict, file_path)
        customer_details_dict["document_url"] = document_path
        customer_details_dict["signing_status"] = "PENDING"

        document_id = mongoDalService.mognoDal.post(jsonable_encoder(customer_details_dict))
        logger.info(f"Document created with document_ID: {document_id}")
        if document_path:
            return JSONResponse(content={"document_ID": str(document_id),
                                         "document_name": file_name}, status_code=status.HTTP_201_CREATED)
        return JSONResponse(content={"message": "Document not created"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        return JSONResponse(content={"message": "Error creating document"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)