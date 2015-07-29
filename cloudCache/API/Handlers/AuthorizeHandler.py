import arrow
import tornado.web
from cloudCache.Business.Models import DB_SESSION as db, User, UserAccessToken
from cloudCache.Business.Models.UserAccessToken import delete_expired_tokens

# -------------------------------------------------------------------------------------------------

class AuthorizeHandler(tornado.web.RequestHandler):
    """ Provides an 'authorize' interface to tornado.web.RequestHandler, which will authorize a
    user for a cloudCache handler web request via access token and username. """


    def authorize(self):
        """ Check username and access token are provided, and that they're valid and have not expired. """

        message  = 'You are not authorized for this action. '
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
            raise tornado.web.Finish()

        delete_expired_tokens()

        user = db.query(User).filter_by(username=username).first()
        token = db.query(UserAccessToken).filter_by(user=user, access_token=access_token).first()

        if not token:
            self.write(fail_response)
            raise tornado.web.Finish()
