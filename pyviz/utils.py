"""
Collection of helper functions for semantic sugar.
"""
import re

from pyviz.structure.base import BaseNode
from pyviz.structure.objects import Property, Method, Class


def Wrap(wrapper: str, *args) -> str:
    types = []
    for arg in args:
        if hasattr(arg, "name"):
            types.append(arg.name)
        else:
            types.append(arg)
    return f"{wrapper}[{', '.join(types)}]"


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
    method.is_async = True
    return method


def Abstract(method: Method) -> Method:
    """
    Return a method as an abstract method.
    """
    method.is_abstract = True
    return method
