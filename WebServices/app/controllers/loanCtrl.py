from app.models.schemas import LoanPackage
from app.utils.utility import serialize_doc

from app.service.initMongoClient import MongoDBServiceLoan
from app.utils.logging import logger
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import status



class MongoDalServiceLoan:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceLoan()

async def create_loan_entry(loan: LoanPackage, mongoDalService: MongoDBServiceLoan):
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
        mongoDalService.mognoDal.post(jsonable_encoder(payload_dict))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content = ({
                "status_code": status.HTTP_201_CREATED,
                "message": "Loan entry created successfully"
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
