from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.responses import CreateDealResp
from app.models.schemas import Deal, DealToUpdate
from app.models.backup_schema import CustomerDetails,CustomerDetailsToUpdate
from app.controllers.dealCtrl import create_deal
from app.service.initMongoClient import MongoDBService
import  app.controllers.dealCtrl as dealCtrl
from typing import Optional
from pydantic import Field  # pylint: disable=no-name-in-module


router = APIRouter()

class MongoDalService:
    def __init__(self) -> None:
        self.mognoDal = MongoDBService()




@router.post("/", response_model=CreateDealResp)
async def create_deal(payload: CustomerDetails, mongoDalService: MongoDalService = Depends(MongoDalService)):
    return await dealCtrl.create_deal(payload, mongoDalService)

@router.get("/{name}")
async def get_deal(name: str,
                   mongoDalService: MongoDalService = Depends(MongoDalService)):
    """
    Get a deal by deal_number
    Args: deal_number, full_name, check_empty, mongoDalService
    Returns: JSONResponse
    """
    return await dealCtrl.get_deal(name, mongoDalService)

@router.put("/{name}")
async def update_deal(name: str, payload: CustomerDetailsToUpdate, mongoDalService: MongoDalService = Depends(MongoDalService)):
    """
    Update a deal by deal_number
    Args: deal_number, payload, mongoDalService
    Returns: JSONResponse
    """
    return await dealCtrl.update_deal(name, payload, mongoDalService)

