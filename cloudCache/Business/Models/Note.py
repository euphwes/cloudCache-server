""" Contains Note SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on Note model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, JsonMixin, DB_SESSION as db
from . import Notebook
from ..Errors import NoteAlreadyExistsError, NoteDoesntExistError

from arrow import now as arrow_now

# -------------------------------------------------------------------------------------------------

class Note(JsonMixin, SQL_ALCHEMY_BASE):
    """ Represents a cloudCache note.

    Attributes:
        id (int): Unique ID of this note.
        notebook_id (int): Unique ID of this note's parent notebook.
        key (string): Key for this note.
        value (string): Value/contents of this note.
        created_on (Arrow): Date/time that this note was originally created.
        last_updated (Arrow): Date/time that this note was last modified.
        notebook (cloudCache.Business.Models.Notebook): This note's Notebook object.

    """

    __tablename__ = 'NOTE'

    id           = Column(Integer, primary_key=True)
    notebook_id  = Column(Integer, ForeignKey('NOTEBOOK.id'))
    key          = Column(String(255))
    value        = Column(String(255))
    created_on   = Column(ArrowType, default=arrow_now)
    last_updated = Column(ArrowType, default=arrow_now, onupdate=arrow_now)

    notebook = relationship(Notebook, backref=backref('notes', cascade='save-update, delete'))


    def __repr__(self):
        self_repr = 'Note(notebook_id={nb_id}, key="{key}", value="{value}")'
        return self_repr.format(nb_id=self.notebook_id, key=self.key, value=self.value)

    def __str__(self):
        self_str = '[{nb_name}] {key} - {value}'
        return self_str.format(nb_name=self.notebook.name, key=self.key, value=self.value)


    def to_ordered_dict(self):
        """ Returns an OrderedDict representation of this Note. """
        return self._to_ordered_dict(_get_attributes())


    def to_json(self, compact=True):
        """ Returns a JSON representation of this Note. """
        return self._to_json(_get_attributes(), compact=compact)

# -------------------------------------------------------------------------------------------------

def _get_attributes():
    """ Returns a list of strings representing the Note attributes which are to be serialized to
    JSON or an OrderedDict. """

    return ['key', 'value', 'id', 'notebook_id', 'created_on', 'last_updated']

# -------------------------------------------------------------------------------------------------

def create_note(key, value, notebook):
    """ Creates a Note entry in the database, and returns the Note object to the caller.

    Args:
        key (string): The new note's key.
        value (string): The new note's value.
        notebook (cloudCache.Business.Models.Notebook): The new note's notebook.

    Returns:
        cloudCache.Business.Models.Note: The newly-created Note.

    """

    if db.query(Note).filter_by(key=key, notebook=notebook).first():
        message = "A note with the key '{}' already exists for the notebook '{}'"
        message = message.format(key, notebook.name)
        raise NoteAlreadyExistsError(message)

    new_note = Note(key=key, value=value, notebook=notebook)

    db.add(new_note)
    db.commit()

    return new_note


def get_note(note_id, user):
    """ Retrieve a Note for a given user.

    Args:
        note_id (string): The note's id.
        user (cloudCache.Business.Models.User): The note's user.

    Returns:
        cloudCache.Business.Models.Note: The Note.

    Raises:
        cloudCache.Business.Errors.NoteDoesntExistError: If a note with the given ID doesn't exist for this user.

    """

    note = db.query(Note).filter_by(id=note_id).first()

    if not note:
        message = "Note with ID '{}' doesn't exist.".format(note_id)
        raise NoteDoesntExistError(message)

    if note.notebook.user != user:
        message = "The note with ID '{}' doesn't belong to you ({}).".format(note_id, user.username)
        raise NoteDoesntExistError(message)

    return note


def delete_note(note_id, user):
    """ Delete a Note for a given user.

    Args:
        note_id (string): The note's id.
        user (cloudCache.Business.Models.User): The note's user.

    Raises:
        cloudCache.Business.Errors.NoteDoesntExistError: If a note with the given ID doesn't exist for this user.

    """

    note = db.query(Note).filter_by(id=note_id).first()

    if not note:
        message = "Note with ID '{}' doesn't exist.".format(note_id)
        raise NoteDoesntExistError(message)

    if note.notebook.user != user:
        message = "The note with ID '{}' doesn't belong to you ({}).".format(note_id, user.username)
        raise NoteDoesntExistError(message)

    db.delete(note)
    db.commit()