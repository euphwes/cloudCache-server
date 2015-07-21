""" Contains Notebook SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on Notebook model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from . import User
from ..Errors import NotebookAlreadyExistsError

from arrow import now as arrow_now
from arrow.arrow import Arrow

from json import dumps, loads

# -------------------------------------------------------------------------------------------------

class Notebook(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache notebook. """

    __tablename__ = 'NOTEBOOK'

    id         = Column(Integer, primary_key=True)
    user_id    = Column(Integer, ForeignKey('USER.id'))
    name       = Column(String(255))
    created_on = Column(ArrowType, default=arrow_now)

    user = relationship(User, backref=backref('notebooks'))


    def __repr__(self):
        self_repr = 'Notebook(user_id={user_id}, name="{name}")'
        return self_repr.format(user_id=self.user_id, name=self.name)

    def __str__(self):
        self_str = '[{username}] {name}'
        return self_str.format(username=self.user.username, name=self.name)


    def to_json(self, compact=True):
        """ Returns a JSON representation of this Notebook. """

        json = dict()
        attrs = ['id', 'user_id', 'name', 'created_on']

        for attribute in attrs:
            attr_val = getattr(self, attribute)
            if isinstance(attr_val, Arrow):
                attr_val = str(attr_val.to('local'))
            json[attribute] = attr_val

        # pylint: disable=E1101
        # Notebook DOES have attribute "notes", it's created as a backref in Note model
        json['notes'] = [loads(note.to_json()) for note in self.notes]

        if compact:
            return dumps(json, separators=(',',':'))
        else:
            return dumps(json, indent=4, separators=(',', ': '))

# -------------------------------------------------------------------------------------------------

def create_notebook(name, user):
    """ Creates a Notebook entry in the database, and returns the Notebook object to the caller.

    Args:
        name (string): The new notebook's name.
        user (cloudCache.Business.Models.User): The new notebook's user.

    Returns:
        cloudCache.Business.Models.Notebook: The newly-created Notebook.

    """

    if db.query(Notebook).filter_by(name=name, user=user).first():
        message = "A notebook with the name '{}' already exists for the user '{}'"
        message = message.format(name, user.username)
        raise NotebookAlreadyExistsError(message)

    new_notebook = Notebook(user=user, name=name)

    db.add(new_notebook)
    db.commit()

    return new_notebook
