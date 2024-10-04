
from enum import Enum
from app.utils.logging import logger
from app.models.backup_schema import (CustomerDetails, CustomerResdientialInfo, ResidenceType, 
                                      EmployeeInfo, EmpoymentType, Vehicle, TradeVehicle, Policy, ClientType)

from app.service.apis.api_client import APIClient
import os


api_clinet = APIClient(os.getenv("API_BASE_URL","http://nova-ai-finance-expert-webservices:8001/nova/ai-fi/api/v1/"))

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

def greet_user_after_introduction(customer_type: str, name: str)-> dict:
  """
  Greet the user based on the customer type.
  """
  logger.warning("========================= calling greet_user_after_introduction")
  message = f"""
            Fantastic!  {name} We appreciate the opportunity. Since you’re ready to buy,
            we’ll be finalizing all your paperwork after which you can take your new car home! 😀
            We can go at your pace, but this likely won’t take more than 20 minutes to complete.
            """ if customer_type.lower() == "customer" else f"Welcome {name}. Please let me know how I can help you today."
  data = {"customer_name": name if name else ""}
  data["message"] = message
  logger.warning("user is a customer")
  return data

def end_conversation(customer_name: str):
  """
  end conversation
  """
  return f"Done! All your documents have been emailed along with our contact info.  Thank you, {customer_name}, we really appreciate your business. Please wait for your sales professional in the lobby till they bring your new car around."

def get_user_input():
  """
  accept user input
  """
  logger.warning("========================= calling get_user_input")
  return input("user: ")

def get_phone_numbers_by_name(name: str) -> str:
    """Fetch phone numbers from given name, if not found returns 'Not found'"""
    logger.warning("========================= calling get_phone_numbers_by_name")
    response = api_clinet.make_call(endpoint=f"verify/phone_numbers?full_name={name}", method="GET")
    message = ""
    if response.status_code == 200:
      phone_nos = response.json()["data"]
      message = f"I need to send a code to the number we have on file for you in order to secure your information.  Please select the number that we should send the code to- {phone_nos}"
    else:
      message = "Sorry We are not able to find your name in our records, We can help you out with some available laon packages"
    logger.info(f"Phone numbers fetched: {message}")
    return message


def generate_otp(phone_number: str) -> str:
    """Generate OTP when a phone number is provided"""
    logger.warning("========================= calling generate_otp {phone_number}")
    response = api_clinet.make_call(endpoint=f"verify/generate_otp_for_phone_number/{phone_number}", method="GET")
    logger.info(f"OTP generated Response: {response.json()}")
    message = ""
    if response.status_code == 200:
       message = response.json()["message"]
    else:
      message = "Sorry we are not able to generate OTP at this moment, please try again later"
    return message

# To be done:  "Need to pass phone number and otp to validate"
def validate_otp(otp: str, name: str) -> str:
    """Validate the OTP provided by the customer, Return cutomer data when Validated successfully"""
    logger.warning("========================= calling validate_otp")
    response = api_clinet.make_call(endpoint=f"verify/validate_otp/{otp}", method="PUT")
    # Validate the OTP API should also return the required infomation to satisfy check_info_missing data when OT is validated
    if response.status_code == 200:
      logger.info(f"OTP validated Response: {response.json()}")
      # return check_customer_info_missing(name=name)
      return f"""Thank you. It looks like the sales team has entered all your information. Can you please confirm that this information is correct, and that this is your agreement with the sales department -
      {fetch_customers_deal_info(name)}"""
    else:
      return "Sorry, the OTP you entered is incorrect. Please try again"
    
# def check_customer_info_missing(name: str,  data: dict = None) -> dict:
#   """Check if user info is missing for the customer or need to update"""
#   # If Called through Validate OTP, then data will be available
  
#   if not name:
#     return "Sorry, we are not able to fetch your information at this moment, please try again later"

