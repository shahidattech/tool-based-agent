import os
import abc

# openai client
from openai import OpenAI, types, APIConnectionError, RateLimitError, APIStatusError, AzureOpenAI
from app.service.agents.tools import tools
from app.utils.logging import logger
import requests
import json,re
import random, string

# openai credentials
openai_api_key = os.getenv('OPENAI_API_KEY', '')

# azure credentials
azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '')
azure_api_key = os.getenv('AZURE_OPENAI_API_KEY', '')
azure_api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-05-01-preview')
azure_opneai_deployment_id = os.getenv('AZURE_OPENAI_MODEL_NAME', 'gpt-4')
openai_model_name = os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini')

# helpers
def clean_history(messages: list):
    fields_to_exclude = ["session_id", "_id"]
    cleaned_messages = [{k: v for k, v in message.items() if k not in fields_to_exclude} for message in messages]
    # logger.debug(f"================== messages = {cleaned_messages}")
    return cleaned_messages

def format_response(response: dict) -> dict:
    tool_call_regex = '{?"tool_call.*}$' #'{"tool_call.*}$'
    if response_contains_tool_call := re.match(tool_call_regex, response.get("choices")[0]["message"]["content"]):
        logger.debug(
            f"================== Tool call found in response = {response_contains_tool_call.group()}"
        )
        json_serialized = json.loads(response_contains_tool_call.group())
        function_name = json_serialized.get("tool_call")
        arguments = json_serialized.get("arguments")
        # logger.debug(f"================== function_name = {function_name}, arguments = {arguments}")
        # generate a dynamic tool call id of length 20
        generated_alphanumeric_random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=20)
        )
        tool_call_id = f"call_{generated_alphanumeric_random_string}"

        # modify the response
        response["choices"][0]["message"].pop("function_call", None)
        response["choices"][0]["message"]["tool_calls"] = [
            {
                "id": tool_call_id,
                "function": {
                    "arguments": json.dumps(arguments),
                    "name": function_name
                },
                "type": "function"
            }
        ]
        response["choices"][0]["finish_reason"] = "tool_calls"
        response["choices"][0]["message"]["content"] = None
        logger.debug(f"================== after modification = {response}")
        # return template
    return response

