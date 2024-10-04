from fastapi import APIRouter, Depends
from app.models.schemas import LoanPackage
from app.models.responses import CreateLoanPackageResp, LoanPackageResp
from app.service.initMongoClient import MongoDBServiceLoan
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status
from app.utils.logging import logger
from app.utils.utility import serialize_doc
from typing import Optional


class MongoDalServiceLoan:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceLoan()



router = APIRouter()

@router.post("/", response_model=CreateLoanPackageResp, description="Create a loan package")
async def create_loan_entry(loan: LoanPackage, mongoDalService: MongoDBServiceLoan = Depends(MongoDalServiceLoan)):
    """
    Create a loan entry
    Args:
        loan (LoanPackage): The loan package
    Returns: CommonResp
    """
    try:
        print("=====Creating deal=====")
        logger.info(f"=====Creating loan entry======={loan.dict()}")
        
        payload_dict = loan.dict()
        inserted_coc_id = mongoDalService.mognoDal.post(jsonable_encoder(payload_dict))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = ({
                "status_code": status.HTTP_201_CREATED,
                "message": "Loan entry created successfully",
                "loan_package_id": str(inserted_coc_id)
            })
        )
    except Exception as e:
        logger.error(f"Error creating deal: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = ({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error creating loan entry"
            })
        )

@router.get("/{limit}", description="list All loan packages")
async def list_loan_packages(limit: Optional[int] = None, mongoDalService: MongoDBServiceLoan = Depends(MongoDalServiceLoan)):
    """
    List all loan packages
    Args: mongoDalService
    Returns: JSONResponse
    """
    try:
        logger.info(f"=====list_loan_packages::::Fetching all loan packages=====")
        loan_packages = mongoDalService.mognoDal.get_all_loan_packages(limit)
        if not loan_packages:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = ({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "No loan packages found"
                })
            )
        logger.debug(f"loan_packages: {loan_packages}") 
        json_loan_package = serialize_doc(loan_packages)
        filtered_json_loan_package = filter_loan_providers(json_loan_package)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = LoanPackageResp(
                status_code=status.HTTP_200_OK,
                message="Loan packages fetched successfully",
                data=filtered_json_loan_package
            ).dict()
            )
    except Exception as e:
        logger.error(f"list_loan_packages:: Error fetching loan packages: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = ({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error fetching loan packages"
            })
        )

@router.get("/loans/{loan_package_id}", description="Get a loan package")
async def get_loan_entry(loan_package_id: str, mongoDalService: MongoDBServiceLoan = Depends(MongoDalServiceLoan)):
    """
    Get a loan entry
    Args:
        loan_package_id (str): The loan package id
    Returns: CommonResp
    """
    try:
        logger.info(f"=====Fetching loan entry======={loan_package_id}")
        loan_package = mongoDalService.mognoDal.get_loan_package(loan_package_id)
        if not loan_package:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = ({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Loan entry not found"
                })
            )
                    # Convert ObjectId to string

        json_loan_package = serialize_doc(loan_package)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = ({
                "status_code": status.HTTP_200_OK,
                "message": "Loan entry fetched successfully",
                "data": json_loan_package
            })
        )
    except Exception as e:
        logger.error(f"Error fetching loan entry: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = ({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error fetching loan entry"
            })
        )

def filter_loan_providers(data):
    filtered_data = []
    
    count = 1
    for entry in data:
        logger.debug(f"Count: {count}")
        filtered_entry = {
            "option": count,
            "details": {
                "provider_name": entry.get("provider_name"),
                "provider_phone": entry.get("provider_phone"),
                "package_includes": entry.get("package_includes"),
                "loan_terms_in_months": entry.get("loan_terms_in_months"),
                "interest_rate": entry.get("interest_rate")
            }
        }
        filtered_data.append(filtered_entry)
        count += 1
    
    return filtered_data

@router.get("/loan-by-civil-score/{cibil_score}",  description="Get a loan package by civil score")
async def get_loan_package_by_cibil_score(cibil_score: int, mongoDalService: MongoDBServiceLoan = Depends(MongoDalServiceLoan)):
    """
    Get a loan package by civil score
    Args:
        civil_score (int): The civil score
    Returns: CommonResp
    """
    try:
        logger.info(f"=====Fetching loan entry by civil score======={cibil_score}")
        loan_package = mongoDalService.mognoDal.get_loan_package_by_cibil_score(cibil_score)
        if not loan_package:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content = ({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Loan entry not found"
                })
            )
        json_loan_package = serialize_doc(loan_package)
        filtered_json_loan_package = filter_loan_providers(json_loan_package)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = LoanPackageResp(
                status_code=status.HTTP_200_OK,
                message="Loan entry fetched successfully",
                data=filtered_json_loan_package
            ).dict()
            )
    except Exception as e:
        logger.error(f"Error fetching loan entry: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = ({
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error fetching loan entry"
            })
        )