#   if data:
#     return f"""
#     Perfect.  It looks like the sales team has entered all your information.
#     Can you please confirm that this information is correct, and that this is your agreement with the sales department - 
#     {data}"""
#   else:
#      customer_data = fetch_customers_deal_info(name)
#      return f"""
#      Perfect.  It looks like the sales team has entered all your information.
#      Can you please confirm that this information is correct, and that this is your agreement with the sales department - 
#      {customer_data}"""

def get_missing_info(customer_data: dict)-> list:
    """Check if user info is missing for the customer or need to update"""
    fields_missing = []
    missing = [None, 0, ""]
    for key, value in customer_data.items():
        if isinstance(value, dict):
          for k, v in value.items():
            if v in missing:
              fields_missing.append(k)
        elif value in missing:
          fields_missing.append(key)
    return fields_missing

def render_html_list(list_data: list):
  """Render list data into html"""
  list_html = ""
  for data in list_data:
    list_html += f"<li>{data}</li>"
  return f"<ul>{list_html}</ul>"

def render_customer_info_html(customer_data: dict):
  """Render customer info into html"""
  customer_info_html = ""
  for key, value in customer_data.items():
    if isinstance(value, dict):
      customer_info_html += f"""
      <tr>
        <td>{key}</td>
        <td>
          <table>
            {render_customer_info_html(value)}
          </table>
        </td>
      </tr>
      """
    else:
      customer_info_html += f"""
      <tr>
        <td>{key}</td>
        <td>{value}</td>
      </tr>
      """
  return f"<table>{customer_info_html}</table>"

def check_customer_info_missing(name: str) -> dict:
  """
  This function checks the customer info in the database and also returns name of the fields if value is empty string
  The return value is of type string containing html tags
  """
  logger.warning("========================= calling check_customer_info_missing")
  fields_missing = []
  response = api_clinet.make_call(endpoint=f"deals/{name}", method="GET")
  if response.status_code == 200:
    customer_data = response.json()["data"]
    missing_details = get_missing_info(customer_data)
    # if missing info found render those into htnl list
    common_message = f"""
       Perfect.  It looks like the sales team has entered your information.
       Can you please confirm that this information is correct, and that this is your agreement with the sales department -
       </br>
       {render_customer_info_html(customer_data)}
       """
    if missing_details:
      missing_info_html = render_html_list(missing_details)
      return f"""
      {common_message}
      </br> We also found that some of the information is missing, could you please confirm whether we should update the following information:
      {missing_info_html}
      """
    return common_message
  return "Sorry, we are not able to fetch your information at this moment, please try again later"

# def create_payload_for_update(data: dict):
#   """Create payload for update where values are not None or not empty or 0"""
#   missing = [None, 0, ""]
#   customer_info_schema = {
#     "full_name": "",
#     "phone_primary": "",
#     "phone_secondary": "",
#     "address": "",
#     "policy": {
#       "policy_no": "",
#       "effective_date": "",
#       "expiry_date": "",
#       "provider": ""
#     },
#     "vehicle": {
#       "vin": "",
#       "trim": "",
#       "miles": 0,
#       "color": ""
#     },
#     "trade_vehicle": {
#       "vin": "",
#       "trim": "",
#       "miles": 0,
#       "color": ""
#     },
#     "sale_price": "",
#     "rebate": "",
#     "dealer_fees": "",
#     "trade_value": "",
#     "trade_payoff": "",
#     "tax_rate": 0.0,
#     "ssn": "",
#     "cibil_score": 0,
#     "customer_resdiential_info": {
#       "duration_of_living": 0,
#       "residence_type": "own",
#       "rent": ""
#     },
#     "employee_info": {
#       "employment_type": "",
#       "duration_of_employment": 0,
#       "organization": ""
#     },
#     "monthly_income": "",
#     "agreement": ""
#   }
#   # update this schema according to the data received
#   for key, value in data.items():
#     if isinstance(value, dict):
#       for k, v in value.items():
#         if v not in missing:
#           customer_info_schema[key][k] = v
#     elif value not in missing:
#       customer_info_schema[key] = value
#   return customer_info_schema

