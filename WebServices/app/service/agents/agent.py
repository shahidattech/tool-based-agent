import abc

from openai import OpenAI, types
import json

from app.utils.logging import logger
from app.service.agents.client import ClientFactory
# from app.service.initMongoClient import MongoDBServiceConv
from app.service.agents.tools import tools
from app.service.agents.utility import chat_completion_message_to_dict
from app.service.prompts.prompt_templates import *
from app.service.functions.supported_functions import *
from app.utils.utility import serialize_doc

# class MongoDalService:
#     def __init__(self) -> None:
#         self.mognoDal = MongoDBServiceConv()


class AgentBase(abc.ABC):
    @abc.abstractmethod
    def generate_answer_with_agent():
        pass

    @abc.abstractmethod
    def append_history():
        pass

    @abc.abstractmethod
    def clear_history():
        pass


class OpenaiAgent(AgentBase):
    def __init__(self, **kwargs):
        try:
            # this flag is used to set the initial history
            logger.warning(f"================= kwargs = {kwargs} ==================")
            self.mongo_service = kwargs.get('mongoDalService')
            self.set_init_history = kwargs.get('set_init_history', True)
            if self.set_init_history:
                # set the initial history
                self.history = []
                self.append_history(role="system", content=system_prompt3)
            self.client = ClientFactory("openai")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

    def set_initial_history(self, history: list):
        try:
            self.history = history
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

    def append_history(
        self,
        completion: types.chat.chat_completion = None,
        role: str = "",
        content: str = "",
        tool_call_id="",
    ) -> None:
        """
        append the history with completion or role and content. This method will append the history and 
        post it to mongo
        """
        try:
            if completion:
                logger.warning(f"================= completion ===================")
                completion_dict = chat_completion_message_to_dict(completion)
                self.history.append(completion_dict)
                doc_id = self.mongo_service.mognoDal.post(completion_dict)
            elif role and content and tool_call_id:
                logger.warning(f"================= role and content and tool_call_id ===================")
                data = {"role": role, "content": content, "tool_call_id": tool_call_id}
                self.history.append(data)
                doc_id = self.mongo_service.mognoDal.post(data)
            elif role and content:
                logger.warning(f"================= role and content ===================")
                data = {"role": role, "content": content}
                self.history.append(data)
                doc_id = self.mongo_service.mognoDal.post(data)
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

    def get_history(self) -> list:
        try:
            return self.history
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

    def clear_history(self) -> None:
        self.history = []

    def set_history(self, history: list)-> None:
        self.history = history

    def generate_answer_with_agent(self, query: str) -> str:
        try:
            # append user quesrt+y
            try:
                self.append_history(role="user", content=query)
            except Exception as e:
                logger.error(f"Error: {e}")
                raise e
            try:
                response = self.client.generate_answer(messages=serialize_doc(self.history), tools=tools)
            except Exception as e:
                logger.error(f"Error: {e}")
                raise e
            if response.choices[0].finish_reason == "tool_calls":
                logger.warning(f"================= tool_calls ===================")
                # this will be done until all function execution done. Need to handle the result and feed it again to model
                # append the completion
                if response.choices[0].message:
                    self.append_history(
                        completion=response.choices[0].message
                    )  # need to check what to append
                # evaluate the tool result
                tool_call_result = self.handle_chat_completion(response)
                # response = self.client.generate_answer(messages=self.history, tools=tools)
                # =================================================================================================
                # self.append_history(
                #     role="assistant", content=response.choices[0].message.content
                # )
                # =================================================================================================
                return (
                    tool_call_result
                    if tool_call_result
                    else response.choices[0].message.content
                )
            else:
                logger.warning(f"================= chat_completion ===================")
                self.append_history(
                    role="assistant", content=response.choices[0].message.content
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error: {e}")

    def handle_chat_completion(self, response) -> str:
        # while response.choices[0].message.tool_calls:
        try:
            tool_calls = response.choices[0].message.tool_calls
            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                tool_call_id = tool_call.id
                result = self.call_tool(tool_name, **json.loads(tool_args))
                # append each tool call results
                self.append_history(
                    role="tool",
                    content=json.dumps(result) if isinstance(result, dict) else result,
                    tool_call_id=tool_call_id,
                )
            # response = self.client.generate_answer(messages=self.history, tools=tools)
            return result
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e

    def call_tool(self, tool_name: str, **args):
        """
        choose a tool from available functions and return the result
        """
        try:
            available_tools = {
                "get_customer_type": get_customer_type,
                "greet_user_after_introduction": greet_user_after_introduction,
                "end_conversation": end_conversation,
                "get_user_input": get_user_input,
                "get_phone_numbers_by_name": get_phone_numbers_by_name,
                "generate_otp": generate_otp,
                "validate_otp": validate_otp,
                "check_info_missing": check_info_missing,
                "fetch_customers_deal_info": fetch_customers_deal_info,
                # "fetch_payoff_info": fetch_payoff_info,
                "fetch_doc_url": fetch_doc_url,
                "update_missing_info": update_missing_info,
                "prompt_to_enter_customer_name": prompt_to_enter_customer_name,
                "generate_dmv_document": generate_dmv_document,
                "fetch_loan_options": fetch_loan_options,
                "sign_document": sign_document,
                "send_email": send_email
            }
            func = available_tools[tool_name]
            return func(**args)
        except Exception as e:
            logger.error(f"Error: {e}")
            raise e


def AgentFactory(platform="openai", **kwargs):
    agent = {
        "openai": OpenaiAgent,
    }
    return agent[platform](**kwargs)