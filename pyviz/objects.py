import re
from typing import List, Optional, Union

_first_cap_re = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")


def to_underscore(name: str) -> str:
    """
    Converts a camelCase string to underscore_format.
    """
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1).lower()


class Property:
    name: str
    type: str

    def __init__(self, name: str, type: Union["Class", str]):
        self.name = name
        if isinstance(type, Class):
            self.type = type.name
        else:
            self.type = type


class Param:
    name: str
    type: str

    def __init__(self, name: str, type: Union["Class", str]):
        self.name = name
        if isinstance(type, Class):
            self.type = type.name
        else:
            self.type = type


class ModuleFunction:
    name: str
    params: List[Param]
    return_type: str

    is_async: bool

    def __init__(
        self,
        name: str,
        params: Optional[List[Param]] = None,
        return_type: Optional[str] = None,
        is_async: bool = False,
    ):
        self.name = name
        self.params = params if params else []
        self.return_type = return_type
        self.is_async = is_async


class Method:
    name: str
    params: List[Param]
    return_type: str

    is_abstract: bool
    is_async: bool
    is_classmethod: bool

    def __init__(
        self,
        name: str,
        params: Optional[List[Param]] = None,
        return_type: Optional[str] = None,
        is_abstract: bool = False,
        is_async: bool = False,
        is_classmethod: bool = False,
    ):
        self.name = name
        self.params = params if params else []
        self.return_type = return_type
        self.is_async = is_async


class Class:
    name: str
    properties: List[Property]
    methods: List[Method]
    inherits: List["Class"]

    def __init__(
        self,
        name: str,
        properties: Optional[List[Property]] = None,
        methods: Optional[List[Method]] = None,
    ):
        self.name = name
        self.methods = methods if methods else []
        self.properties = properties if properties else []

    def as_param(self, name: Optional[str] = None):
        if not name:
            name = to_underscore(self.name)
        return Param(name, type=self.name)

    def as_tparam(self, name: Optional[str] = None):
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Param(name, type=f"Type[{self.name}]")

    def as_prop(self, name: Optional[str] = None):
        if not name:
            name = to_underscore(self.name)
        return Property(name, type=self.name)

    def as_tprop(self, name: Optional[str] = None) -> Property:
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Property(name, type=f"Type[{self.name}]")
