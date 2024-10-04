from app.models.schemas import Deal, DealToUpdate
from app.models.responses import CreateDealResp
from app.models.backup_schema import CustomerDetails, CustomerDetailsToUpdate
from fastapi.responses import JSONResponse 
from fastapi import status
import asyncio
from app.utils.logging import logger
from app.models.responses import CreateDealResp
from app.service.initMongoClient import MongoDBService
import random
import string
from fastapi.encoders import jsonable_encoder
from typing import Optional

class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBService()

async def create_deal(payload: CustomerDetails, mongoDalService: MongoDalService):
    """
    Create a deal
    Args: Deal, mongoDalService
    Returns: JSONResponse
    """

    try:
        print("=====Creating deal=====")
        logger.info(f"=====Creating deal====={payload.dict()}")

        payload_dict = payload.dict()
        deal_number = generate_unique_deal_no()
        payload_dict["deal_number"] = deal_number
        # Strip and lower payload_dict["full_name"]
        payload_dict["full_name"] = payload_dict["full_name"].strip().lower()
        mongoDalService.mognoDal.post(jsonable_encoder(payload_dict))
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=CreateDealResp(
                status_code=status.HTTP_201_CREATED,
                message= f"Deal created successfully with deal_number:{deal_number}"
            ).dict(),
        )
    except Exception as e:
        logger.error(f"Error creating deal: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CreateDealResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error creating deal",
            ).dict(),
        )

def generate_unique_deal_no(length=5):
    """
    Generate a unique alphanumeric string of specified length.
    Args:
        length (int): Length of the generated string. Default is 5.
    Returns:
        str: Generated unique alphanumeric string.
    """
    characters = string.ascii_uppercase + string.digits
    unique_id = ''.join(random.choices(characters, k=length))
    return unique_id

async def get_deal(name: str, mongoDalService: MongoDalService):
    """
    Get a deal by deal_number
    Args: deal_number, mongoDalService
    Returns: JSONResponse
    """
    try:
        logger.info(f"=====Getting name====={name}")
        deal = mongoDalService.mognoDal.collection.find_one({"full_name": name.strip().lower()})
        if deal:
            # Convert ObjectId to string
            if "_id" in deal:
                deal["_id"] = str(deal["_id"])            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=CreateDealResp(
                    status_code=status.HTTP_200_OK,
                    message="Deal fetched successfully with empty fields in vehicle",
                    data=deal
                ).dict(),
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=CreateDealResp(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Deal not found",
                ).dict(),
            )

    except Exception as e:
        logger.error(f"Error getting deal: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CreateDealResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error getting deal",
            ).dict(),
        )
    

def filter_empty_values(input_dict):
    """
    Filter empty values from a dictionary
    Args: input_dict
    Returns: dict
    """
    filtered_dict = {}

    for key, value in input_dict.items():
        print("=====", key, value)
        if isinstance(value, dict):
            # Recursively filter nested dictionaries
            nested_filtered = filter_empty_values(value)
            if nested_filtered:  # Add non-empty results from nested dict
                filtered_dict[key] = nested_filtered
        elif value == "" or value is None or value == "string" or key == "deal_number":
            # Check for empty string or None values
            filtered_dict[key] = value
    return filtered_dict

# This function extract the desired values as in filtered_deal from the deal object
def filter_desired_values(deal):
    """
    Filter desired values from a dictionary
    Args: deal
    Returns: dict
    """
    filtered_dict = {}

    for key, value in deal.items():
        if key == "owner":
            owner = value
            filtered_dict["social_security_number"] = owner["social_security_number"]
            filtered_dict["full_name"] = owner["name"]["full_name"]
            filtered_dict["phone"] = owner["phone"]
            filtered_dict["residential_address"] = owner["residential_address"]
        elif key == "vehicle":
            filtered_dict["vehicle"] = value
        elif key == "trade_vehicle_details":
            filtered_dict["trade_vehicle_details"] = value
        elif key == "financial_details":
            filtered_dict["financial_details"] = value
        elif key == "job_details":
            filtered_dict["job_details"] = value

    return filtered_dict

async def update_deal(name: str, payload:CustomerDetailsToUpdate, mongoDalService: MongoDalService):
    """
    Update a deal by deal_number
    Args: deal_number, payload, mongoDalService
    Returns: JSONResponse
    """
    try:
        logger.info(f"=====Updating deal====={name}")
        # Convert payload to dict and exclude unset values
        logger.info(f"=====payload====={payload.dict()}")
        name = name.strip().lower()
        # Allowed update values are full_anme,Address and policy, anything else if comens for update raise error
        if not payload.full_name and not payload.address and not payload.policy:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=CreateDealResp(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Sorry! you are allowed to update  Only full_name, residential_address and policy",
                ).dict(),
            )
        payload_dict_to_update = payload.dict(exclude_unset=True)
        existing_deal = mongoDalService.mognoDal.collection.find_one({"full_name": name})
        if existing_deal:
            # Merge update_data with existing_deal
            def merge_dicts(d1, d2):
                for k, v in d2.items():
                    if isinstance(v, dict):
                        d1[k] = merge_dicts(d1.get(k, {}), v)
                    else:
                        d1[k] = v.lower() if k=="full_name" else v
                return d1

            updated_deal = merge_dicts(existing_deal, payload_dict_to_update)
            logger.info(f"==payload_dict=== {updated_deal}")
            # Update the deal with the new payload
            mongoDalService.mognoDal.collection.update_one({"full_name": name}, {"$set": updated_deal})
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=CreateDealResp(
                    status_code=status.HTTP_200_OK,
                    message="Deal updated successfully",
                ).dict(),
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=CreateDealResp(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Deal not found",
                ).dict(),
            )
    except Exception as e:
        logger.error(f"Error updating deal: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CreateDealResp(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error updating deal",
            ).dict(),
        )