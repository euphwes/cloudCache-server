""" Module for the AccessHandler class in the cloudCache REST API. """

from . import AuthorizeHandler

from cloudCache.Business.Models.UserAccessToken import create_access_token
from cloudCache.Business.Errors import InvalidApiKeyError, UserDoesntExistError

# -------------------------------------------------------------------------------------------------

class AccessHandler(AuthorizeHandler):
    """ The request handler for creating and delivering cloudCache UserAccessTokens. """

    def get(self, username, api_key):
        """ Handles creating an access token for a given username, if they submit the correct API
        key. If the key is invalid, or the user doesn't exist, and appropriate error message is
        returned with the correct HTTP status code. If everything works out, the access token is
        returned. """

        try:
            token = create_access_token(username, api_key)
            response = {'access token': token.to_ordered_dict()}

        except UserDoesntExistError as e:
            self.set_status(404) # Not Found
            response = {'message': str(e)}

        except InvalidApiKeyError as e:
            self.set_status(401) # unauthenticated
            response = {'message': str(e)}

        self.write(response)
