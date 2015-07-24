""" Init for cloudCache errors package. """

# -------------------------------------------------------------------------------------------------

class CloudCacheError(Exception):
    """ Base exception class for all cloudCache app errors. """

    def __init__(self, message):
        super().__init__(message)

# -------------------------------------------------------------------------------------------------

class UserDoesntExistError(CloudCacheError):
    """ Raised when a user doesn't exist for a specified username. """

class UserAlreadyExistsError(CloudCacheError):
    """ Raised when a given username is already taken. """

class InvalidApiKeyError(CloudCacheError):
    """ Raised when an incorrect API key is provided for a specified username. """

class NotebookAlreadyExistsError(CloudCacheError):
    """ Raised when attempting to create a Notebook for a specific user, and a Notebook with that
    name already exists for that user. """

class NoteAlreadyExistsError(CloudCacheError):
    """ Raised when attempting to create a Note for a specific notebook, and a Note with that key
    already exists for that notebook. """
