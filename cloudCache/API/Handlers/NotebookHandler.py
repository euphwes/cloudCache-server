""" Module for the NotebookHandler class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models import User, Notebook, DB_SESSION as db
from cloudCache.Business.Models.Notebook import create_notebook
from cloudCache.Business.Errors import NotebookAlreadyExistsError

# -------------------------------------------------------------------------------------------------

class NotebookHandler(AuthorizeHandler):
    """ The request handler for managing cloudCache notebooks. """

    def post(self, **kwargs):
        self.authorize()

        url_username = kwargs.get('username')

        if url_username != self.current_user.username:
            message = 'You ({}) cannot create a notebook for another user ({}).'
            message = message.format(header_username, url_username)
            self.write({
                'status' : 'Error',
                'message': message
            })
            return

        notebook_name = json_decode(self.request.body).get('notebook_name')
        user = db.query(User).filter_by(username=url_username).first()

        if not user:
            message = 'User "{}" doesn\'t exist.'.format(url_username)
            self.write({
                'status' : 'Error',
                'message': message
            })
            return

        try:
            notebook = create_notebook(notebook_name, user)
            response = {
                'status': 'OK',
                'notebook': notebook.to_ordered_dict()
            }
        except NotebookAlreadyExistsError as e:
            response = {
                'status': 'Error',
                'message': str(e)
            }

        self.write(response)
