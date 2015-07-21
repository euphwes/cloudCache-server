""" Init for cloudCache errors package. """

# -------------------------------------------------------------------------------------------------

class CloudCacheError(Exception):
    """ Base exception class for all cloudCache app errors. """

    def __init__(self, message):
        super().__init__(message)

# -------------------------------------------------------------------------------------------------

class UserAlreadyExistsError(CloudCacheError):
    """ A custom error which is thrown when a given username is already taken. """

class NotebookAlreadyExistsError(CloudCacheError):
    """ A custom error which is thrown when attempting to create a Notebook for a specific user,
    and a Notebook with that name already exists for that user. """

class NoteAlreadyExistsError(CloudCacheError):
    """ A custom error which is thrown when attempting to create a Note for a specific notebook,
    and a Note with that key already exists for that notebook. """
