# define Python user-defined exceptions
class TypeAxesError(Exception):
    """Raised when the type is not an Axes-object of matplotlib"""
    pass

class TypeListError(Exception):
    """Raised when the type is not a List"""
    pass

class TypeDictionaryError(Exception):
    """Raised when the type is not a Dictionary"""
    pass

class TypeIntegerError(Exception):
    """Raised when the type is not a List"""
    pass

class TypeDataFrameError(Exception):
    """Raised when the type is not a pandas DataFrame"""
    pass

class TypeStringError(Exception):
    """Raised when the type is not a String"""
    pass

class TypeBooleanError(Exception):
    """Raised when the type is not a List"""
    pass