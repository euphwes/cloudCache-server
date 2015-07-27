""" Module for the UserHandler class in the cloudCache REST API. """

import tornado.web
from tornado.escape import json_decode

from cloudCache.Business.Models.User import create_user
from cloudCache.Business.Errors import UserAlreadyExistsError

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
