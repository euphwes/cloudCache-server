""" Contains UserAccessToken model, and utility functions for manipulating this model. """

# pylint: disable=W0232,C0103
# Disable no-init warning on UserAccessToken model
# Disable name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from . import User
from ..Errors import UserDoesntExistError, InvalidApiKeyError

from arrow import utcnow
from uuid import uuid4 as guid

# -------------------------------------------------------------------------------------------------

class UserAccessToken(SQL_ALCHEMY_BASE):
    """ Represents a cloudCache UserAccessToken. """

    __tablename__ = 'USER_ACCESS_TOKEN'

    id           = Column(Integer, primary_key=True)
    user_id      = Column(Integer, ForeignKey('USER.id'))
    access_token = Column(String(32))
    expires_on   = Column(ArrowType)

    user = relationship(User)


    def __repr__(self):
        self_repr = 'UserAccessToken(user_id={uid}, access_token="{token}", expires_on="{exp}")'
        return self_repr.format(uid=self.user_id, token=self.access_token, exp=self.expires_on)

    def __str__(self):
        self_str = '[{u}] {token} - {exp}'
        return self_str.format(u=self.user.username, token=self.access_token, exp=self.expires_on)

# -------------------------------------------------------------------------------------------------

def create_access_token(username, api_key):
    """ Creates a UserAccessToken for the User whose username is supplied, if the API key supplied
    is valid for that user. The UserAccessToken is only valid for 1 hour from the time that it is
    issued.

    Args:
        username (string): The username of the User requesting the access token.
        api_key (string): The API key of the User requesting the access token.

    Returns:
        cloudCache.Business.Models.UserAccessToken: The newly-generated access token.

    Raises:
        cloudCache.Business.Errors.UserDoesntExistError: If `username` doesn't exist.
        cloudCache.Business.Errors.InvalidApiKeyError: If `api_key` doesn't match
        `username`'s api_key.

    """

    user = db.query(User).filter_by(username=username).first()
    if not user:
        message = 'The user "{}" does not exist.'.format(username)
        raise UserDoesntExistError(message)

    if user.api_key != api_key:
        message = 'The API key provided for user "{}" is invalid.'.format(api_key)
        raise InvalidApiKeyError(message)

    # generate new guid for access token, and set the expiration date 1 hour from right now
    token      = str(guid()).upper().replace('-', '')
    expires_on = utcnow().replace(hours=1)

    user_access_token = UserAccessToken(user=user, access_token=token, expires_on=expires_on)
    db.add(user_access_token)
    db.commit()

    return user_access_token
