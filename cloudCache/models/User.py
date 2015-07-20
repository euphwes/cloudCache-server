""" Contains User SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on User model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils.types import ArrowType
from . import SQL_ALCHEMY_BASE

import arrow

# -------------------------------------------------------------------------------------------------

class User(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache user. """

    __tablename__ = 'USER'

    id            = Column(Integer, primary_key=True)
    username      = Column(String, unique=True)
    first_name    = Column(String)
    last_name     = Column(String)
    email_address = Column(String)
    api_key       = Column(String)
    date_joined   = Column(ArrowType, default=arrow.now)