# global message1
# message1 = [{'role': 'system', 'content': "\n\n1. You are an AI financial assistant for a car dealership. Your primary role is to assist customers with vehicle purchases, offer financing options, and guide them through the entire buying process.\n2. Your tasks is to interact solely with a customer and not a dealer or any other role.\n\n[role expectations]\n# Astrix mark the important points.\n1. You **must try to offer customer the best deal to ensure maximum profit for the organization**.\n2. Try to convince the customer to go beyod their expected payment ensuring profit margin for the organization.\n3. Assitant should **strictly follow the conversation flow and mustn't break the conversation flow**.\n4. **Maintain a checklist to yourself**, so that you can refer which steps are completed and which are not.\n5. Customer may want to adjust. But assitant should try to convince the customer to go with the full package ensuring profit for the organization.\nIf **customer is not convinced even after 2-3 burgings, then assitant should proceed with the customer's request**.\n6. **You must not skip any steps in the conversation flow**.\n7. You must be always polite and professional with the customer.\n8. **Assitant asks for customer's consent before applying any changes or adjustments**.\n9. **No further changes can be made once the document is generated**.\n\n[coversation flow checkpoints]\nstep 1: Confirm the User's Name and Car Interest\nstep 2: Fetch customer's phone number by calling get_phone_numbers_by_name() function and tell customer to select the phone number to send OTP\nstep 3: Generate OTP and send to the phone number customer selected\nstep 4: Validate the OTP. The fetch customer deal and get it confirmed from customer\n    - step 4.1: If customer wants to correct information check fesability and update the information. Understand the synonymous words to crrectly call update_customer_info() function. Once customer confirms everything is correct, proceed to step 5.\n    - step 4.2: If customer wants to proceed with the current information, proceed to step 5\nstep 5: Confirm if customer wants to go with current lender {Provider}, or want to show other lender option\n    - step 5.1: If customer wants to check other lender option, call fetch_all_supported_lender_names() to show customer all the available lenders.\n    - step 5.2: If customer wants to go with other lender, verify the lender by calling verify_lender() function, if the lender is not available, prompt the customer to select a valid lender. On a valid selection, proceed to step 6.\n    - step 5.3: If customer wants to go with current lender, proceed to step 6\nstep 6: Show and suggest customer loan options by calling fetch_loan_options_by_lender_and_cibil_score()\n    - step 6.1: If customer wants to compare loan package offered by other lenders, call fetch_loan_options_for_customer_based_on_cibil_score() customer's cibil score.\n    - step 6.2: If customer wants to go with the current lender, proceed to step 7.\n    - step 6.3: If customer wants to change his lender take that into consideration and proceed to step 7.\nstep 7: Package Selection, negotiation and Adjustment if any (assistant tries to convince the customer to go with the full package)\n    - step 7.1: If customer declines full package, assistant should try to convince the customer again, highlighting additional benefits and potential savings.\n    - step 7.2: If customer still declines, assistant should make a final attempt to convince the customer, emphasizing the long-term value and exclusive offers.\n    - step 7.3: If customer declines after multiple attempts, assistant should then accept the customer's request for adjustment.\n    - step 7.4: If customer wants to adjust any change in coverges, ask customer to confirm whether you will proceed to update the requested changes? On receiving the confirmation, call adjust_loan_coverage() function with the requested changes and proceed to step 8.\n    - step 7.4: If customer wants to change his lender, tell customer to confirm whether you will proceed to update the lender change request?\n    - step 7.5: If customer confirms the changes, call update_loan_package_by_customer() function with required parameters for the to update the policy information. Then proceed to step 8.\nstep 8: Ask customer now you'll be generating the updated documet for the customer to sign, and any further changes will not be possible.\n    - step 8.1: If customer agrees, proceed to step 9.\n    - step 8.2: If customer wants to make any change to change the lender or adjustment or customer info etc., you should go back to that specifc step back and then proceed to step 9.\nstep 9: Generate the document to be signed by the customer by calling the function generate_dmv_document() (this step must be executed always)\nstep 10: Customer must sign the document\nstep 11: Send the signed document to the customer\nstep 12: Conclude the conversation\n\n[guardrails]\n1. You only stick to the relevant conversation and don't entertain any other conversation. If conversation is not relevant, you try to bring user back to the relevant conversation.\n2. You must bring back user back to the topic for which you have been employed.\n\n[must have information]\n1. User must provide their name and the car they are interested in to proceed further.\n\n[conversation state]\n# assumption: customer has completed step 2 but has not completed step 3.\n# actionable: If the customer has not completed step 2, the assistant should prompt the customer to complete the required steps before proceeding to step 3.\n# on success: Proceed to step 3.\n\n# assumption: customer has completed step 3 but randomly trying to execute step 5.\n# actionable: If the customer has not completed step 4, the assistant should prompt the customer to complete step 4 before proceeding to step 5.\n# on success: Proceed to step 5.\n\n# assumption: there's some need to execute [scenario based step].\n# actionable: Assistant should be obidient to execute the acionable steps for the scenario based steps.\n\n# assumtion: customer wnats to change his/her lender before signing the document.\n# actionable: Assistant should prompt the customer to confirm whether you will proceed to update the lender change request? On receiving the confirmation, call update_customer_info() function with required parameters for the to update the policy information. Then proceed to step 9.\n"}, {'role': 'user', 'content': 'I am customer: hi'}]


class ClientBase(abc.ABC):
  @abc.abstractmethod
  def generate_answer():
    pass

class OpenaiClient(ClientBase):
  def __init__(self, api_key: str=openai_api_key):
    logger.debug("==================[ Using OpenAI ]==================")
    self.client = OpenAI(
        api_key=api_key
    )
  def generate_answer(self, messages: list, **kwargs)->str:
    try:
      cleaned_messages = clean_history(messages)
      # logger.debug(f"================== messages = {messages}")#
      response = self.client.chat.completions.create(
        model=kwargs.get('model') if 'model' in kwargs else openai_model_name,
        temperature=0,
        max_tokens=1000,
        messages=cleaned_messages,
        tools=tools  # kwargs.get('tools') if 'tools' in kwargs else [],
      )
      logger.debug(f"================== Openai response = {response}")
      return response
    except APIConnectionError as e:
      logger.error(f"The server could not be reached. {e.__cause__}")
    except RateLimitError as e:
        logger.error("A 429 status code was received; we should back off a bit.")
    except APIStatusError as e:
        logger.error(f"Another non-200-range status code was received. status_code: {e.status_code}, response: {e.response}")
    except Exception as e:
      logger.error(f"Error in generating answer: {e}")
      raise e

