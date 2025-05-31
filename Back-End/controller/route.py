from typing import List
from service import crud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import String
from DAO.schemas import SightSchema,clientIn,UserCreate,UserLogin
from service.crud import get_processed_sightseeing_data,clientSave, get_user_by_email, getDashBoardDetails, getSearchHistory


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
   


@router.post("/register")
async def UserRegistration(user: UserCreate):
    existing_user = await crud.get_user_by_email(user.email) 
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user_details = await crud.userSave(user)
    if not user_details:
        raise HTTPException(status_code=500, detail="User save failed. Register again.")
    
    return {"message": "Registration is successful"}

@router.post("/login")
async def login(user: UserLogin):
    try:
        db_user = await get_user_by_email(user.email)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error during login")

    if not db_user:
        raise HTTPException(status_code=404, detail="User not registered")

    if db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful", "user": db_user["email"]}


@router.get("/dashboard/{email}/{password}")
async def dashboard(email:str, password:str):

    userDetails = await getDashBoardDetails(email,password)
    if not userDetails:
        return {"User is not registered / User details not matched"}
    else:
        searchHis = await getSearchHistory(userDetails["full_name"])
        return userDetails,searchHis

