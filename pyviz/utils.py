"""
Wrapper functions to assist the datamodel.
"""
from copy import copy
from enum import Enum
from typing import Any, TypeVar

from pyviz.datamodel import Var, Method, ModuleMethod, Class

AwaitableMethod = TypeVar("AwaitableMethod", Method, ModuleMethod)


def Async(method: AwaitableMethod) -> AwaitableMethod:
    """
    Args:
        method (AwaitableMethod): The method to mark as asynchronous.
    Returns:
        AwaitableMethod: An asynchronous method. Copy if not module method.
    """
    if not isinstance(method, ModuleMethod):
        m = copy(method)
    else:
        m = method

    m.is_async = True
    return m


def Cls(method: Method) -> Method:
    """
    Args:
        method (Method): The method to mark as a classmethod.
    Returns:
        Method: A classmethod copy of the method.
    """
    m = copy(method)
    m.is_cls = True
    return m


def Abstract(method: Method) -> Method:
    """
    Args:
        method (Method): The method to mark as a abstract.
    Returns:
        Method: An abstract copy of the method.
    """
    m = copy(method)
    m.is_abstract = True
    return m

