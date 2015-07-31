""" Module for the NotebookHandler class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models import User, Notebook, DB_SESSION as db
from cloudCache.Business.Models.Notebook import create_notebook
from cloudCache.Business.Errors import NotebookAlreadyExistsError

# -------------------------------------------------------------------------------------------------

# /notebooks/{notebook}

class NotebookHandler(AuthorizeHandler):
    """ The request handler for managing cloudCache notebooks. """


    def get(self, **kwargs):
        """ Implements the HTTP GET call on /notebooks/{notebook}. If the user does not provide a
        a notebook, the call will retrieve details for all notebooks that belong to the
        authenticated user. If the caller provides a notebook, the call will retrieve all notes in
        that notebook. """

        self.authorize()

        notebook = kwargs.get('notebook')

        if notebook:
            self.set_status(500) # Not implemented
            response = {'message': 'Not yet implemented.'}

        else:
            notebooks = db.query(Notebook).filter_by(user=self.current_user).all()
            response  = {'notebooks': [notebook.name for notebook in notebooks]}

        self.write(response)



    def post(self, **kwargs):
        """ Implements the HTTP POST call on /notebooks. The user must provide an HTTP
        body of the type application/json, with the following format:

        {
            'notebook_name': 'My Awesome Notebook'
        }

        Returns the notebook ID if successful, or an error message otherwise. """

        self.authorize()

        info = json_decode(self.request.body)

        try:
            notebook_name = info['notebook_name']

            notebook = create_notebook(notebook_name, self.current_user)
            response = {'notebook_id': notebook.id}

        except NotebookAlreadyExistsError as e:
            self.set_status(409) # Conflict
            response = {'message': str(e)}

        except KeyError:
            self.set_status(400) # Bad Request
            message = 'Invalid POST body. Must include notebook_name.'
            response = {'message': message}

        self.write(response)
