# database.py
from sqlalchemy import create_engine
from databases import Database
from models import metadata 

DATABASE_URL = "mysql+aiomysql://root:Plmokn098!@localhost/transport_db"

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL.replace("aiomysql", "pymysql"))
