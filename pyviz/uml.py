from abc import ABCMeta, abstractmethod
from typing import Dict, List, NamedTuple, Optional
from enum import Enum

from pyviz.base import IRenderable, SimpleRenderable, IRenderComponent, SimpleRenderComponent
from pyviz.config import GraphConfig
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

    def render_dot(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.dot_fmt for param in self.params])
        label = f"{self.name}({params}): {fmt.color_type(self.type)}"

        if self.is_awaitable:
            label = fmt.awaitable(label)

        return label


class UMLFunction(IRenderComponent):
    """
    A function that is to be rendered as a component.
    """

    params: List[UMLVar] = []
    is_awaitable: bool = False
    is_abstract: bool = False

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self.params = []
        self.is_awaitable = False
        self.is_abstract = False
        super().__init__(*args, **kwargs)

    def render_dot(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.dot_fmt for param in self.params])
        label = f"{self.name}({params})"

        if self.is_abstract:
            label = fmt.abstract(label)
        label = f"{label}: {fmt.color_type(self.type)}"
        if self.is_awaitable:
            label = fmt.awaitable(label)

        return label


class UMLClassMethod(UMLFunction):
    """
    Represents a function bound to an object type.
    """


class UMLMethod(UMLFunction):
    """
    Represents a function bound to an instance of an object.
    """


class UMLClass(IRenderable):
    """
    Represents a class.
    """

    properties: List[UMLProperty]
    methods: List[UMLMethod]
    class_methods: List[UMLClassMethod]

    def __init__(
        self,
        *,
        properties: List[UMLProperty] = None,
        methods: List[UMLMethod] = None,
        class_methods: List[UMLClassMethod] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if not properties:
            properties = []
        if not methods:
            methods = []
        if not class_methods:
            class_methods = []
        self.properties = properties
        self.methods = methods
        self.class_methods = class_methods

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: mapping of UMLClass attributes.
        """
        return {"shape": "record"}

    def render_label(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: A dot format HTML label for this node.
        """
        label = "\n".join(
            filter(
                lambda x: x is not None,
                [
                    f"< {{<B>{self.name}</B>",
                    fmt.section("Properties", [prop.render(fmt) for prop in self.properties]),
                    fmt.section(
                        "Abstract Methods",
                        [prop.render(fmt) for prop in self.methods if prop.is_abstract],
                    ),
                    fmt.section(
                        "Abstract Class Methods",
                        [prop.render(fmt) for prop in self.class_methods if prop.is_abstract],
                    ),
                    fmt.section(
                        "Methods",
                        [prop.render(fmt) for prop in self.methods if not prop.is_abstract],
                    ),
                    fmt.section(
                        "Class Methods",
                        [prop.render(fmt) for prop in self.class_methods if not prop.is_abstract],
                    ),
                    "\t} >",
                ],
            )
        )
        return label