def create_payload_for_update(full_name: str, address: str, policy: dict) -> dict:
   try:
      payload_dict = {}
      if full_name:
        payload_dict["full_name"] = full_name
      if address:
        payload_dict["address"] = address
      if policy:
        payload_dict["policy"] = policy
      return payload_dict
   except Exception as e:
      raise e

# def update_customer_info(existing_customer_name: str, full_name: str = "", address: str = "", policy: dict = {}) -> str:
#     # import json
#     """Update customer information, accept name and data to update"""
#     logger.warning("========================= calling update_customer_info")
#     # logger.info(f"args: {args}")
#     # logger.info(f"kwargs: {kwargs}")
#     # return "Successfully updated your information."
#     # if kwargs:
#     #   name = kwargs.get("name")
#     #   data = kwargs.get("data")
#     # else:
#     #   name = args[1]
#     #   data = args[0]
#     # logger.warning("========================= calling update_customer_info")
#     logger.info(f"===Full name: {full_name}, Address: {address}, Policy: {policy}")
#     data = create_payload_for_update(full_name=full_name, address=address, policy=policy)
#     logger.debug(f"===Data to update:==== {data}")
#     response = api_clinet.make_call(endpoint=f"deals/{existing_customer_name}", method="PUT", json=data)
#     if response.status_code == 200:
#       to_call_with_name = full_name if full_name else existing_customer_name
#       return f"Successfully updated your information. Please reverify the information = {fetch_customers_deal_info(to_call_with_name)}"
#     else:
#       return "Sorry, we are not able to update your information at this moment, please try again later."

def update_customer_info(**kwargs) -> str:
    # import json
    """Update customer information, accept name and data to update"""
    allowed_fields_to_update = ["full_name", "address", "policy", "existing_customer_name"]
    logger.info(f"===kwargs: {kwargs}")
    # check kwargs keys are in allowed fields to update
    if any(key for key in kwargs.keys() if key not in allowed_fields_to_update):
      return "Sorry, we are not able to update your information. You are permitted to update only full name, address, policy."
    existing_customer_name = kwargs.get("existing_customer_name")
    full_name = kwargs.get("full_name")
    address = kwargs.get("address")
    policy = kwargs.get("policy")
    # logger.info(f"args: {args}")
    # logger.info(f"kwargs: {kwargs}")
    # return "Successfully updated your information."
    # if kwargs:
    #   name = kwargs.get("name")
    #   data = kwargs.get("data")
    # else:
    #   name = args[1]
    #   data = args[0]
    # logger.warning("========================= calling update_customer_info")
    logger.info(f"===Full name: {full_name}, Address: {address}, Policy: {policy}")
    data = create_payload_for_update(full_name=full_name, address=address, policy=policy)
    logger.debug(f"===Data to update:==== {data}")
    response = api_clinet.make_call(endpoint=f"deals/{existing_customer_name}", method="PUT", json=data)
    if response.status_code == 200:
      to_call_with_name = full_name if full_name else existing_customer_name
      return f"Successfully updated your information. Please reverify the information = {fetch_customers_deal_info(to_call_with_name)}"
    else:
      return "Sorry, we are not able to update your information at this moment, please try again later."



def fetch_customers_deal_info(customer_name: str) -> dict:
    """Fetch deal information from the customer_name"""
    logger.warning("========================= calling fetch_customers_deal_info")
    response = api_clinet.make_call(endpoint=f"deals/{customer_name}", method="GET")
    if response.status_code == 200:
      return response.json()['data']
    else:
      return "Sorry, we are not able to fetch deal information at this moment, please try again later"

# def update_missing_info():
#   """Update missing user info"""
#   return True

# not in use
# def fetch_customers_deal_info(deal_number: str) -> dict:
#     """Fetch deal information from the deal number"""
#     logger.warning("========================= calling fetch_customers_deal_info")
#     logger.info(f"=====Fetching deal info by deal number====== {deal_number}")
#     return {
#         "car": "Toyota Camry",
#         "address": "123 Main St, Springfield, IL 62701",
#         "email": "xyz@mail.com",
#         "ssn": "123-45-6789"
#     }

