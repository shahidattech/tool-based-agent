from pydantic import BaseModel
from typing import List, Optional, Any

class CreateDealResp(BaseModel):
    status_code: int
    message: str
    data: Optional[dict] = None

class PhoneNumbersResp(BaseModel):
    status_code: int
    message: str
    data: Any

class OTPResp(BaseModel):
    status_code: int
    message: str
    phone_number: str
    otp: int

class ErrorResp(BaseModel):
    status_code: int
    message: str
    error: Optional[str] = None

class CommonResp(BaseModel):
    status_code: int
    message: str
    data: Optional[dict] = None

class AssistantResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[dict] = None

class CreateLoanPackageResp(BaseModel):
    status_code: int
    message: str
    loan_package_id : str

class LoanPackageResp(BaseModel):
    status_code: int
    message: str
    data: Optional[list[dict]] = None

class HistoryResponse(BaseModel):
    status_code: int
    data: list