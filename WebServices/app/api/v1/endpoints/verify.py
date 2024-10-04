from fastapi import APIRouter, Depends, HTTPException
from app.models.responses import PhoneNumbersResp
from app.models.responses import OTPResp
import app.controllers.verificationCtrl as  verificationCtrl
from app.utils.logging import logger
from app.models.responses import CreateDealResp, CommonResp
from app.service.initMongoClient import MongoDBServiceOTP, MongoDBService
import random
import string
from typing import List, Dict, Optional


class MongoDalServiceOTP:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceOTP()

class MongoDalServiceDeal:
    def __init__(self) -> None:
        self.mognoDal = MongoDBService()

router = APIRouter()

@router.get("/phone_numbers", response_model=PhoneNumbersResp)
async def get_phone_numbers(
    deal_number: Optional[str] = None, 
    full_name: str = None, 
    mongoDalService: MongoDalServiceDeal = Depends(MongoDalServiceDeal)
):
    """
    Get all phone numbers
    Returns: PhoneNumbersResp
    """
    logger.info(f"==\n\n\nFetching phone numbers for deal_number: {deal_number}, full_name: {full_name} ")

    return await verificationCtrl.get_phone_numbers(deal_number, full_name, mongoDalService)



@router.get("/generate_otp_for_phone_number/{phone_number}", response_model=OTPResp)
async def generate_otp_for_phone_number(phone_number: str, mongoDalService: MongoDalServiceOTP = Depends(MongoDalServiceOTP)):
    """
    Verify a phone number
    Args:
        phone_number (str): The phone number to verify
    Returns: OTPResp
    """
    logger.info(f"==\n\n\nVerifying phone number: {phone_number}")
    return await verificationCtrl.generate_otp_for_phone_number(phone_number, mongoDalService)

@router.put("/validate_otp/{otp}", response_model=CommonResp)
async def validate_otp(otp: int, mongoDalServiceOTP: MongoDalServiceOTP = Depends(MongoDalServiceOTP), mongoDalServiceDEAL: MongoDalServiceDeal = Depends(MongoDalServiceDeal)):
    """
    Validate OTP
    Args:
        otp_id (str): The OTP ID
        otp (int): The OTP
    Returns: CommonResp
    """
    logger.info(f"==\n\n\nValidating OTP: {otp}")
    return await verificationCtrl.validate_otp(otp, mongoDalServiceOTP, mongoDalServiceDEAL)