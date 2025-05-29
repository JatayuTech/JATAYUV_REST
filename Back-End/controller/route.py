from typing import List
from service import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import String
from DAO.schemas import SightSchema,clientIn
from service.crud import get_processed_sightseeing_data,clientSave


router=APIRouter()
@router.post("/clientPlanPreparing")
async def saveClient(client:clientIn):
   client_details = await crud.clientSave(client)
   if not client_details:
      raise HTTPException(status_code=500, detail="Client save failed")
   transport_data=await crud.getTransportPlan(client)
   Sightseeing_data = await crud.get_processed_sightseeing_data(client.cNsightseeing,client.cDes,client.cBudget)
   food_data = await crud.get_processed_food(client.cDes,client.cFoodSug,client.cFoodChoice)
   if not transport_data:
      raise HTTPException(status_code=500, detail="There is no particular transporation is there for your requirements")

   acc_data=await crud.get_accomdation_Low_Medium_High(client.cDes,client.cAccomodationPrf)
   return transport_data,Sightseeing_data,food_data,acc_data
   


