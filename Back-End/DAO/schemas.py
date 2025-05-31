from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime, time
import re

class clientIn(BaseModel):
    cId: int
    cName: str
    cSrc: Optional[str] = None
    cDes: Optional[str] = None
    cTotalDays: Optional[int] = None
    cBudget: Optional[int] = None
    cNsightseeing: Optional[int] = None
    cTravelPrf: Optional[str] = None
    cBusType: Optional[str] = None
    cTrainCoach: Optional[str] = None
    cTravelStartTime: Optional[time] = None
    cTravelEndTime: Optional[time] = None
    cReturnTravelPrf: Optional[str] = None
    cReturnBusType: Optional[str] = None
    cReturnTrainCoach: Optional[str] = None
    cReturnTravelStartTime: Optional[time] = None
    cReturnTravelEndTime: Optional[time] = None
    cAccomodationPrf: Optional[str] = None
    cLowType: Optional[str] = None
    cFoodSug: Optional[bool] = None
    cFoodChoice: Optional[str] = None



class SightSchema(BaseModel):
    sId:int
    sPlace:str
    sLoc:str
    sTiming:str
    sEnfee:str
    sBestTime:str
    sDis:str
    sTransport:str
    sTransportPrice:str
    sDes:str


class FoodSchema(BaseModel):
    fId:int 
    fItem:str 
    fAdd:str 
    fLoc:str 
    fResname:str

class Accommdation(BaseModel):
    aId: int
    aName: str
    aAdd: str
    aRoomtype: str
    aPrice: str
    aRating: str
    aLoc: str
    aHoteltype: str
    aDes:str

class UserCreate(BaseModel):
    full_name: str
    phone_number: int
    location: str
    email: str
    password: str
    @field_validator("full_name")
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError("Full name must be at least 3 characters long.")
        return v

    @field_validator("phone_number")
    def validate_phnNO(cls, v):
            if len(str(v)) != 10:
                raise ValueError("Phone Number must be 10 digits.")
            return v   

    @field_validator("email")
    def validate_email(cls, v):
            pattern = r"^[a-zA-Z0-9._-]+@gmail\.com$"
            if not re.fullmatch(pattern, v):
                raise ValueError("Invalid email format.")
            return v

    @field_validator("password")
    def validate_password(cls, v):
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters long.")
            if not re.search(r"[A-Z]", v):
                raise ValueError("Password must contain at least one uppercase letter.")
            if not re.search(r"[a-z]", v):
                raise ValueError("Password must contain at least one lowercase letter.")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
                raise ValueError("Password must contain at least one special character.")
            return v

class UserLogin(BaseModel):
    email: str
    password: str

class searchHistory(BaseModel):
    cSrc:str
    cDes:str
    cTotalDays:int
    cBudget:int