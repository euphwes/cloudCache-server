""" Module for the NotebookHandler class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models import User, Notebook, DB_SESSION as db
from cloudCache.Business.Models.Notebook import create_notebook
from cloudCache.Business.Errors import NotebookAlreadyExistsError

# -------------------------------------------------------------------------------------------------

class NotebookHandler(AuthorizeHandler):
    """ The request handler for managing cloudCache notebooks. """


    def get(self, **kwargs):

        self.authorize()

        notebook = kwargs.get('notebook')

        if notebook:
            response = self.get_failure_response('Not implemented yet.')

        else:
            notebooks = db.query(Notebook).filter_by(user=self.current_user).all()
            notebooks = [notebook.to_ordered_dict() for notebook in notebooks]
            response = {
                'status': 'OK',
                'notebooks' : notebooks
            }

        self.write(response)



    def post(self, **kwargs):
        self.authorize()

        notebook_name = json_decode(self.request.body).get('notebook_name')

        try:
            notebook = create_notebook(notebook_name, self.current_user)
            response = {
                'status': 'OK',
                'notebook': notebook.to_ordered_dict()
            }
        except NotebookAlreadyExistsError as e:
            response = self.get_failure_response(e)

        self.write(response)
