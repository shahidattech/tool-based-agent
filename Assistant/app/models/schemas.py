from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime, date
from app.models.backup_schema import ClientType
import uuid
from enum import Enum

class OwnerDetails(BaseModel):
    florida_resident: Optional[bool] = None
    us_citizen: Optional[bool] = None
    deaf_or_hard_of_hearing: Optional[bool] = None
    ownership_type: Optional[str] = None
    life_estate_remainder_person: Optional[bool] = None
    tenancy_by_the_entirety: Optional[bool] = None
    rights_of_survivorship: Optional[bool] = None

class Name(BaseModel):
    full_name: str = Field(examples=["John Doe"])
    @validator('full_name', pre=True, always=True)
    def normalize_full_name(cls, v):
        return v.lower().strip()

# STORE ADDRESS TYPE EITHER RENTAL OR OWNED
class AddressType(Enum):
    RENTAL= "RENTAL"
    OWNED= "OWNED"




class Address(BaseModel):
    street: Optional[str] = Field(examples=["123 Oak Street"])
    city: Optional[str] = Field(examples=["Miami"])
    state: Optional[str] = Field(examples=["Florida"])
    zip: Optional[str] = Field(examples=["33101"])
    type_of_address: Optional[AddressType] = None
    years_at_address: Optional[str] = Field(None, examples=["10"])
    rent_amount: Optional[str] = Field(None, examples=["$1000"])



class dealStatus(Enum):
    COMPLETED = "COMPLETED"
    PENDING = "PENDING"

class Insurance(BaseModel):
    company: Optional[str]= None
    policy_number: Optional[str] = None
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    coverage: Optional[str] = None

class vehicle(BaseModel):
    vin: str
    title_number: str
    license_plate_number: Optional[str] = None
    make: str
    miles : Optional[int] = None
    model: Optional[str] = None
    year: Optional[str] = None
    body: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None
    insurance: Optional[Insurance] = None

class trade_vehicle(BaseModel):
    vin: str
    trade_value: Optional[str] = None
    title_number: str
    license_plate_number: Optional[str] = None
    make: str
    miles : Optional[int] = None
    model: Optional[str] = None
    year: Optional[str] = None
    body: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None
    insurance: Optional[Insurance] = None

class Dealer(BaseModel):
    name: str
    address: Address
    dealer_number: str
    stock_number: str

class Job(BaseModel):
    title: Optional[str] = Field(None, examples=["Software Engineer"])
    job_type: Optional[str] = Field(None, examples=["Full Time"])
    employer: Optional[str] = Field(None, examples=["ABC Company"])
    year_at_work: Optional[int] = Field(None, examples=[10])
    monthly_income: Optional[str] = Field(None, examples=["$10000"])


class Owner(BaseModel):
    social_security_number: str = Field(examples=["123-45-6789"])
    customer_number: str = Field(default=uuid.uuid4().hex)
    fleet_number: str = Field(default=uuid.uuid4().hex)
    unit_number: str = Field(default=uuid.uuid4().hex)
    county_of_residence: str = Field(examples=["Miami-Dade"])
    details: Optional[OwnerDetails] = None
    name: Name
    phone: Optional[str] = Field(None, examples=["555-555-0293"])
    email: Optional[str] = Field(None, examples=["jane.doe@gmail.com"])
    sex: Optional[str] = Field(None, examples=["Male"])
    date_of_birth: Optional[str] = Field(None, examples=["1990-01-01"])
    id_number: Optional[str] = Field(None, examples=["123-45-6789"])
    civil_score: Optional[int] = Field(None, examples=[700])
    mailing_address: Optional[Address] = None
    residential_address: Optional[Address] = None
    agreement: Optional[str]  = Field(None, examples=["Customer expects a payment below $700"])


class Signature(BaseModel):
    dealer: str
    owner1: str
    owner2: Optional[str] = None

class FinanaicalDetails(BaseModel):
    sale_price: Optional[str] = None
    trade_in_value: Optional[str] = None
    rebate: Optional[str] = None
    dealer_fee: Optional[str] = None
    tax_rate: Optional[str] = None
    customer_payment_agreement: Optional[str] = None