def fetch_doc_url():
  """Fetch document url"""
  return "You can now download your deal confirmation from here- http://example.com"

def prompt_to_enter_customer_name():
  """Prompt to enter customer name"""
  return "Could you please help me with your name"


def generate_dmv_document(customer_name: str) -> str:
    import json
    """returns the downloadable url for the DMV document a pdf"""
    logger.warning("========================= calling generate_dmv_document")
    response = api_clinet.make_call(endpoint=f"deals/{customer_name}", method="GET")
    if response.status_code == 200:
      customer_data : dict = response.json()["data"]
      logger.info(f"Customer data: {customer_data} and type: {type(customer_data)}")
      #filter out the key _id
      customer_data.pop("_id")
      # Now make call to the above endpoint to generate the document that return document_name
      response = api_clinet.make_call(endpoint="document-management/", method="POST", json=customer_data)
      document_name = response.json()["document_name"]
      
      return f"Please check your dmv document:  {document_name}"
    else:
      return "Sorry, we are not able to generate DMV document at this moment, please try again later"

def fetch_customer_cibil_score_by_name(customer_name: str) -> int:
    """Fetch customer cibil score"""
    logger.warning("========================= calling fetch_customer_cibil_score")
    response = api_clinet.make_call(endpoint=f"deals/{customer_name}", method="GET")
    if response.status_code == 200:
      return response.json()['data']["cibil_score"]
    else:
      return "Sorry, we are not able to fetch your cibil score at this moment, please try again later"


def fetch_loan_options_for_customer(customer_name: str)-> list[dict]:
    """Fetch loan options for customer"""
    logger.warning("========================= calling fetch_loan_options")
    if not customer_name:
      return "Sorry, we are not able to fetch loan options at this moment, please try again later"
    cibil_score = fetch_customer_cibil_score_by_name(customer_name)
    response = api_clinet.make_call(endpoint=f"loan-package/loan-by-civil-score/{cibil_score}", method="GET")
    if response.status_code == 200:
      loan_packages = response.json()["data"]
      loan_package_html = ""
      for serial_no,loan_package in enumerate(loan_packages, start=1):
        loan_package_html += f"""
        <tr>
          <td>Option {serial_no}</td>
          <td>
            <table>
              <tr>
                <td>Provider Name</td>
                <td>{loan_package["details"]['provider_name']}</td>
              </tr>
              <tr>
                <td>Provider Phone</td>
                <td>{loan_package["details"]['provider_phone']}</td>
              </tr>
              <tr>
                <td>Package Includes</td>
                <td>{loan_package["details"]['package_includes']}</td>
              </tr>
              <tr>
                <td>Loan Terms in Months</td>
                <td>{loan_package["details"]['loan_terms_in_months']}</td>
              </tr>
              <tr>
                <td>Interest Rate</td>
                <td>{loan_package["details"]['interest_rate']}</td>
              </tr>
            </table>
        </tr>
        </br>
        """
         
      # return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: </br>{loan_package_html}"
      return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: {loan_packages}"
    else:
      return "Sorry, we are not able to fetch loan options at this moment, please try again later"
  
def fetch_loan_options_for_dealer()-> str:
    """Fetch loan options for dealer"""
    response = api_clinet.make_call(endpoint="loan-package/4", method="GET")
    if response.status_code == 200:
      loan_packages = response.json()["data"]
      loan_package_html = ""
      for loan_package in loan_packages:
        loan_package_html += f"""
        <tr>
          <td>Provider Name</td>
          <td>{loan_package["details"]['provider_name']}</td>
        </tr>
        <tr>
          <td>Provider Phone</td>
          <td>{loan_package["details"]['provider_phone']}</td>
        </tr>
        <tr>
          <td>Package Includes</td>
          <td>{loan_package["details"]['package_includes']}</td>
        </tr>
        <tr>
          <td>Loan Terms in Months</td>
          <td>{loan_package["details"]['loan_terms_in_months']}</td>
        </tr>
        <tr>
          <td>Interest Rate</td>
          <td>{loan_package["details"]['interest_rate']}</td>
        </tr>
        </br>
        """
      loan_package_html = f"<table>{loan_package_html}</table>"
      return f"Here are the loan options for the dealer: </br> {loan_packages}"
    else:
      return "Sorry, we are not able to fetch loan options at this moment, please try again later"

