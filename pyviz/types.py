"""
Convenient typing wrappers.
"""
from enum import Enum
from functools import partial
from typing import Any, Union, List, Optional

from pyviz.datamodel import Class, Method, Var


def _wrap_coerce(arg: Any) -> str:
    if isinstance(arg, str):
        return arg
    if isinstance(arg, (Class, Method)):
        return arg.name
    if isinstance(arg, (Var)):
        return arg.type
    return str(arg)


def wrap(wrapper: Optional[str], *args) -> str:
    """Wrap arguments in the provided wrapper."""
    params = ", ".join(_wrap_coerce(arg) for arg in args)
    if not wrapper:
        return f"[{params}]"
    return f"{wrapper}[{params}]"


TYPE = partial(wrap, "Type")
UNION = partial(wrap, "Union")
OPTIONAL = partial(wrap, "Optional")
DICT = partial(wrap, "Dict")
LIST = partial(wrap, "List")
TUPLE = partial(wrap, "Tuple")
NAMED_TUPLE = partial(wrap, "NamedTuple")
GENERIC = partial(wrap, "Generic")
SEQUENCE = partial(wrap, "Sequence")
MAPPING = partial(wrap, "Mapping")
ITERABLE = partial(wrap, "Iterable")
CLASS_VAR = partial(wrap, "ClassVar")


def CALLABLE(*params, return_type: Optional[Union[str, Class]] = None) -> str:
    """
    Callable[ [params], return_type] wrapper.
    """
    if not return_type:
        return_type = "None"
    if params:
        params: str = wrap(None, *params)
        return wrap("Callable", params, return_type)
    else:
        return wrap("Callable", "[]", return_type)

