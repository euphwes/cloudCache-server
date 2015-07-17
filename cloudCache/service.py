""" A REST API for the cloudCache application. """

import tornado.web
import tornado.ioloop

# -------------------------------------------------------------------------------------------------

class CacheItemHandler(tornado.web.RequestHandler):
    """ The main API handler for creating, updating, and retrieving cloudCache entries. """

    def get(self, key, value):
        print("{}: {}".format(key, value))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    routes = [(r"/cache/(.+)/(.+)", CacheItemHandler)]

    application = tornado.web.Application(routes)
    application.listen(8888)

    tornado.ioloop.IOLoop.instance().start()

# curl -I -X GET http://localhost:8888/cache/name/wes
