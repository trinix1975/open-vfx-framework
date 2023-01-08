
import ctypes
# from tx.exceptions import * # I had weird intermitent errors when loading from here

def isinstance(object, class_type):
    """
    Replace the standard isinstance.

    The standard comparison does not work if one of the two class we compare are from a different module
    and have been imported differently, with absolute path vs from <module> import <class>. The problem
    is that those two class definitions are a different object, therefore they are not equal. You can
    confirm this by looking at their class object id (not the class object instance id).

    Use the class name and class module location in order to decide whether it is the same class or not.
    """
    object_class_path = '{}.{}'.format(object.__class__.__module__, object.__class__.__name__)
    class_type_path = '{}.{}'.format(class_type.__module__, class_type.__name__)
    if object_class_path == class_type_path:
        return True
    else:
        return False

def get_object(id):
    """
    Return the python object associated with the provided id
    """
    if type(id) == int: # use directly the id
        value = id
    elif type(id) == str: # convert the hexadecimal
        value = int(id, 16)
    return ctypes.cast(value, ctypes.py_object).value
