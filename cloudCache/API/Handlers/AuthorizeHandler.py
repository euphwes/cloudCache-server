import arrow
import tornado.web
from cloudCache.Business.Models import DB_SESSION as db, User, UserAccessToken
from cloudCache.Business.Models.UserAccessToken import get_user_for_token

# -------------------------------------------------------------------------------------------------

class AuthorizeHandler(tornado.web.RequestHandler):
    """ Provides an 'authorize' interface to tornado.web.RequestHandler, which will authorize a
    user for a cloudCache handler web request via access token and username. """


    def authorize(self):
        """ Check username and access token are provided, and that they're valid and have not expired. """

        message  = 'You are not authorized for this action. '
        message += 'Please check that you have supplied a username and access token, '
        message += 'that the username exists, and your access token is valid and has not expired.'

        access_token = self.request.headers.get('access token')

        if not access_token:
            self.write({'message': message})
            raise tornado.web.Finish()

        user = get_user_for_token(access_token)

        if not user:
            self.write({'message': message})
            raise tornado.web.Finish()

        self.current_user = user