class Deal(BaseModel):
    application_type: str = Field(examples=["New"])
    state: str = Field(examples=["Florida"])
    certificate_print_request: str = Field(examples=["Yes"])
    off_highway_vehicle_type: str = Field(examples=["No"])
    owner: Owner = Field(...),
    co_owner: Optional[Owner] = None
    job_details: Optional[Job] = None
    vehicle: vehicle
    trade_vehicle_details: Optional[trade_vehicle] = None
    financial_details: Optional[FinanaicalDetails] = None
    dealer: Dealer
    signatures: Signature
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    status: Optional[dealStatus] = None



class vehicleUpdate(BaseModel):
    vin: Optional[str] = None
    title_number: Optional[str] = None
    license_plate_number: Optional[str] = None
    make: Optional[str] = None
    miles : Optional[int] = None
    model: Optional[str] = None
    year: Optional[str] = None
    body: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None
    insurance: Optional[Insurance] = None


class DealToUpdate(BaseModel):
    vehicle: Optional[vehicleUpdate] = None


class Otp(BaseModel):
    phone_number: str
    time_sent: datetime = datetime.now()
    time_verified: Optional[datetime] = None
    verified: bool = False
    otp: int

class LoanPackage(BaseModel):
    provider_name: str
    provider_address: Optional[Address] = None
    provider_phone: Optional[str] = None
    package_includes: Optional[str] = None
    loan_terms_in_months: Optional[int] = None
    interest_rate: Optional[float]
    min_civig_score: Optional[int] = None
    max_civig_score: Optional[int] = None
    min_loan_amount: Optional[float] = None

class ContractDoc(BaseModel):
    contract_number: str
    contract_date: date
    contract_amount: float
    contract_terms: str
    contract_provider: str
    contract_provider_address: Address
    contract_provider_phone: str
    contract_provider_email: str
    contract_provider_fax: str
    contract_provider_contact_person: str
    contract_provider_contact_person_title: str
    contract_provider_contact_person_phone: str
    contract_provider_contact_person_email: str
    contract_provider_contact_person_fax: str
    contract_provider_contact_person_address: Address
    contract_provider_contact_person_city: str
    contract_provider_contact_person_state: str
    contract_provider_contact_person_zip: str
    contract_provider_contact_person_country: str
    contract_provider_contact_person_county: str
    contract_provider_contact_person_mailing_address: Address
    contract_provider_contact_person_residential_address: Address
    contract_provider_contact_person_agreement: str
    contract_provider_contact_person_signature: Signature
    contract_provider_contact_person_job_details: Job
    contract_provider_contact_person_owner: Owner
    contract_provider_contact_person_co_owner: Owner
    contract_provider_contact_person_vehicle: vehicle
    contract_provider_contact_person_trade_vehicle_details: trade_vehicle
    contract_provider_contact_person_financial_details: FinanaicalDetails
    contract_provider_contact_person_dealer: Dealer
    contract_provider_contact_person_signatures: Signature
    contract_provider_contact_person_created_at: datetime
    contract_provider_contact_person_updated_at: Optional[datetime]
    contract_provider_contact_person_status: dealStatus
    contract_provider_contact_person_application_type: str
    contract_provider_contact_person_state: str
    contract_provider_contact_person_certificate_print_request: str
    contract_provider_contact_person_off_highway_vehicle_type: str
    contract_provider_contact_person_owner: Owner
    contract_provider_contact_person_co_owner: Owner
    contract_provider_contact_person_job_details: Job
    contract_provider_contact_person_vehicle: vehicle
    contract_provider_contact_person_trade_vehicle_details: trade_vehicle
    contract_provider_contact_person_financial_details: FinanaicalDetails
    contract_provider_contact_person_dealer: Dealer
    contract_provider_contact_person_signatures: Signature
    contract_provider_contact_person_created_at: datetime
    contract_provider_contact_person_updated_at: Optional[datetime]
    contract_provider_contact_person_status: dealStatus

class ChatPayloadModel(BaseModel):
    query:str
    session_id: Optional[str] = None
    customer_type: ClientType = Field(examples=["customer"])
    # customer_name: Optional[str] = Field("", examples=["John Doe"], description="Customer name for customer type. For dealer, it should be optional.")