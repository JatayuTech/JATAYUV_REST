from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class SightSchema(BaseModel):
    sId:int
    sPlace:str
    sLoc:str
    sTiming:str
    sEnfee:str
    sBesttime:str
    sDis:str
    sTransport:str
    sTransportPrice:str
    sDes:str
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
    cTravelStartTime: Optional[datetime] = None
    cTravelEndTime: Optional[datetime] = None
    cReturnTravelPrf: Optional[str] = None
    cReturnBusType: Optional[str] = None
    cReturnTrainCoach: Optional[str] = None
    cReturnTravelStartTime: Optional[datetime] = None
    cReturnTravelEndTime: Optional[datetime] = None
    cAccomodationPrf: Optional[str] = None
    cLowType: Optional[str] = None
    cFoodSug: Optional[bool] = None
    cFoodChoice: Optional[str] = None
class FoodSchema(BaseModel):
    fId:int 
    fItem:str 
    fAdd:str 
    fLoc:str 
    fResname:str