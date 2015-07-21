""" Contains Note SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on Note model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from . import Notebook

from arrow import now as arrow_now

# -------------------------------------------------------------------------------------------------

class Note(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache note. """

    __tablename__ = 'NOTE'

    id           = Column(Integer, primary_key=True)
    notebook_id  = Column(Integer, ForeignKey('NOTEBOOK.id'))
    key          = Column(String(255))
    value        = Column(String(255))
    created_on   = Column(ArrowType, default=arrow_now)
    last_updated = Column(ArrowType, default=arrow_now, onupdate=arrow_now)

    notebook = relationship(Notebook, backref=backref('notes'))
