from abc import ABCMeta, abstractmethod
from typing import Dict, List, NamedTuple, Optional
from enum import Enum

from pyviz.base import IRenderable, ISimpleRenderable, IRenderComponent, ISimpleRenderComponent
from pyviz.conf import ColorScheme
from pyviz.formatting import format_abstract, format_async, color, type_color, section


class UMLGlobal(ISimpleRenderable):
    """
    Represents a global value.
    """

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: UMLGlobal attributes.
        """
        return {"shape": "triangle", "color": "red"}


class UMLConstant(ISimpleRenderable):
    """
    Represents a global constant that does not change.
    """

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: UMLConstant attributes.
        """
        return {"shape": "triangle", "color": "orange"}


class UMLVar(ISimpleRenderComponent):
    """
    Represents a variable that is either a parameter to a function, or a return value from one.
    """


class UMLProperty(ISimpleRenderComponent):
    """
    Represents an instance read-only attribute of an object type.
    """


class UMLClassProperty(ISimpleRenderComponent):
    """
    Represents an instance read-only attribute of an object type.
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

    @property
    def dot_label(self) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.dot_fmt for param in self.params])
        label = f"{self.name}({params}): {type_color(self.type)}"

        if self.is_awaitable:
            label = format_async(label)

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

    @property
    def dot_label(self) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([param.dot_fmt for param in self.params])
        label = f"{self.name}({params})"

        if self.is_abstract:
            label = format_abstract(label)
        label = f"{label}: {type_color(self.type)}"
        if self.is_awaitable:
            label = format_async(label)

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

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self.properties = []
        self.methods = []
        self.class_methods = []
        super().__init__(*args, **kwargs)

    @property
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: mapping of UMLClass attributes.
        """
        return {"shape": "record"}

    @property
    def dot_label(self) -> str:
        """
        Returns:
            str: A dot format HTML label for this node.
        """
        label = "\n".join(
            filter(
                lambda x: x is not None,
                [
                    f"< {{<B>{self.name}</B>",
                    section("Properties", [prop.dot_fmt for prop in self.properties]),
                    section(
                        "Abstract Methods",
                        [prop.dot_fmt for prop in self.methods if prop.is_abstract],
                    ),
                    section(
                        "Abstract Class Methods",
                        [prop.dot_fmt for prop in self.class_methods if prop.is_abstract],
                    ),
                    section(
                        "Methods", [prop.dot_fmt for prop in self.methods if not prop.is_abstract]
                    ),
                    section(
                        "Class Methods",
                        [prop.dot_fmt for prop in self.class_methods if not prop.is_abstract],
                    ),
                    "\t} >",
                ],
            )
        )
        return label

