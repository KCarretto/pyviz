"""
Wrapper functions to assist the datamodel.
"""
from copy import copy
from enum import Enum
from typing import Any

from pyviz.datamodel import Var, Method, Class


def Async(method: Method) -> Method:
    """
    Args:
        method (Method): The method to mark as asynchronous.
    Returns:
        Method: An asynchronous copy of the method.
    """
    m = copy(method)
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


class Wrapper(Enum):
    TYPE: str = "Type"
    UNION: str = "Union"
    CALLABLE: str = "Callable"
    OPTIONAL: str = "Optional"
    DICT: str = "Dict"
    LIST: str = "List"
    TUPLE: str = "Tuple"
    NAMED_TUPLE: str = "NamedTuple"
    GENERIC: str = "Generic"
    SEQUENCE: str = "Sequence"
    MAPPING: str = "Mapping"
    ITERABLE: str = "Iterable"
    CLASSVAR: str = "ClassVar"


def Wrap(wrapper: Wrapper, *args) -> str:
    """
    Coerce the arguments and then wrap them in the given wrapper.

    Args:
        wrapper (Wrapper): The type of wrapper to use.
        *args: Positional arguments, may include str, Var, Method, Class. Other types with be cast
            using str()
    Returns:
        str: The string with coerced arguments wrapped by the wrapper.
    """

    def _wrap_coerce(arg: Any) -> str:
        if isinstance(arg, str):
            return arg
        if isinstance(arg, (Class, Method)):
            return arg.name
        if isinstance(arg, (Var)):
            return arg.type
        return str(arg)

    params = ", ".join(_wrap_coerce(arg) for arg in args)
    return f"{wrapper.value}[{params}]"
