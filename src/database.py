import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def createDB():
    connection = psycopg2.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"))
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    sql_create_database = cursor.execute(f'create database {os.getenv("DB_NAME")}')
    cursor.close()
    connection.close()

def getConnectionStr():
    return f"{os.getenv("AL_DIALECT")}+{os.getenv("AL_DRIVER")}://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"

url = getConnectionStr()
print(url)
sync_engine = create_engine(
    url=url,
    echo=True,
)
session_factory = sessionmaker(sync_engine)