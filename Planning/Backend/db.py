from databases import Database
from sqlalchemy import create_engine, MetaData
DATABASE_URL ="mysql+aiomysql://root:mypass@localhost:3306/lb"
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(
    DATABASE_URL.replace("aiomysql", "pymysql")  
)
