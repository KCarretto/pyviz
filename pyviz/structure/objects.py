from abc import ABCMeta, abstractmethod
from typing import Dict, List, NamedTuple, Optional, TypeVar
from enum import Enum

from pyviz.structure.base import BaseNode, to_underscore


class Param(BaseNode):
    """
    Represents a parameter to a function.
    """


class Property(BaseNode):
    """
    Represents an instance read-only attribute of an object type.
    """

    is_classproperty: bool = False


class Global(BaseNode):
    """
    Represents a global value.
    """


class Constant(BaseNode):
    """
    Represents a global constant that does not change.
    """


class ModuleFunction(BaseNode):
    """
    Represents a module level function.
    """

    params: List[Param] = []
    is_awaitable: bool = False

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self.params = []
        self.is_awaitable = False
        super().__init__(*args, **kwargs)


class Method(BaseNode):
    """
    A function that is to be rendered as a component.
    """

    params: List[Param] = []
    is_awaitable: bool = False
    is_abstract: bool = False
    is_classmethod: bool = False

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self.params = []
        self.is_awaitable = False
        self.is_abstract = False
        self.is_classmethod = False
        super().__init__(*args, **kwargs)


class Class(BaseNode):
    """
    Represents a class.
    """

    properties: List[Property]

    _abstract_cls_methods: List[Method]
    _abstract_methods: List[Method]
    _class_methods: List[Method]
    _methods: List[Method]

    _inherits: List["Class"]
    _type_deps: List[BaseNode]

    def __init__(self, *args, props=List[Property], methods=List[Method], **kwargs):
        self._props = []
        self._abstract_cls_methods = []
        self._abstract_methods = []
        self._class_methods = []
        self._methods = []
        self._inherits = []
        self._type_deps = []

        super().__init__(*args, **kwargs)

        self._sort_methods(methods)

        if not self.type:
            self.type = self.name

    def _sort_methods(self, methods: List[Method]) -> None:
        """
        Ensures methods are categorized appropriately.
        """
        abstract_classmethods = []
        abstract_methods = []
        class_methods = []
        methods = []

        for m in methods:
            if m.is_abstract:
                if m.is_classmethod:
                    abstract_methods.append(m)
                else:
                    abstract_methods.append(m)
            else:
                if m.is_classmethod:
                    class_methods.append(m)
                else:
                    methods.append(m)
        self._abstract_cls_methods = abstract_classmethods
        self._abstract_methods = abstract_methods
        self._class_methods = class_methods
        self._methods = methods

    @property
    def abstract_class_methods(self) -> List[Method]:
        return self._abstract_cls_methods

    @property
    def abstract_methods(self) -> List[Method]:
        return self._abstract_methods

    @property
    def class_methods(self) -> List[Method]:
        return self._abstract_methods

    @property
    def methods(self) -> List[Method]:
        return self._methods

    def type_prop(self, name: Optional[str] = None) -> Property:
        """
        Return this classes Type as a property.
        """
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Property(name, type=f"Type[{self.type}]")

    def type_param(self, name: Optional[str] = None) -> Param:
        """
        Return this classes Type as a param.
        """
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Param(name, type=f"Type[{self.type}]")

    def prop(self, name: Optional[str] = None) -> Property:
        """
        Return this class as a property.
        """
        if not name:
            name = to_underscore(self.name)
        return Property(name, type=self.type)

    def param(self, name: Optional[str] = None) -> Param:
        """
        Return this class as a param.
        """
        if not name:
            name = to_underscore(self.name)
        return Param(name, type=self.type)

    def inherits(self, cls: "Class") -> None:
        """
        Mark this class as inheriting another class.
        """
        self._inherits.append(cls)
