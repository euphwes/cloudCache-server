""" Contains User SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103
# disable no-init warning on User model, and name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from ..Errors import UserAlreadyExistsError

from arrow import now as arrow_now
from uuid import uuid4 as guid

# -------------------------------------------------------------------------------------------------

class User(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache user. """

    __tablename__ = 'USER'

    id            = Column(Integer, primary_key=True)
    username      = Column(String(255), unique=True)
    first_name    = Column(String(255))
    last_name     = Column(String(255))
    email_address = Column(String(255))
    api_key       = Column(String(32))
    date_joined   = Column(ArrowType, default=arrow_now)

# -------------------------------------------------------------------------------------------------

def create_user(username, first_name, last_name, email_address):
    """ Creates a User entry in the database, and returns the user object to the caller.

    Args:
        username (string): The new user's username.
        first_name (string): The new user's first name.
        last_name (string): The new user's last name.
        email_address (string): The new user's email address.

    Returns:
        cloudCache.Business.Models.User: The newly-created User.

    Raises:
        cloudCache.Business.Errors.UserAlreadyExistsError: If `username` is already taken.

    """

    if db.query(User).filter_by(username=username).first():
        message = 'The username {} is already taken by another user'.format(username)
        raise UserAlreadyExistsError(message)

    api_key = str(guid()).upper().replace('-', '')

    new_user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email_address=email_address,
                    api_key=api_key)

    db.add(new_user)
    db.commit()

    return new_user