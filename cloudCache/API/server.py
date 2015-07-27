""" The cloudCache REST API. Intended for use in cloudCache CLI and Android apps. """

import tornado.web
import tornado.ioloop

from Handlers import UserHandler

# -------------------------------------------------------------------------------------------------

SERVER_PORT = 8888

# -------------------------------------------------------------------------------------------------

def main():
    """ Runs the server. """

    routes = [(r'/users/?(?P<username>[a-zA-Z0-9_-]+)?', UserHandler)]

    application = tornado.web.Application(routes)
    application.listen(SERVER_PORT)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
