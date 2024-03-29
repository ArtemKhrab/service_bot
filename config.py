from dotenv import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv(verbose=True)
token = os.getenv("bot_token")
host = os.getenv("db_host")
user = os.getenv("db_user")
password = os.getenv("db_password")
port = os.getenv("db_port")
utc = int(os.getenv('utc'))

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/Bot?host={host}?port={port}', pool_recycle=3600,
                       isolation_level='READ COMMITTED')
Session = sessionmaker(bind=engine)
session = Session()
