# db.py
import os
from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine, MetaData

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError(
        "Database credentials (DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) not found in environment variables or .env file."
    )

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL.replace("aiomysql", "pymysql")
)