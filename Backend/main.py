from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- IMPORT THIS
from db import database, metadata, engine

from routes import route 

app = FastAPI()

origins = [
    "http://localhost",         # General localhost
    "http://localhost:5500",    # Example: VS Code Live Server
    "http://127.0.0.1",         # General 127.0.0.1
    "http://127.0.0.1:5500",    # Example: VS Code Live Server
    "null",                     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # List of allowed origins
    allow_credentials=True,      # Allow cookies (if your app uses them)
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Crucially include OPTIONS
    # allow_methods=["*"], # Or allow all methods
    allow_headers=["Content-Type", "Authorization"], # Allow specific headers
    # allow_headers=["*"],  # Or allow all headers
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
