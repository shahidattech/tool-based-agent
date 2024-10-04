from fastapi.responses import JSONResponse 
from fastapi import status
from app.utils.logging import logger
import os, random
import datetime, uuid

from app.service.initMongoClient import MongoDBServiceOTP, MongoDBService
from app.models.responses import PhoneNumbersResp, OTPResp, ErrorResp, CommonResp
from app.models.schemas import Otp
import app.service.mongoDal as mongoDalGlobal


class MongoDalServiceOTP:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceOTP()

class MongoDalServiceDeal:
    def __init__(self) -> None:
        self.mognoDal = MongoDBService()
        

async def get_phone_numbers(deal_number: str = None, full_name: str = None, mongoDalService: MongoDalServiceDeal = None):
    """
    Verify a phone number
    Args:
        phone_number (str): The phone number to verify
    Returns: bool
    """
    try:
        logger.info(f"Fetching phone numbers for deal_number: {deal_number}, full_name: {full_name}")
        if not deal_number and not full_name:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ErrorResp(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Deal number or name is required"
                ).dict(),
            )
        phone_numbers = []
        result = None
        if not deal_number and full_name:
            logger.debug(f"Fetching phone numbers for full_name: {full_name}")
            phone_numbers = mongoDalService.mognoDal.get_phone_numbers_by_name(full_name)
            logger.debug(f"deal numnber: {mongoDalGlobal.customer_deal_number}")
        if (deal_number and not full_name) or (deal_number and full_name):
            logger.debug(f"Fetching phone numbers for deal_number: {deal_number}")
            phone_numbers = mongoDalService.mognoDal.get_phone_numbers_by_deal_number(deal_number)

        if phone_numbers:
            # Mask phone Numbers except last four digits
                for i in range(len(phone_numbers)):
                    phone_numbers[i] = f"XXX-XXX-{phone_numbers[i][-4:]}"

                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=PhoneNumbersResp(
                        status_code=status.HTTP_200_OK,
                        message="Phone numbers fetched successfully",
                        data=phone_numbers
                    ).dict(),
                    )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResp(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Phone numbers not found"
                ).dict(),
            )
    
    except Exception as e:
        logger.error(f"Error fetching phone numbers: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error fetching phone numbers",
                error=str(e)
            ).dict(),
        )

async def generate_otp_for_phone_number(phone_number: str, mongoDalService: MongoDalServiceOTP):
    """
    Verify a phone number
    Args:
        phone_number (str): The phone number to verify
    Returns: bool
    """
    try:
        logger.info(f"Verifying phone number: {phone_number}")
        # Generate OTP
        otp = generate_otp()
        otp_obj = Otp(phone_number=phone_number, otp=otp)
        mongoDalService.mognoDal.post(otp_obj.dict())
        # Send OTP to phone_number
        logger.info(f"===OTP: {otp} Generated and sent to Phone number====== {phone_number}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=OTPResp(
                status_code=status.HTTP_200_OK,
                message=f"OTP sent successfully to this phone number for verification: {phone_number}",
                phone_number=phone_number,
                otp=otp
            ).dict()
            )
    
    except Exception as e:
        logger.error(f"Error verifying phone number: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error verifying phone number",
                error=str(e)
            ).dict(),
        )

def generate_otp():
    """
    Generate OTP - a 4 digit random number
    Returns: int
    """
    return random.randint(1000, 9999)

async def validate_otp(phone_number: str, otp: int, mongoDalService: MongoDalServiceOTP):
    """
    Validate OTP
    Args:
        otp_id (str): The OTP ID
        otp (int): The OTP
    Returns: bool
    """
    try:
        logger.info(f"Validating OTP: {otp}")
        query = {"phone_number": phone_number, "otp": otp, "verified": False}
        otp_obj = mongoDalService.mognoDal.get_otp(query)
        if otp_obj is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ErrorResp(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Invalid OTP",
                    error="OTP not found"
                ).dict(),
            )
        if otp_obj["otp"] == otp:
            # Update OTP as verified
            otp_obj_dict = {
                "verified": True,
                "time_verified": datetime.datetime.now()
            }
            mongoDalService.mognoDal.put_otp(otp_obj["_id"], otp_obj_dict)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=CommonResp(
                    status_code=status.HTTP_200_OK,
                    message="OTP verified successfully"
                ).dict(),
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResp(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="OTP validation failed"
            ).dict(),
        )
    
    except Exception as e:
        logger.error(f"Error validating OTP: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error validating OTP",
                error=str(e)
            ).dict(),
        )
