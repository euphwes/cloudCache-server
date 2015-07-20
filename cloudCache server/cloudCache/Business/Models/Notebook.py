""" Contains Notebook SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on Notebook model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from . import User

from arrow import now as arrow_now

# -------------------------------------------------------------------------------------------------

class Notebook(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache notebook. """

    __tablename__ = 'NOTEBOOK'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('USER.id'))
    name       = Column(String)
    created_on = Column(ArrowType, default=arrow_now)

    user = relationship(User, backref=backref('notebooks'))
