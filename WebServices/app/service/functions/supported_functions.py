
from enum import Enum
from app.utils.logging import logger
from app.models.backup_schema import (CustomerDetails, CustomerResdientialInfo, ResidenceType, 
                                      EmployeeInfo, EmpoymentType, Vehicle, TradeVehicle, Policy)

class ClientType(str, Enum):
  CUSTOMER = "customer"
  DEALER = "dealer"

def get_customer_type(user_response: str):
  """
  confirm the customer type from the response. It helps to identify if the user is a customer or a dealer.
  """
  logger.warning("========================= calling get_customer_type")
  if ('customer' not in user_response.lower()) or ('dealer' not in user_response.lower()):
    return "Customer or Dealer?"
  elif "customer" in user_response.lower():
    return ClientType.CUSTOMER
  elif "dealer" in user_response.lower():
    return ClientType.DEALER
  else:
    return "Customer or Dealer?"

def greet_user_after_introduction(customer_type: str, name: str):
  """
  Greet the user based on the customer type.
  """
  logger.warning("========================= calling greet_user_after_introduction")
  message = f"""
            Fantastic!  {name} We appreciate the opportunity. Since you’re ready to buy,
            we’ll be finalizing all your paperwork after which you can take your new car home! 😀
            We can go at your pace, but this likely won’t take more than 20 minutes to complete.
            """ if customer_type.lower() == "customer" else "I'm sorry. At present I don't know how to converse with dealers. I can only trained to help customers."
  logger.warning("user is a customer")
  return message

def end_conversation():
  """
  end conversation
  """
  logger.warning("========================= calling end_conversation")
  return "Thank you. Please visit again"

def get_user_input():
  """
  accept user input
  """
  logger.warning("========================= calling get_user_input")
  return input("user: ")

def get_phone_numbers_by_name(name: str) -> str:
    """Fetch phone numbers from given name, if not found returns 'Not found'"""
    logger.warning("========================= calling get_phone_numbers_by_name")
    phone_nos = ["123-1234-1234", "111111111"]
    message = f"I need to send a code to the number we have on file for you in order to secure your information.  Please select the number that we should send the code to- {phone_nos}"
    return message

def generate_otp(phone_number: str) -> str:
    """Generate OTP when a phone number is provided"""
    logger.warning("========================= calling generate_otp")
    return "123456"

def validate_otp(otp: str, name: str) -> bool:
    """Validate the OTP provided by the customer for given phone number , Return True when Valid else False"""
    return check_info_missing(name=name)

def check_info_missing(name: str):
  """Check if user info is missing"""
  customer_details = CustomerDetails(
      full_name=name,
      phone_or_address="555-555-0293 / 123 Oak Street..",
      policy=Policy(
          policy_no="123456789",
          effective_date="2023-01-01",
          expiry_date="2024-01-01",
          provider="ABC Insurance"
      ),
      vehicle=Vehicle(
          vin="12345678901234567",
          trim="2023 Hyundai Santa Fe Limited Black",
          miles=10000,
          color="Red"
      ),
      trade_vehicle=TradeVehicle(
          vin="12345678901234567",
          trim="2023 Hyundai Santa Fe Limited Black",
          miles=10000,
          color="Red"
      ),
      sale_price="$10000",
      rebate="$1000",
      dealer_fees="$1000",
      trade_value="$10000",
      trade_payoff="$10000",
      tax_rate=0.05,
      ssn="123-45-6789",
      customer_resdiential_info=CustomerResdientialInfo(
          duration_of_living=10.0,
          residence_type=ResidenceType.OWN
      ),
      employee_info=EmployeeInfo(
          employment_type=EmpoymentType.FULL_TIME,
          duration_of_employment=10.0
      ),
      monthly_income="$10000",
      agreement="Customer expects a payment below $700"
  ).dict()
  return f"""
  Perfect.  It looks like the sales team has entered all your information.
  Can you please confirm that this information is correct, and that this is your agreement with the sales department - 
  {customer_details}"""

def update_missing_info():
  """Update missing user info"""
  return True

def fetch_customers_deal_info(deal_number: str) -> dict:
    """Fetch deal information from the deal number"""
    logger.warning("========================= calling fetch_customers_deal_info")
    logger.info(f"=====Fetching deal info by deal number====== {deal_number}")
    return {
        "car": "Toyota Camry",
        "address": "123 Main St, Springfield, IL 62701",
        "email": "xyz@mail.com",
        "ssn": "123-45-6789"
    }

def fetch_doc_url():
  """Fetch document url"""
  return "You can now download your deal confirmation from here- http://example.com"

def prompt_to_enter_customer_name():
  """Prompt to enter customer name"""
  return "Could you please help me with your name"
#===============================================================================
# keeping this for dummy else need to write the whole schema for it, will write later
def generate_dmv_document(customer_name) -> str:
    """returns the downloadable url for the DMV document a pdf"""
    logger.warning("========================= calling generate_dmv_document")
    return "http://example.com/customer_full_name_dmv_document.pdf"

def fetch_loan_options(cibil_score: int)-> str:
    """Fetch loan options based on cibil score"""
    logger.warning("========================= calling fetch_loan_options")
    return f"""
    Based on your cibil score of {cibil_score}, you are eligible for the following loan options:
    1. Loan option 1
    2. Loan option 2
    3. Loan option 3
    """

def sign_document(customer_name: str)-> str:
    """Sign document"""
    return "success"

def send_email(email_id: str)-> str:
    """Send email"""
    return "success"


