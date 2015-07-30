""" Module for the UserHandler class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models import User, DB_SESSION as db
from cloudCache.Business.Models.User import create_user
from cloudCache.Business.Errors import UserAlreadyExistsError, UserDoesntExistError

# -------------------------------------------------------------------------------------------------

class UserHandler(AuthorizeHandler):
    """ The request handler for managing cloudCache users. """

    def post(self, **kwargs):
        info = json_decode(self.request.body)

        try:
            username   = info['username']
            first_name = info['first_name']
            last_name  = info['last_name']
            email      = info['email']
            user = create_user(username, first_name, last_name, email)
            response = {
                'status': 'OK',
                'user'  : user.to_ordered_dict()
            }

        except UserAlreadyExistsError as error:
            response = self.get_failure_response(error)

        self.write(response)


    def get(self, username):

        if not username:
            self.authorize()

        # looking for a specific user
        if username:
            user = db.query(User).filter_by(username=username).first()
            if user:
                response = {
                    'status': 'OK',
                    'user'  : user.to_ordered_dict()
                }
            else:
                message = 'The user "{}" does not exist.'.format(username)
                response = self.get_failure_response(message)

        # Get all users
        else:
            users = [user.to_ordered_dict() for user in db.query(User).all()]
            response = {
                'status': 'OK',
                'users' : users
            }

        self.write(response)