def authenticate_dealer_with_otp(otp: str)-> str:
    """Authenticate dealer with OTP"""
    return "success"



def sign_document(customer_name: str)-> list[dict]:
    """Sign document"""
    return "We can email your signed documents or print them for you, which would you prefer?"

def send_email(email_id: str)-> str:
    """Send email"""
    return f"We have sent email to your email id to {email_id}"

def print_signed_document():
    """Print signed document"""
    return "We have successfully printed your signed documents"

def verify_lender(lender_name: str)-> str:
    """Verify lender"""
    response = api_clinet.make_call(endpoint=f"loan-package/all_lenders/", method="GET")
    if response.status_code == 200:
      supported_lenders = response.json()["data"]
    else:
       return "Sorry, we are not able to fetch supported lenders at this moment, please try again later"
    if lender_name in supported_lenders:
      return f"Ok so you are interested in {lender_name} loan options. Let me check the rates for you."
    return f"Sorry, we don't have option to finance with {lender_name} Are you open to other lenders such as {','.join(supported_lenders)} rates are a bit lower."

def fetch_loan_package_by_lender_and_customer_name(customer_name: str, lender_name: str = "", )->str:
   try:
      cibil_score = fetch_customer_cibil_score_by_name(customer_name)
      if lender_name:
        params = {"lender_name": lender_name}
        response = api_clinet.make_call(
          endpoint=f"loan-package/loan-by-civil-score/{cibil_score}",
          method="GET",
          params=params)
      else:
          response = api_clinet.make_call(
          endpoint=f"loan-package/loan-by-civil-score/{cibil_score}",
          method="GET")
      if response.status_code == 200:
        loan_packages = response.json()["data"]
      return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: {loan_packages}"
   except Exception as e:
      return f"Sorry, we are not able to fetch loan options at this moment, please try again later"
   
def adjust_loan_coverage(customer_name: str, coverages: list):
   logger.warning("========================= calling adjust_loan_coverage")
   # make call to the endpoint to adjust the loan coverage
   logger.warning(f"coverages to adjust: {coverages} for customer: {customer_name}")
   return "We have made the requested changes to your loan coverage. May we proceed to the next formalities?"

def fetch_loan_options_for_customer_based_on_cibil_score(cibil_score: int)-> list[dict]:
    """Fetch loan options for customer based on cibil score"""
    logger.warning("========================= calling fetch_loan_options")
    response = api_clinet.make_call(endpoint=f"loan-package/loan-by-civil-score/{cibil_score}", method="GET")
    if response.status_code == 200:
      loan_packages = response.json()["data"]
      # return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: </br>{loan_package_html}"
      return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: {loan_packages}"
    else:
      return "Sorry, we are not able to fetch loan options at this moment, please try again later"

def fetch_loan_options_by_lender_and_cibil_score(lender_name: str, cibil_score: int)-> list[dict]:
    """Fetch loan options for customer based on cibil score"""
    logger.warning("========================= calling fetch_loan_options")
    response = api_clinet.make_call(endpoint=f"loan-package/loan-by-civil-score/{cibil_score}?lender_name={lender_name}", method="GET")
    if response.status_code == 200:
      loan_packages = response.json()["data"]
      # return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: </br>{loan_package_html}"
      return f"Based on your cibil score of {cibil_score}, you are eligible for the following loan options: {loan_packages}"
    else:
      return "Sorry, we are not able to fetch loan options at this moment, please try again later"
    
def fetch_all_supported_lender_names()-> list[str]:
    """Fetch all supported lender names"""
    response = api_clinet.make_call(endpoint=f"loan-package/all_lenders/", method="GET")
    if response.status_code == 200:
      return f"Here are the supported lenders: {response.json()['data']}"
    else:
      return "Sorry, we are not able to fetch supported lenders at this moment, please try again later"



