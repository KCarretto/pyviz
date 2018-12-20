from abc import ABCMeta, abstractmethod
from typing import Dict, List, NamedTuple, Optional
from enum import Enum

from pyviz.base import IRenderable, SimpleRenderable, IRenderComponent, SimpleRenderComponent
from pyviz.config import GraphConfig, UMLAttributes
from pyviz.fmt import DotFormatter


class UMLVar(SimpleRenderComponent):
    """
    Represents a variable that is either a parameter to a function, or a return value from one.
    """


class UMLProperty(SimpleRenderComponent):
    """
    Represents an instance read-only attribute of an object type.
    """


class UMLClassProperty(SimpleRenderComponent):
    """
    Represents an instance read-only attribute of an object type.
    """


class UMLGlobal(SimpleRenderable):
    """
    Represents a global value.
    """


class UMLConstant(SimpleRenderable):
    """
    Represents a global constant that does not change.
    """


class UMLModuleFunction(IRenderable):
    """
    Represents a module level function.
    """

    params: List[UMLVar] = []
    is_awaitable: bool = False

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self.params = []
        self.is_awaitable = False
        super().__init__(*args, **kwargs)

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


class UMLMethod(IRenderComponent):
    """
    A function that is to be rendered as a component.
    """

    params: List[UMLVar] = []
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


class UMLClass(IRenderable):
    """
    Represents a class.
    """

    properties: List[UMLProperty]
    methods: List[UMLMethod]

    def __init__(self, *args, **kwargs):

        self.properties = []
        self.methods = []

        super().__init__(*args, **kwargs)

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: mapping of UMLClass attributes.
        """
        return {"shape": "record"}

    def get_attributes(self, uml_config: UMLAttributes) -> Optional[Dict[str, str]]:
        """
        Override to return UMLClass specific attributes.
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

