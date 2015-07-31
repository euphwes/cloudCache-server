""" Module for the UserHandler class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models import User, DB_SESSION as db
from cloudCache.Business.Models.User import create_user
from cloudCache.Business.Errors import UserAlreadyExistsError, UserDoesntExistError

# -------------------------------------------------------------------------------------------------

# /users/{username}

class UserHandler(AuthorizeHandler):
    """ The request handler for managing cloudCache users. """

    def post(self, **kwargs):
        """ Implements HTTP POST for the UserHandler. Creates a new user. The user must provide an
        HTTP body of the type application/json, with the following format:

        {
            "username"  : "jswanson",
            "first_name": "Joe",
            "last_name" : "Swanson",
            "email"     : "jswanson@gmail.com"
        }

        Returns the user ID and API key if successful, or an error message otherwise. """

        info = json_decode(self.request.body)

        try:
            username   = info['username']
            first_name = info['first_name']
            last_name  = info['last_name']
            email      = info['email']
            user = create_user(username, first_name, last_name, email)

            response = {
                'user_id': user.id,
                'api_key': user.api_key
            }

        except UserAlreadyExistsError as error:
            self.set_status(409) # Conflict
            response = {'message': str(error)}

        except KeyError:
            self.set_status(400) # Bad Request
            message = 'Invalid POST body. Must include username, first and last names, and email.'
            response = {'message': message}

        self.write(response)


    def get(self, username):
        """ Implements the HTTP GET call on /users/{username}. If the caller does not provide a
        a username, the call will retrieve details for all users in the system. If the caller
        provides a username, the call will retrieve all details for that user. """

        if not username:
            self.authorize()

        # looking for a specific user
        if username:
            user = db.query(User).filter_by(username=username).first()
            if user:
                response = {'user': user.to_ordered_dict()}
            else:
                self.set_status(404) # Not Found
                response = {'message': 'The user "{}" does not exist.'.format(username)}

        # Get all users
        else:
            users = [{'id': user.id, 'username': user.username} for user in db.query(User).all()]
            response = {'users' : users}

        self.write(response)
