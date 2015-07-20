""" A module which contains cloudCache User-related errors. """

# -------------------------------------------------------------------------------------------------

from . import CloudCacheError

# -------------------------------------------------------------------------------------------------

class UserAlreadyExistsError(CloudCacheError):
    """ A custom error which is thrown when a given username is already taken. """

    def __init__(self):
        super().__init__()
