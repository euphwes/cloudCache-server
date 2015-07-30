import arrow
import tornado.web
from cloudCache.Business.Models import DB_SESSION as db, User, UserAccessToken
from cloudCache.Business.Models.UserAccessToken import get_user_for_token

# -------------------------------------------------------------------------------------------------

class AuthorizeHandler(tornado.web.RequestHandler):
    """ Provides an 'authorize' interface to tornado.web.RequestHandler, which will authorize a
    user for a cloudCache handler web request via access token and username. """


    def get_failure_response(self, exception):
        """ Returns a dict which is to be written as the RequestHandler's response. The status is
        'Error' and the message is the string representation of the provided exception, or the
        provided error message itself.

        Args:
            exception (Exception or string): The Exception which is the cause of the failure, or
                the error message to be delivered.

        Returns:
            dict: The dict object which is to be written as the response to this HTTP call.

        """

        resp = {
            'status' : 'Error',
            'message': str(exception)
        }

        return resp


    def authorize(self):
        """ Check username and access token are provided, and that they're valid and have not expired. """

        message  = 'You are not authorized for this action. '
        message += 'Please check that you have supplied a username and access token, '
        message += 'that the username exists, and your access token is valid and has not expired.'
        fail_response = self.get_failure_response(message)

        access_token = self.request.headers.get('access token')

        if not access_token:
            self.write(fail_response)
            raise tornado.web.Finish()

        user = get_user_for_token(access_token)

        if not user:
            self.write(fail_response)
            raise tornado.web.Finish()

        self.current_user = user
