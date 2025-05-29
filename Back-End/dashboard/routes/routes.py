from fastapi import APIRouter, HTTPException
from crud import create_registration, fetch_client_travel_data
from schemas import RegistrationIn, RegistrationResponse

router = APIRouter()

@router.post("/register", response_model=RegistrationResponse)
async def register_with_travel(reg: RegistrationIn):
    travel_data = await fetch_client_travel_data(reg.cId)
    if not travel_data:
        raise HTTPException(status_code=404, detail="Client ID not found")

    reg_id = await create_registration(reg)
    return RegistrationResponse(registrationId=reg_id, travelData=travel_data)
