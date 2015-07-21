""" Contains Notebook SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103,E1101
# Disable no-init warning on Notebook model
# Disable name-too-short warning on `id` variable
# Notebook DOES have attribute "notes", it's created as a backref in Note model

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, JsonMixin, DB_SESSION as db
from . import User
from ..Errors import NotebookAlreadyExistsError

from arrow import now as arrow_now

# -------------------------------------------------------------------------------------------------

class Notebook(JsonMixin, SQL_ALCHEMY_BASE):
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


    def to_ordered_dict(self):
        """ Returns an OrderedDict representation of this Notebook. """

        attrs = ['name', 'id', 'user_id', 'created_on']
        kvp = {'notes': [note.to_ordered_dict() for note in self.notes]}
        return self._to_ordered_dict(attrs, additional_kvp=kvp)


    def to_json(self, compact=True):
        """ Returns a JSON representation of this Notebook. """

        attrs = ['name', 'id', 'user_id', 'created_on']
        kvp = {'notes': [note.to_ordered_dict() for note in self.notes]}
        return self._to_json(attrs, compact=compact, additional_kvp=kvp)

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
