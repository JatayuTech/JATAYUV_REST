from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database
from routes.routes import router  

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# ✅ Register router
app.include_router(router)
