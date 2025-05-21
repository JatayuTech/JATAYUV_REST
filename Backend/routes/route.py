from typing import List
import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import String
from schemas import SightSchema,clientIn
from crud import get_processed_sightseeing_data,clientSave
router=APIRouter()
@router.post("/saveClient")
async def saveClient(client:clientIn):
   client_details=await crud.clientSave(client)
   if not client_details:
      raise HTTPException(status_code=500, detail="Client save failed")
   sightseeing_data= await crud.get_processed_sightseeing_data(client_details["cNsightseeing"],client_details["cDes"])
   food_data = await crud.get_processed_food(client_details["cDes"],client_details["cFoodSug"],client_details["cFoodChoice"])
   return [sightseeing_data,food_data]
   


