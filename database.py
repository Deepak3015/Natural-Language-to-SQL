from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import os
load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
name = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://{user}:{password}@{host}/{name}"
)
engine = create_engine(DATABASE_URL)
connection  = engine.connect()


