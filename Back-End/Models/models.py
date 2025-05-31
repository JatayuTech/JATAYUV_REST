from sqlalchemy import BIGINT, Table, Column, Integer, String, Float,Boolean,DateTime
from DAO.db import metadata
client1 = Table(
"client",
metadata,
Column("cId", BIGINT, primary_key=True, index=True),
Column("cName", String(255), nullable=False),
Column("cSrc", String(100)),
Column("cDes", String(100)),
Column("cTotalDays", Integer),
Column("cBudget", Integer),
Column("cNsightseeing", Integer),
Column("cTravelPrf", String(50)),
Column("cBusType", String(50), default=None),
Column("cTrainCoach", String(50), default=None),
Column("cTravelStartTime", DateTime),
Column("cTravelEndTime", DateTime),
Column("cReturnTravelPrf", String(50)),
Column("cReturnBusType", String(50), default=None),
Column("cReturnTrainCoach", String(50), default=None),
Column("cReturnTravelStartTime", DateTime),
Column("cReturnTravelEndTime", DateTime),
Column("cAccomodationPrf", String(50)),
Column("cLowType", String(50)),
Column("cFoodSug", Boolean),
Column("cFoodChoice", String(100))
)

transport = Table(
    "transport1",
    metadata,
    Column("S.No",Integer,primary_key=True),
    Column("Tname",String(100)),
    Column("Ttype",String(100)),
    Column("Tdepa",String(100)),
    Column("Tarr",String(100)),
    Column("Tsrc",String(100)),
    Column("Tdura",String(100)),
    Column("Tdes",String(100)),
    Column("Tprice",String(100)),
    Column("Tfrequency",String(100)),
    Column("TypeofRoute",String(100))
)



sights = Table(
    "sights",
    metadata,
    Column("sId", Integer, primary_key=True),
    Column("sPlace", String(100)),
    Column("sLoc", String(100)),
    Column("sTiming", String(100)),
    Column("sEnfee", String(100)),
    Column("sBesttime", String(100)),
    Column("sDis", String(100)),
    Column("sTransport", String(100)),
    Column("sTransportPrice", String(100)),
    Column("sDes", String(100))
)

food=Table(
    "food",
    metadata,
    Column("fId",Integer,primary_key=True),
    Column("fItem",String(100)),
    Column("fAdd",String(100)),
    Column("fLoc",String(100)),
    Column("fResname",String(100))
)

accomdation1 = Table(
    "accomodation",
    metadata,
    Column("aId", Integer, primary_key=True),
    Column("aName", String(100)),
    Column("aAdd", String(100)),
    Column("aRoomtype", String(100)),
    Column("aPrice", String(100)),
    Column("aRating", String(100)),
    Column("aLoc", String(100)),
    Column("aHoteltype", String(100)),
    Column("aDes",String(100))
)


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True,autoincrement=True),
    Column("full_name", String(100), nullable=False,),
    Column("phone_number", Integer, nullable=False),
    Column("location", String(100), nullable=False),
    Column("email", String(100), nullable=False, unique=True, index=True),
    Column("password", String(255), nullable=False)
)