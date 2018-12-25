"""
Collection of helper functions for semantic sugar.
"""
import re

from pyviz.structure.base import BaseNode
from pyviz.structure.objects import Property, Method, Class


def Wrap(wrapper: str, *args) -> str:
    """
    Wrap arguments in a container (i.e. List[myclass], Dict[str, myclass])

    Args:
        wrapper (str): The wrapping container (i.e. List)
        *args (Union[str, BaseNode]): The remaining arguments to wrap.
    Returns:
        str: Wrapped string formatted by the given types.
    """
    types = []
    for arg in args:
        if isinstance(arg, BaseNode):
            types.append(arg.type)
        else:
            types.append(arg)
    return f"{wrapper}[{', '.join(types)}]"


def ClassProperty(prop: Property) -> Property:
    """
    Returns the property as a class property,
    """
    prop.is_classproperty = True
    return prop


def Cls(method: Method) -> Method:
    """
    Return the method as a classmethod.
    """
    method.is_classmethod = True
    return method


def Async(method: Method) -> Method:
    """
    Return a method as an async method.
    """
    method.is_awaitable = True
    return method


def Abstract(method: Method) -> Method:
    """
    Return a method as an abstract method.
    """
    method.is_abstract = True
    return method
