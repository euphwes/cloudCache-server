""" Module for the Notes class in the cloudCache REST API. """

from tornado.escape import json_decode

from . import AuthorizeHandler

from cloudCache.Business.Models.Note import get_note
from cloudCache.Business.Errors import NoteDoesntExistError

# -------------------------------------------------------------------------------------------------

# /notes/{note}

class NoteHandler(AuthorizeHandler):
    """ The request handler for managing individual cloudCache notes. """

    def get(self, **kwargs):
        """ Implements the HTTP GET call on /notes/{note}. """
        self.authorize()

        note_id = kwargs.get('note')

        try:
            # will raise ValueError if the note_id isn't parseable as an int
            int(note_id)
            note = get_note(note_id, self.current_user)
            response = note.to_ordered_dict()

        except NoteDoesntExistError as error:
            self.set_status(404)  # Not Found
            response = {'message': str(error)}

        except ValueError:
            self.set_status(400) # Bad Request
            message = 'Invalid note argument. '
            message += 'You must supply the note ID, not the note name.'
            response = {'message': message}

        self.write(response)
