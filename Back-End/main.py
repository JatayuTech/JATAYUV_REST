from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 
from DAO.db import database, metadata, engine

from controller import route 

app = FastAPI()

origins = [
    "http://localhost:5500",  
    "http://127.0.0.1",         
    "http://127.0.0.1:5500",        
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,      
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  
    allow_headers=["Content-Type", "Authorization"],
)

metadata.create_all(engine)

# Connect DB at startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect DB at shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(route.router)
