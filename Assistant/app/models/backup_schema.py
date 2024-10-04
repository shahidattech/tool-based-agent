
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Policy(BaseModel):
  policy_no: str
  effective_date: str
  expiry_date: str
  provider: str

class Vehicle(BaseModel):
  vin: str = Field(examples=["12345678901234567"])
  trim: str = Field(examples=["2023 Hyundai Santa Fe Limited Black"])
  miles: int = Field(examples=[10000], description="Miles ran")
  color: str = Field(examples=["Red"])

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
  duration_of_living: float = Field(examples=[10.0], description="duration of living in years")
  residence_type: ResidenceType
  rent: Optional[str] = Field(examples=["$1000"], default="")

class EmployeeInfo(BaseModel):
  employment_type: EmpoymentType
  duration_of_employment: float = Field(examples=[10.0], description="duration of employment in years")
  organization: Optional[str] = Field(default= None, examples=["ABC Company"])

class CustomerDetails(BaseModel):
  """
  Customer Details
  """
  full_name: str
  phone : str = Field(examples=["555-555-0293"])
  address: str = Field(examples=["555-555-0293 / 123 Oak Street.."])
  policy: Policy
  vehicle: Vehicle
  trade_vehicle: Optional[TradeVehicle] = None
  sale_price: str = Field(examples=["$10000"])
  rebate: Optional[str] = Field(default= None, examples=["$1000"])
  dealer_fees: str = Field(examples=["$1000"])
  trade_value: Optional[str] = Field(default= None, examples=["$10000"])
  trade_payoff: Optional[str] = Field(default= None, examples=["$10000"])
  tax_rate: float = Field(examples=[0.05], description="tax rate in %")
  ssn: str = Field(examples=["123-45-6789"])
  customer_resdiential_info: CustomerResdientialInfo
  employee_info: EmployeeInfo
  monthly_income: str = Field(examples=["$10000"], description="monthly income")
  agreement: str = Field(examples=["Customer expects a payment below $700"], description="agreement")

class ClientType(str, Enum):
  CUSTOMER = "customer"
  DEALER = "dealer"