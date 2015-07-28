""" __init__ for cloudCache.API. Contains utility functions. """

import arrow
from cloudCache.Business.Models import DB_SESSION as db, User, Note, Notebook, UserAccessToken

# -------------------------------------------------------------------------------------------------

def _purge_expired_tokens():
    """ Delete any UserAccessTokens from the database which are expired (older than one hour). """

    all_tokens = db.query(UserAccessToken).all()
    expired_tokens = [t for t in all_tokens if arrow.get(t.expires_on) <= arrow.now()]

    for expired_token in expired_tokens:
        db.delete(expired_token)

    db.commit()


def authorize(headers):
    """ Check username and access token are provided, and that they're valid and have not expired. """

    username = headers.get('username')
    access_token = headers.get('access token')

    if not username or not access_token:
        return False

    _purge_expired_tokens()

    user = db.query(User).filter_by(username=username).first()
    token = db.query(UserAccessToken).filter_by(user=user, access_token=access_token).first()

    if not token:
        return False

    return True
