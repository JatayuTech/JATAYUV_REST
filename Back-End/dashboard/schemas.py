from pydantic import BaseModel
from typing import List, Optional

class RegistrationIn(BaseModel):
    fullName: str
    phoneNumber: str
    Address: str
    email: str
    password: str
    cId: int

class ClientTravelData(BaseModel):
    source: str
    destination: str
    days: int
    budget: int

class RegistrationResponse(BaseModel):
    registrationId: int
    travelData: ClientTravelData