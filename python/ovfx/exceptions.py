"""
OpenVFX exceptions

DO NOT RELOAD THIS MODULE. Otherwise it may introduce strange bugs like the exceptions are sometimes not visible.
"""



class OvfxError(Exception):
    """
    Base class Ovfx exceptions
    """
    def __init__(self, msg=None):
        if not msg:
            msg = 'Error in a Tx module.'
        super(OvfxError, self).__init__(msg)


class AlreadyExists(OvfxError):
    """
    Raised when trying to create a file or directory which already exists.
    """
    def __init__(self, msg=None, item=None):
        if msg is None:
            if item is None:
                msg = 'An item already exists.'
            else:
                msg = 'The following item already exists: {} {}'.format(item, type(item))
        super(AlreadyExists, self).__init__(msg)
        self.item = item
        self.msg = msg


class NotFound(OvfxError):
    """
    Raised when an object is not found.
    """
    def __init__(self, msg=None, obj=None):
        if msg is None:
            if obj is None:
                msg = 'The object cannot be found.'
            else:
                msg = 'The following object cannot be found: {}'.format(obj)
        super(NotFound, self).__init__(msg)
        self.obj = obj
        self.msg = msg

class InvalidFormat(OvfxError):
    """
    Raised when a value is not in a valid format
    """
    def __init__(self, msg=None, value=None):
        if msg is None:
            if value is None:
                msg = 'The format is invalid.'
            else:
                msg = 'The following value has an unexpected format: {}'.format(value)
        super(InvalidFormat, self).__init__(msg)
        self.value = value
        self.msg = msg
