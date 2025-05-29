from sqlalchemy import Table, Column, Integer, String, Time, Boolean, MetaData

metadata = MetaData()

registration = Table(
    "registration", metadata,
    Column("id", Integer, primary_key=True),
    Column("fullName", String(255)),
    Column("phoneNumber", String(15)),
    Column("Address", String(255)),
    Column("email", String(100)),
    Column("password", String(50)),
)

client = Table(
    "client", metadata,
    Column("cId", Integer, primary_key=True),
    Column("cName", String(255)),
    Column("cSrc", String(100)),
    Column("cDes", String(100)),
    Column("cTotalDays", Integer),
    Column("cBudget", Integer),
    Column("cNsightseeing", Integer),
    Column("cTravelPrf", String(50)),
    Column("cBusType", String(50)),
    Column("cTrainCoach", String(50)),
    Column("cTravelStartTime", Time),
    Column("cTravelEndTime", Time),
    Column("cReturnTravelPrf", String(50)),
    Column("cReturnBusType", String(50)),
    Column("cReturnTrainCoach", String(50)),
    Column("cReturnTravelStartTime", Time),
    Column("cReturnTravelEndTime", Time),
    Column("cAccomodationPrf", String(50)),
    Column("cLowType", String(50)),
    Column("cFoodSug", Boolean),
    Column("cFoodChoice", String(100)),
)
