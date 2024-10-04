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

chat = {}


class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBServiceConv()


# async def ai_assistant(query: str, MongoDalService: MongoDalService ):
#     """
#     Get response from AI Assistant
#     Args: query, MongoDalService
#     Returns: JSONResponse
#     """
#     try:
#         cot = CoT()
#         # last_5_conversations = MongoDalService.mognoDal.get_last_n_conversations(5)
#         answer = cot.forward(query)
#         MongoDalService.mognoDal.post({"FI": query, "customer": answer, "session_time": datetime.datetime.now()})
#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content=AssistantResponse(
#                 status_code=status.HTTP_200_OK,
#                 message=answer
#             ).dict(),
#         )
#     except Exception as e:
#         logger.error(f"Error querying AI Assistant: {e}")
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content=AssistantResponse(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 message="Error querying AI Assistant",
#             ).dict(),
#         )



# # Define your prompt template with the required 'agent_scratchpad' variable
# template = """
#     You are an AI financial assistant for a car dealership.
#     Your job is to help customers with their vehicle purchases, provide financing options, 
#     and ensure all necessary steps are completed. Answer questions, guide customers through 
#     the process.

#     Here is the task you need to complete:
#             1. Collect the customer's name or deal number.
#             2. Fetch the list of phone numbers available for the customer.
#             3. Ask the customer to choose a phone number to receive the OTP.
#             4. Generate and send the OTP to the chosen phone number.
#             5. Collect the OTP from the customer and validate it.
#             6. Collect the customer's deal information (car, address, email, social security number, etc.) and confirm with the customer.
#             7. Provide the document URL for the customer to read and sign.
#             8. Collect the customer's signature and close the deal.
       
#     Sample Conversation:
#             Customer: "I’m Jane Doe.  I’m buying the Sante Fe"
#             AI financial assistant: "Fantastic!  We appreciate the opportunity. Since you’re ready to buy, we’ll be finalizing all your paperwork after which you can take your new car home! 😀 We can go at your pace, but this likely won’t take more than 20 minutes to complete."
#             Customer: "Ok great."
#             AI financial assistant: "Jane, I need to send a code to the number we have on file for you in order to secure your information.  Please select the number that we should send the code to: \nXXX-XXX-4567\nXXX-XXX-6789\nXXX-XXX-0293"
#             Customer: "XXX-XXX-0293"
#             AI financial assistant: "Ok Jane I've sent a code to your phone.  Please tell me the code."
#             Customer: "1234"
#             AI financial assistant: "Thank you Jane.  I have your information secure.  Let's move on to the next step.  Please confirm the following information: \nCar: Sante Fe\nAddress: 123 Main St, Anytown"
#             Customer: "Yes that's correct."
#             AI financial assistant: "Great!  I will send you a link to the documents for you to review and sign.  Please click the link and sign the documents."
#             Customer: "Ok."
#             AI financial assistant: "Thank you Jane.  Your purchase is complete.  You can pick up your new Sante Fe at your convenience.  Have a great day!"
#             Customer: "Thank you!"
#         Here is the conversation so far:
#               {conversation_history}
#     Customer: {customer_query}
#     {agent_scratchpad}
#     AI Assistant:
# """

async def ai_assistant_v2(query: str, mongoDalService: MongoDalService):
    try:
        if last_conversations := serialize_doc(mongoDalService.mognoDal.get_last_n_conversations()):
            logger.info(f"=========== Last conversations: {last_conversations} ===========")
            openai_agent = AgentFactory("openai", mongoDalService=mongoDalService, set_init_history=False)
            openai_agent.clear_history()
            openai_agent.set_history(last_conversations)
        else:
            logger.info(f"=========== No last conversations ===========")
            openai_agent = AgentFactory("openai", mongoDalService=mongoDalService, set_init_history=True)
        # openai_agent.clear_history()
        bot_response = openai_agent.generate_answer_with_agent(query)
        # mongoDalService.mognoDal.post({"assistant": bot_response, "customer": query, "session_time": datetime.datetime.now()})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AssistantResponse(
                status_code=status.HTTP_200_OK,
                message=bot_response
            ).dict()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Got error - {e}")

async def get_conversation_history(mongoDalService: MongoDalService):
    try:
        items = [serialize_doc(doc) for doc in mongoDalService.mognoDal.get()]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=HistoryResponse(
                status_code=status.HTTP_200_OK,
                data=items
            ).dict()
        )
    except Exception as e:
        HTTPException(status_code=500, detail=f"Got error - {e}")

async def delete_coversation_history(mongoDalService: MongoDalService):
    try:
        if mongoDalService.mognoDal.delete_all():
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT
            )
        else:
            raise HTTPException(status_code=500, detail="Error deleting all conversation history")
    except Exception as e:
        HTTPException(status_code=500, detail=f"Got error - {e}")