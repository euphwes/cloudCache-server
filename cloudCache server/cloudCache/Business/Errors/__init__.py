""" Init for cloudCache errors package. """

# -------------------------------------------------------------------------------------------------

class CloudCacheError(Exception):
    """ Base exception class for all cloudCache app errors. """

    def __init__(self, message):
        super().__init__(message)

# -------------------------------------------------------------------------------------------------

from .UserErrors import UserAlreadyExistsError
from .NotebookErrors import NotebookAlreadyExistsError
