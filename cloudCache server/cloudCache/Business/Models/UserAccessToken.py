""" Contains UserAccessToken model, and utility functions for manipulating this model. """

# pylint: disable=W0232,C0103
# Disable no-init warning on UserAccessToken model
# Disable name-too-short warning on `id` variable

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types import ArrowType

from . import SQL_ALCHEMY_BASE, DB_SESSION as db
from . import User

from arrow import now
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
        return self_repr.format(user_id=self.user_id, token=self.access_token, exp=self.expires_on)

    def __str__(self):
        self_str = '[{u}] {token} - {exp}'
        return self_str.format(u=self.user.username, token=self.access_token, exp=self.expires_on)
