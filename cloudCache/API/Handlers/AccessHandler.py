""" Module for the AccessHandler class in the cloudCache REST API. """

from . import AuthorizeHandler

from cloudCache.Business.Models import User, UserAccessToken, DB_SESSION as db
from cloudCache.Business.Models.UserAccessToken import create_access_token
from cloudCache.Business.Errors import InvalidApiKeyError, UserDoesntExistError

# -------------------------------------------------------------------------------------------------

class AccessHandler(AuthorizeHandler):
    """ The request handler for creating and delivering cloudCache UserAccessTokens. """

    def get(self, username, api_key):

        try:
            token = create_access_token(username, api_key)
            response = {
                'status'      : 'OK',
                'access token': token.to_ordered_dict()
            }

        except (InvalidApiKeyError, UserDoesntExistError) as e:
            response = {
                'status' : 'Error',
                'message': str(e)
            }

        self.write(response)
