""" Module for the UserHandler class in the cloudCache REST API. """

import tornado.web
from tornado.escape import json_decode

from cloudCache.Business.Models import User, DB_SESSION as db
from cloudCache.Business.Models.User import create_user
from cloudCache.Business.Errors import UserAlreadyExistsError, UserDoesntExistError

from cloudCache.API import authorize

# -------------------------------------------------------------------------------------------------

class UserHandler(tornado.web.RequestHandler):
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
            response = {
                'status' : 'Error',
                'message': str(error)
            }

        self.write(response)


    def get(self, username):

        # looking for a specific user
        if username is not None:
            user = db.query(User).filter_by(username=username).first()
            if user:
                response = {
                    'status': 'OK',
                    'user'  : user.to_ordered_dict()
                }
            else:
                response = {
                    'status': 'Error',
                    'message': 'The user "{}" does not exist.'.format(username)
                }

        # Get all users
        else:
            if not authorize(self.request.headers):
                message = 'You are not authorized for this action. '
                message += 'Please check that you have supplied a username and access token, '
                message += 'that the username exists, and your access token is valid and has not expired.'
                response = {
                    'status':  'Error',
                    'message': message
                }
                self.write(response)

            users = [user.to_ordered_dict() for user in db.query(User).all()]
            response = {
                'status': 'OK',
                'users' : users
            }

        self.write(response)
