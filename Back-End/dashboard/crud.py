from models import registration, client
from schemas import RegistrationIn, ClientTravelData
from database import database
from sqlalchemy import select

async def create_registration(reg: RegistrationIn) -> int:
    reg_dict = reg.dict()
    reg_dict.pop("cId")  # exclude cId before insert
    query = registration.insert().values(**reg_dict)
    return await database.execute(query)

async def fetch_client_travel_data(cId: int) -> ClientTravelData:
    query = select(
    client.c.cSrc.label("source"),
    client.c.cDes.label("destination"),
    client.c.cTotalDays.label("days"),
    client.c.cBudget.label("budget")
).where(client.c.cId == cId)

    result = await database.fetch_one(query)
    return ClientTravelData(**result) if result else None