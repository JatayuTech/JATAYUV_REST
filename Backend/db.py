from databases import Database
from sqlalchemy import create_engine, MetaData
DATABASE_URL ="mysql+aiomysql://vamsi:Vamsi-9989816487@localhost/lb"
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL.replace("aiomysql", "pymysql")  
)
