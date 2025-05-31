from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time


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