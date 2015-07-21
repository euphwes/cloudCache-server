""" Init for cloudCache SQLAlchemy models """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

CONN_STRING = 'mysql+pymysql://{user}:{password}@{host}:{port}/cloudCache'
CONN_STRING = CONN_STRING.format(user='root',
                                 password='password',
                                 host='localhost',
                                 port='3306')

DB_ENGINE = create_engine(CONN_STRING)
DB_SESSION = Session(bind=DB_ENGINE)
SQL_ALCHEMY_BASE = declarative_base()

from .JsonMixin import JsonMixin
from .User import User
from .Notebook import Notebook
from .Note import Note

SQL_ALCHEMY_BASE.metadata.create_all(DB_ENGINE)
