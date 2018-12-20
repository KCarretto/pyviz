from abc import ABCMeta, abstractmethod
from typing import Dict, List, NamedTuple, Optional, TypeVar
from enum import Enum

from pyviz.base import (
    UMLBase,
    IRenderable,
    SimpleRenderable,
    IRenderComponent,
    SimpleRenderComponent,
)
from pyviz.config import GraphConfig, UMLAttributes
from pyviz.fmt import DotFormatter, to_underscore


class Param(SimpleRenderComponent):
    """
    Represents a parameter to a function.
    """


class Property(SimpleRenderComponent):
    """
    Represents an instance read-only attribute of an object type.
    """

    is_classproperty: bool = False


def Wrap(wrapper: str, *args) -> str:
    """
    Wrap arguments in a container (i.e. List[myclass], Dict[str, myclass])

    Args:
        wrapper (str): The wrapping container (i.e. List)
        *args (Union[str, UMLBase]): The remaining arguments to wrap.
    Returns:
        str: Wrapped string formatted by the given types.
    """
    types = []
    for arg in args:
        if isinstance(arg, UMLBase):
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


class Global(SimpleRenderable):
    """
    Represents a global value.
    """


class Constant(SimpleRenderable):
    """
    Represents a global constant that does not change.
    """


class ModuleFunction(IRenderable):
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

    def get_attributes(self, uml_config: UMLAttributes) -> Optional[Dict[str, str]]:
        """
        Returns:
            Dict[str, str]: mapping of ModuleFunction attributes.
        """
        return uml_config.uml_module_function

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: mapping of UMLModuleFunction attributes.
        """
        return {"shape": "oval"}

    def render_label(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.render(fmt) for param in self.params])
        label = f"{self.name}({params}): {fmt.color_type(self.type)}"

        if self.is_awaitable:
            label = fmt.awaitable(label)

        return label


class Method(IRenderComponent):
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

    def render(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.render(fmt) for param in self.params])
        label = f"{self.name}({params})"

        if self.is_abstract:
            label = fmt.abstract(label)
        label = f"{label}: {fmt.color_type(self.type)}"
        if self.is_awaitable:
            label = fmt.awaitable(label)

        return label


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


class Class(IRenderable):
    """
    Represents a class.
    """

    properties: List[Property]
    methods: List[Method]

    def __init__(self, *args, **kwargs):

        self.properties = []
        self.methods = []

        super().__init__(*args, **kwargs)

    @property
    def type(self) -> str:
        """
        Returns:
            str: The type string for this node.
        """
        return self.name

    def type_prop(self, name: Optional[str] = None) -> Property:
        """
        Return this classes Type as a property.
        """
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Property(name, type=Wrap("Type", self.type))

    def type_param(self, name: Optional[str] = None) -> Param:
        """
        Return this classes Type as a param.
        """
        if not name:
            name = f"{to_underscore(self.name)}_cls"
        return Param(name, type=Wrap("Type", self.type))

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

    def get_attributes(self, uml_config: UMLAttributes) -> Optional[Dict[str, str]]:
        """
        Returns:
            Dict[str, str]: mapping of Class attributes.
        """
        return uml_config.uml_class

    def render_label(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot format HTML label for this node.
        """
        abstract_classmethods = []
        abstract_methods = []
        classmethods = []
        methods = []

        for m in self.methods:
            if m.is_abstract:
                if m.is_classmethod:
                    abstract_classmethods.append(m)
                else:
                    abstract_methods.append(m)
            else:
                if m.is_classmethod:
                    classmethods.append(m)
                else:
                    methods.append(m)

        label = "\n".join(
            filter(
                lambda x: x is not None,
                [
                    f"< {{<B>{self.name}</B>",
                    fmt.section("Properties", [prop.render(fmt) for prop in self.properties]),
                    fmt.section(
                        "Abstract Class Methods",
                        [prop.render(fmt) for prop in abstract_classmethods],
                    ),
                    fmt.section(
                        "Abstract Methods", [prop.render(fmt) for prop in abstract_methods]
                    ),
                    fmt.section("Class Methods", [prop.render(fmt) for prop in classmethods]),
                    fmt.section("Methods", [prop.render(fmt) for prop in methods]),
                    "\t} >",
                ],
            )
        )
        return label

