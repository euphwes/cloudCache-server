""" The cloudCache REST API. Intended for use in cloudCache CLI and Android apps. """

import tornado.web
import tornado.ioloop

from Handlers import UserHandler, AccessHandler, NotebookHandler, NoteHandler

# -------------------------------------------------------------------------------------------------

SERVER_PORT = 8888

USERNAME_OPT = r'?(?P<username>[a-zA-Z0-9_-]+)?'
USERNAME_REQ = r'(?P<username>[a-zA-Z0-9_-]+)'
NOTEBOOK_OPT = r'?(?P<notebook>[a-zA-Z0-9_-]+)?'
NOTEBOOK_REQ = r'(?P<notebook>[a-zA-Z0-9_-]+)'
NOTE_OPT     = r'?(?P<note>[a-zA-Z0-9_-]+)?'
NOTE_REQ     = r'(?P<note>[a-zA-Z0-9_-]+)'
API_KEY_REQ  = r'(?P<api_key>[A-Z0-9]+)'

USER_HANDLER_URL     = '/users/{}'.format(USERNAME_OPT)
ACCESS_HANDLER_URL   = '/access/{}/{}'.format(USERNAME_REQ, API_KEY_REQ)
NOTEBOOK_HANDLER_URL = '/notebooks/{}'.format(NOTEBOOK_OPT)
NOTES_HANDLER_URL    = '/notebooks/{}/notes/{}'.format(NOTEBOOK_REQ, NOTE_OPT)

# -------------------------------------------------------------------------------------------------

def main():
    """ Runs the server. """

    routes = [(NOTES_HANDLER_URL, NoteHandler),
              (NOTEBOOK_HANDLER_URL, NotebookHandler),
              (USER_HANDLER_URL, UserHandler),
              (ACCESS_HANDLER_URL, AccessHandler)]

    application = tornado.web.Application(routes)
    application.listen(SERVER_PORT)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
