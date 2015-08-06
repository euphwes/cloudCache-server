""" Contains User SQLAlchemy model, and utility functions for manipulating these models. """

# pylint: disable=W0232,C0103,E1101
# Disable no-init warning on User model
# Disable name-too-short warning on `id` variable
# User DOES have attribute "notebooks", it's created as a backref in Notebook model

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils.types import ArrowType, PasswordType

from . import SQL_ALCHEMY_BASE, JsonMixin, DB_SESSION as db
from ..Errors import UserAlreadyExistsError

from arrow import now as arrow_now
from uuid import uuid4 as guid

# -------------------------------------------------------------------------------------------------

class User(JsonMixin, SQL_ALCHEMY_BASE):
    """ Represents a cloudCache user.

    Attributes:
        id (int): This User's unique ID.
        username (string): This User's username.
        first_name (string): This User's first name.
        last_name (string): This User's last name.
        email_address (string): This User's email address.
        api_key (string): Randomly generated GUID which acts as a key for this user to obtain a
            temporary UserAccessToken.
        date_joined (Arrow): The date/time that this User account was created.

    """

    __tablename__ = 'USER'

    id            = Column(Integer, primary_key=True)
    username      = Column(String(255), unique=True)
    first_name    = Column(String(255))
    last_name     = Column(String(255))
    email_address = Column(String(255))
    api_key       = Column(String(32))
    date_joined   = Column(ArrowType, default=arrow_now)
    password      = Column(PasswordType(schemes=['pbkdf2_sha512']))


    def __repr__(self):
        s = 'User(username="{u}", first_name="{f}", last_name="{l}", email_address="{e}")'
        return s.format(u=self.username, f=self.first_name, l=self.last_name, e=self.email_address)

    def __str__(self):
        return self.username


    def to_ordered_dict(self):
        """ Returns an OrderedDict representation of this User. """

        kvp = {'notebooks': [notebook.to_ordered_dict() for notebook in self.notebooks]}
        return self._to_ordered_dict(_get_attributes(), additional_kvp=kvp)


    def to_json(self, compact=True):
        """ Returns a JSON representation of this User. """

        kvp = {'notebooks': [notebook.to_ordered_dict() for notebook in self.notebooks]}
        return self._to_json(_get_attributes(), compact=compact, additional_kvp=kvp)

# -------------------------------------------------------------------------------------------------

def _get_attributes():
    """ Returns a list of strings representing the User attributes which are to be serialized to
    JSON or an OrderedDict. """

    return ['username', 'id', 'first_name', 'last_name', 'email_address', 'api_key', 'date_joined']

# -------------------------------------------------------------------------------------------------

def create_user(username, first_name, last_name, email_address, password):
    """ Creates a User entry in the database, and returns the user object to the caller.

    Args:
        username (string): The new user's username.
        first_name (string): The new user's first name.
        last_name (string): The new user's last name.
        email_address (string): The new user's email address.
        password (string): The new user's password.

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
                    api_key=api_key,
                    password=password)

    db.add(new_user)
    db.commit()

    return new_user


def delete_user(user):
    """ Delete a user.

    Args:
        user (cloudCache.Business.Models.User): The user.

    """

    db.delete(user)
    db.commit()