from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, NamedTuple
from collections import OrderedDict

from pyviz.formatting import type_color


class IAttr:
    """
    Attribute interface that stores a name, type, and description.
    """

    name: str
    type: Optional[str] = None
    description: Optional[str] = None

    def __init__(
        self, name: str, type: Optional[str] = None, description: Optional[str] = None, **kwargs
    ):
        """
        Initialize the class
        """
        self.name = name
        self.type = type
        self.description = description

        for name, value in kwargs.items():
            if name in self.__dict__ and getattr(self, name):
                raise Exception(
                    f"Attempted to set a value for {name}, but it already exists on this object."
                )
            setattr(self, name, value)


class IRenderable(IAttr):
    """
    Represents a UML attribute that can be rendered as it's own node.
    """

    _deps: List["IRenderable"]
    _impl: List["IRenderable"]

    def __init__(self, *args, **kwargs):
        """
        Initialize defaults for this class.
        """
        self._deps = []
        self._impl = []
        super().__init__(*args, **kwargs)

    @property
    @abstractmethod
    def dot_attributes(self) -> Dict[str, str]:
        """
        Returns:
            Dict[str, str]: A mapping of attributes to set while rendering this node.
        """

    @property
    @abstractmethod
    def dot_label(self) -> str:
        """
        Returns:
            str: The dot syntax HTML label for this object.
        """

    @property
    def deps(self) -> List["IRenderable"]:
        """
        Returns:
            List[IRenderable]: List of nodes that this node depends on.
        """
        return self._deps

    @property
    def impl(self) -> List["IRenderable"]:
        """
        Returns:
            List[IRenderable]: List of interface nodes that this node implements.
        """
        return self._impl

    def depends_on(self, node: "IRenderable") -> None:
        """
        Register a dependency for this node.

        Args:
            node (IRenderable): A node that this node depends on.
        """
        self._deps.append(node)

    def implements(self, node: "IRenderable") -> None:
        """
        Describe an interface that this node implements.

        Args:
            node (IRenderable): A node that this node depends on.
        """
        self._impl.append(node)


class IRenderComponent(IAttr):
    """
    Represents a UML attribute that is not rendered on it's own, but as part of another node.
    """

    @property
    @abstractmethod
    def dot_fmt(self) -> str:
        """
        Returns:
            str: Formatted dot string representing this component.
        """


class ISimpleRenderComponent(IRenderComponent):
    """
    An extension of IRenderComponent that provides a default dot_fmt property.
    """

    @property
    def dot_fmt(self) -> str:
        """
        Returns:
            str: Formatted dot string of this UML component.
        """
        return f"{self.name}: {type_color(self.type)}"


class ISimpleRenderable(IRenderable):
    """
    An extension of IRenderable that provides a default dot_label property.
    """

    @property
    def dot_label(self) -> str:
        """
        Returns:
            str: Simple label for this renderable.
        """
        return f"<B>{self.name}</B>: {type_color(self.type)}"
