# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class MethodDoesNotExist(Error):
    """Raised when the input value is wrong"""
    pass


