""" Init for cloudCache errors package. """

# -------------------------------------------------------------------------------------------------

class CloudCacheError(Exception):
    """ Base exception class for all cloudCache app errors. """

    def __init__(self):
        super().__init__()

# -------------------------------------------------------------------------------------------------

from .UserErrors import UserAlreadyExistsError
