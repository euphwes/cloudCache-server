""" A module which contains cloudCache Notebook-related errors. """

# -------------------------------------------------------------------------------------------------

from . import CloudCacheError

# -------------------------------------------------------------------------------------------------

class NotebookAlreadyExistsError(CloudCacheError):
    """ A custom error which is thrown when attempting to create a Notebook for a specific user,
    and a Notebook with that name already exists for that user. """
