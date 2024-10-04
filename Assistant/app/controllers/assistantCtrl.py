from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.service.initMongoClient import MongoDBServiceConv
from app.service.mongoDal import customer_deal_number
from app.models.responses import AssistantResponse, HistoryResponse
from app.utils.logging import logger
from app.utils.utility import serialize_doc
import datetime
# from app.service.dspy.DSPy import CoT
from app.service.agents.agent import AgentFactory
from app.service.prompts.prompt_templates import system_prompt2
from app.models.schemas import ChatPayloadModel
import uuid
import os

chat = {}


class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceConv()

def get_openai_client(**kwargs):
    try:
        ai_source = os.getenv("AI_SOURCE")
        if ai_source.lower() == "openai":
            return AgentFactory("openai", **kwargs)
        elif ai_source.lower() == "azure_openai":
            return AgentFactory("azure_openai", **kwargs)
        elif ai_source.lower() == "azure_rest":
            return AgentFactory("azure_rest", **kwargs)
        else:
            raise ValueError("Unsupported AI_SOURCE")
    except Exception as e:
        raise e


async def ai_assistant_v2(input: ChatPayloadModel, mongoDalService: MongoDalService):
    try:
        query = input.query
        customer_type = input.customer_type.lower()
        session_id : str = str(input.session_id) if input.session_id else str(uuid.uuid4())
        # logger.debug(f"=========== Query: {query} ===========")
        if last_conversations := serialize_doc(mongoDalService.mognoDal.get_last_n_conversations(session_id=session_id)):
            # logger.info(f"=========== Last conversations: {last_conversations} ===========")
            # openai_agent = AgentFactory("azure_openai", mongoDalService=mongoDalService, set_init_history=False, session_id=session_id, customer_type=customer_type)
            openai_agent = get_openai_client(mongoDalService=mongoDalService, set_init_history=False, session_id=session_id, customer_type=customer_type)
            openai_agent.clear_history()
            openai_agent.set_history(last_conversations)
        else:
            logger.info(f"=========== No last conversations ===========")
            openai_agent = get_openai_client(mongoDalService=mongoDalService, set_init_history=True, session_id=session_id, customer_type=customer_type)
            # openai_agent = AgentFactory("azure_openai", mongoDalService=mongoDalService, set_init_history=True, session_id=session_id, customer_type=customer_type)
        # openai_agent.clear_history()

        # TO-DO   Session ID need to be stored in the database
        bot_response_from_agent: str | dict = openai_agent.generate_answer_with_agent(query)
        message = bot_response_from_agent.get("message") if isinstance(bot_response_from_agent, dict) else bot_response_from_agent
        message = message.strip().strip("\n")
        data = {"session_id": str(session_id), "customer_name": bot_response_from_agent.get("customer_name", "")
                      if (isinstance(bot_response_from_agent, dict)) or ("customer_name" in bot_response_from_agent) else ""}
        # mongoDalService.mognoDal.post({"assistant": bot_response, "customer": query, "session_time": datetime.datetime.now()})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AssistantResponse(
                status_code=status.HTTP_200_OK,
                message=message,
                data=data
            ).dict()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"ValueError - {e}")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error - {e}")

async def get_conversation_history(session_id: str, filter_conversation_only: bool, mongoDalService: MongoDalService):
    try:
        # if filer is true, only get conversation history for user and assistant for that session_id else
        # get all conversation history for that session_id
        exclude_list = ["tool_calls"]
        filter = {"session_id": session_id, "$or": [{"role": "user"}, {"role": "assistant"}], "$nor": [{field: {"$exists": True}} for field in exclude_list]} if filter_conversation_only else {"session_id": session_id}
        items = [serialize_doc(doc) for doc in mongoDalService.mognoDal.get(filter)]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=HistoryResponse(
                status_code=status.HTTP_200_OK,
                data=items
            ).dict()
        )
    except Exception as e:
        HTTPException(status_code=500, detail=f"Got error - {e}")

async def delete_coversation_history(session_id: str, mongoDalService: MongoDalService):
    try:
        if mongoDalService.mognoDal.delete_all():
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT
            )
        else:
            raise HTTPException(status_code=500, detail="Error deleting all conversation history")
    except Exception as e:
        HTTPException(status_code=500, detail=f"Got error - {e}")