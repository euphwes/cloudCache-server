""" A REST API for the cloudCache application. """

import tornado.web
import tornado.ioloop

# -------------------------------------------------------------------------------------------------

SERVER_PORT = 8888

# -------------------------------------------------------------------------------------------------

class CacheItemHandler(tornado.web.RequestHandler):
    """ The main API handler for creating, updating, and retrieving cloudCache entries. """

    def get(self, key, value):
        print("{}: {}".format(key, value))

# -------------------------------------------------------------------------------------------------

def main():
    """ Runs the server. """

    routes = [(r"/cache/(.+)/(.+)", CacheItemHandler)]

    application = tornado.web.Application(routes)
    application.listen(SERVER_PORT)

    tornado.ioloop.IOLoop.instance().start()

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()

# curl -I -X GET http://localhost:8888/cache/name/wes
