""" Init for cloudCache SQLAlchemy models """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_SESSION = None
SQL_ALCHEMY_BASE = declarative_base()

from .User import User

# TODO: This should actually point to real database
# TODO: Actually, check first if it exists? If not, create first?
DB_ENGINE = create_engine('sqlite://')
SQL_ALCHEMY_BASE.metadata.create_all(DB_ENGINE)
DB_SESSION = Session(bind=DB_ENGINE)
