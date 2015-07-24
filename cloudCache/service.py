""" The cloudCache REST API. Intended for use in future CLI and Android apps. """

import tornado.web
import tornado.ioloop

from tornroutes import route

# -------------------------------------------------------------------------------------------------

SERVER_PORT = 8888

# -------------------------------------------------------------------------------------------------

@route('/cache/item/(.+)')
class GetCacheItemHandler(tornado.web.RequestHandler):
    """ The main API handler for updating and retrieving cloudCache entries. """

    def get(self, key):
        raise tornado.web.HTTPError(404)


    def put(self, key):
        raise tornado.web.HTTPError(404)

# -------------------------------------------------------------------------------------------------

def main():
    """ Runs the server. """

    application = tornado.web.Application(route.get_routes())
    application.listen(SERVER_PORT)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()


# curl -I -X GET http://localhost:8888/cache/item/wes