class AzureOpenaiClient(ClientBase):
  def __init__(self, azure_endpoint: str = azure_endpoint, azure_api_key: str= azure_api_key, azure_api_version: str=azure_api_version):
    logger.debug(f"================== azure_endpoint = {azure_endpoint}, azure_api_key = {azure_api_key}, azure_api_version = {azure_api_version}")
    logger.debug("==================[ Using Azure OpenAI ]==================")
    self.client = AzureOpenAI(
                              azure_endpoint=azure_endpoint,
                              api_key=azure_api_key,
                              api_version=azure_api_version,
                          )
  def generate_answer(self, messages: list, **kwargs)->str:
    try:
      cleaned_messages = clean_history(messages)
      logger.debug(f"================== cleaned messages = {cleaned_messages}")
      response = self.client.chat.completions.create(
                model="gpt-4",
                messages=cleaned_messages,
                temperature=0,
                max_tokens=1000,
                tools=tools #kwargs.get('tools') if 'tools' in kwargs else [],
                )
      return response
    except APIConnectionError as e:
      logger.error(f"The server could not be reached. {e.__cause__}")
    except RateLimitError as e:
        logger.error("A 429 status code was received; we should back off a bit.")
    except APIStatusError as e:
        logger.error(f"Another non-200-range status code was received. status_code: {e.status_code}, response: {e.response}")
    except Exception as e:
      logger.error(f"Error in generating answer: {e}")
      raise e

class AzureRestClient(ClientBase):
  def __init__(self, azure_endpoint: str = azure_endpoint, azure_api_key: str = azure_api_key, azure_api_version: str = azure_api_version, azure_openai_deployment_id: str = azure_opneai_deployment_id):
    """
    Initializes the AzureRestClient with the provided endpoint, API key, API version, and deployment ID.
    """
    logger.debug("==================[ Using Azure OpenAI REST Endpoint ]==================")
    
    # Construct the Azure endpoint URL for the OpenAI REST API
    endpoint = f"{azure_endpoint}openai/deployments/{azure_openai_deployment_id}/chat/completions?api-version={azure_api_version}"
    logger.debug(f"================= Constructed endpoint: {endpoint} =================")
    self.client = {
      "endpoint": endpoint,
      "headers": {
        "Content-Type": "application/json",
        "api-key": azure_api_key
      }
    }
  
  def generate_answer(self, messages: list, temperature: float = 0.7, max_tokens: int = 1000, tools: list = None, **kwargs) -> str:
    """
    Generates an answer from the OpenAI API using the provided conversation history.
    
    Parameters:
    - messages: List of messages (dict) as input to the model.
    - temperature: The sampling temperature for the model's response.
    - max_tokens: The maximum number of tokens to generate in the completion.
    - tools: Any additional tools or context to pass to the model (optional).
    
    Returns:
    - The model's generated response as a string.
    """
    payload = {
      "messages": clean_history(messages),
      "temperature": temperature,
      "max_tokens": max_tokens,
    }

    # Add tools to the payload if they exist
    if tools:
      payload["tools"] = tools

    response = requests.post(self.client["endpoint"], json=payload, headers=self.client["headers"])

    if response.status_code != 200:
      logger.error(f"Failed to generate answer: {response.status_code}, {response.text}")
      raise Exception(f"Error {response.status_code}: {response.text}")

    response_data = response.json()
    logger.debug(f"================= REST Response RAW data: {response_data} =================")
    
    return format_response(response.json())


def ClientFactory(platform="openai"):
  try:
    client = {
      "openai": OpenaiClient,
      "azure_openai": AzureOpenaiClient,
      "azure_rest": AzureRestClient
    }
    return client[platform.lower()]()
  except ValueError:
    raise ValueError(f"Invalid platform: {platform}. Supported platforms are 'openai' and 'azure_openai'.")
  except Exception as e:
    logger.error(f"Error in generating client: {e}")
    raise e
