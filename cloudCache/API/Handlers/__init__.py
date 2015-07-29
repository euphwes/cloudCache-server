""" __init__ for cloudCache.API.Handlers. """

import arrow
import tornado.web
from cloudCache.Business.Models import DB_SESSION as db, User, UserAccessToken

# -------------------------------------------------------------------------------------------------

class AuthorizeHandler(tornado.web.RequestHandler):
    """ Provides an 'authorize' interface to tornado.web.RequestHandler, which will authorize a
    user for a cloudCache handler web request via access token and username. """

    def _purge_expired_tokens(self):
        """ Delete any UserAccessTokens from the database which are expired (older than one hour). """

        all_tokens = db.query(UserAccessToken).all()
        expired_tokens = [t for t in all_tokens if arrow.get(t.expires_on) <= arrow.now()]

        for expired_token in expired_tokens:
            db.delete(expired_token)

        db.commit()


    def authorize(self):
        """ Check username and access token are provided, and that they're valid and have not expired. """

        message = 'You are not authorized for this action. '
        message += 'Please check that you have supplied a username and access token, '
        message += 'that the username exists, and your access token is valid and has not expired.'
        fail_response = {
            'status':  'Error',
            'message': message
        }

        username     = self.request.headers.get('username')
        access_token = self.request.headers.get('access token')

        if not (username and access_token):
            self.write(fail_response)
            return False

        self._purge_expired_tokens()

        user = db.query(User).filter_by(username=username).first()
        token = db.query(UserAccessToken).filter_by(user=user, access_token=access_token).first()

        if not token:
            self.write(fail_response)
            return False

        return True

# -------------------------------------------------------------------------------------------------

from .UserHandler import UserHandler
from .AccessHandler import AccessHandler
from .NotebookHandler import NotebookHandler
