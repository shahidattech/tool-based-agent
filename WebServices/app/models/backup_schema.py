
from pydantic import BaseModel, Field,validator
from enum import Enum
from typing import Optional, Annotated

class Policy(BaseModel):
  policy_no: str = Field(default=None, examples=["1234567890"])
  effective_date: str = Field(default=None, examples=["2023-01-01"])
  expiry_date: str = Field(default=None, examples=["2024-01-01"])
  provider: str = Field(default=None, examples=["ABC Insurance"])

class Vehicle(BaseModel):
  vin: str = Field(default=None, examples=["12345678901234567"])
  trim: str = Field(default=None,examples=["2023 Hyundai Santa Fe Limited Black"])
  miles: int = Field(default=None, examples=[10000], description="Miles ran")
  color: str = Field(default=None, examples=["Red"])

class TradeVehicle(Vehicle):
  pass

class ResidenceType(str, Enum):
  OWN = "own"
  RENT = "rent"

class EmpoymentType(str, Enum):
  FULL_TIME = "full_time"
  PART_TIME = "part_time"
  SELF_EMPLOYED = "self_employed"

class CustomerResdientialInfo(BaseModel):
  duration_of_living: float = Field(default=None, examples=[10.0], description="duration of living in years")
  residence_type: ResidenceType
  rent: Optional[str] = Field(default=None, examples=["$1000"])

class EmployeeInfo(BaseModel):
  employment_type: EmpoymentType
  duration_of_employment: float = Field(default=None, examples=[10.0], description="duration of employment in years")
  organization: Optional[str] = Field(default= None, examples=["ABC Company"])


class CustomerDetails(BaseModel):
  """
  Customer Details
  """
  full_name: str = Field(examples=["John Doe"])
  phone_primary: str = Field(examples=["555-555-0293"])
  phone_secondary: Optional[str] = Field(default= None, examples=["555-555-0294"])
  address: Optional[str] = Field(default= None, examples=["123 Oak Street.."])
  policy: Policy
  vehicle: Vehicle
  trade_vehicle: Optional[TradeVehicle] = None
  sale_price: Optional[str] = Field(default=None, examples=["$10000"])
  rebate: Optional[str] = Field(default= None, examples=["$1000"])
  dealer_fees: str = Field(examples=["$1000"])
  trade_value: Optional[str] = Field(default= None, examples=["$10000"])
  trade_payoff: Optional[str] = Field(default= None, examples=["$10000"])
  tax_rate: float = Field(examples=[0.05], description="tax rate in %")
  ssn: str = Field(examples=["123-45-6789"])
  cibil_score: Optional[int] = Field(default= None, examples=[700])
  customer_resdiential_info: CustomerResdientialInfo
  employee_info: EmployeeInfo
  monthly_income: str = Field(examples=["$10000"], description="monthly income")
  agreement: str = Field(examples=["Customer expects a payment below $700"], description="agreement")

class CustomerDetailsToGenerateDocument(CustomerDetails):
  """
  Customer Details
  """
  deal_number :  Annotated[str, Field(examples=["1234567890"])]

class CustomerDetailsToUpdate(BaseModel):
  """
  Customer Details
  """
  full_name: Optional[str] = Field(default= None, examples=["John Doe"])
  phone_primary: Optional[str] = Field(default= None, examples=["555-555-0293"])
  phone_secondary: Optional[str] = Field(default= None, examples=["555-555-0294"])
  address: Optional[str] = Field(default=None, examples=["123 Oak Street.."])
  policy: Optional[Policy] = None
  vehicle: Optional[Vehicle] = None
  trade_vehicle: Optional[TradeVehicle] = None
  sale_price: Optional[str] = Field(default= None, examples=["$10000"])
  rebate: Optional[str] = Field(default= None, examples=["$1000"])
  dealer_fees: Optional[str] = Field(default= None, examples=["$1000"])
  trade_value: Optional[str] = Field(default= None, examples=["$10000"])
  trade_payoff: Optional[str] = Field(default= None, examples=["$10000"])
  tax_rate: Optional[float] = Field(default= None,examples=[0.05], description="tax rate in %")
  ssn: Optional[str] = Field(default=None, examples=["123-45-6789"])
  cibil_score: Optional[int] = Field(default= None, examples=[700])
  customer_resdiential_info: Optional[CustomerResdientialInfo] = None
  employee_info: Optional[EmployeeInfo] = None
  monthly_income: Optional[str] = Field(default= None, examples=["$10000"], description="monthly income")
  agreement: Optional[str] = Field(default= None, examples=["Customer expects a payment below $700"], description="agreement")

class ClientType(str, Enum):
  CUSTOMER = "customer"
  DEALER = "dealer"
  
