from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from collections import OrderedDict

from pyviz.config import UMLAttributes
from pyviz.fmt import DotFormatter


class UMLBase(ABC):
    """
    Attribute interface that stores a name, type, and description.
    """

    name: str
    type: Optional[str] = None
    description: Optional[str] = None

    def __init__(
        self,
        name: str,
        type: Optional[Union[str, "UMLBase"]] = None,
        description: Optional[str] = None,
        **kwargs,
    ):
        self.name = name
        if isinstance(type, UMLBase):
            self.type = type.type
        else:
            self.type = type
        self.description = description

        for name, attr in kwargs.items():
            setattr(self, name, attr)


class IRenderable(UMLBase):
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

    @abstractmethod
    def render_label(self, fmt: DotFormatter) -> str:
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

    def get_attributes(self, uml_config: UMLAttributes) -> Optional[Dict[str, str]]:
        """
        Override this function to allow for specific attributes to be passed to the render function.

        Args:
            uml_config (UMLAttributes): A NamedTuple representing global uml attribute settings.

        Returns:
            Optional[Dict[str, str]]: An optional mapping of named attributes to use for rendering.
        """
        return None

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


class IRenderComponent(UMLBase):
    """
    Represents a UML attribute that is not rendered on it's own, but as part of another node.
    """

    @abstractmethod
    def render(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: Formatted dot string representing this component.
        """


class SimpleRenderComponent(IRenderComponent):
    """
    An extension of IRenderComponent that provides a default dot_fmt property.
    """

    def render(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: Formatted dot string of this UML component.
        """
        if self.name.startswith("*"):
            return self.name
        return f"{self.name}: {fmt.color_type(self.type)}"


class SimpleRenderable(IRenderable):
    """
    An extension of IRenderable that provides a default dot_label property.
    """

    def render_label(self, fmt: DotFormatter) -> str:
        """
        Returns:
            str: Simple label for this renderable.
        """
        return f"<B>{self.name}</B>: {fmt.color_type(self.type)}"
