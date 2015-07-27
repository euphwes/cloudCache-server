""" The cloudCache REST API. Intended for use in cloudCache CLI and Android apps. """

import tornado.web
import tornado.ioloop
from tornado.escape import json_decode

from Business.Models.User import create_user
from Business.Errors import UserAlreadyExistsError

# -------------------------------------------------------------------------------------------------

SERVER_PORT = 8888

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
                'status': 'Error',
                'message': str(error)
            }

        self.write(response)


# -------------------------------------------------------------------------------------------------

def main():
    """ Runs the server. """

    routes = [(r'/users/?(?P<username>[a-zA-Z0-9_-]+)?', UserHandler)]

    application = tornado.web.Application(routes)
    application.listen(SERVER_PORT)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
