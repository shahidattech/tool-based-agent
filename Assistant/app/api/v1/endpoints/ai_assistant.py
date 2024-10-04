from fastapi import APIRouter, Depends, HTTPException, Query
from app.utils.logging import logger
from app.models.responses import AssistantResponse
from app.service.initMongoClient import MongoDBServiceConv
from app.controllers.assistantCtrl import ai_assistant_v2, get_conversation_history, delete_coversation_history
from app.service.functions.supported_functions import  get_phone_numbers_by_name, generate_dmv_document,fetch_loan_options_for_customer, fetch_loan_options_for_dealer,check_customer_info_missing,update_customer_info, validate_otp, generate_otp, end_conversation, get_user_input
from app.models.schemas import ChatPayloadModel
from typing import Optional



router = APIRouter()

class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceConv()

    
@router.post("/ai-assistant/")
async def _ai_assistant_v2(input: ChatPayloadModel,
                       mongoDalService: MongoDalService = Depends(MongoDalService)):
    return await ai_assistant_v2(input=input, mongoDalService=mongoDalService)

@router.get("/get_conversation_history")
async def conversation_history(session_id: Optional[str] = None, filter_conversation_only: bool=False, mongoDalService: MongoDalService = Depends(MongoDalService)):
    return await get_conversation_history(session_id, filter_conversation_only, mongoDalService=mongoDalService)

@router.delete("/delete_conversation_history", status_code=204)
async def _delete_conversation_history(session_id: Optional[str] = None, mongoDalService: MongoDalService = Depends(MongoDalService)):
    return await delete_coversation_history(session_id, mongoDalService=mongoDalService)


