"""
Define intermediary data structures that store state for objects.
"""
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Type, TypeVar, Union


def _coerce_type(value: Optional[Union[str, "Var", "Method", "Class"]]) -> str:
    """
    Args:
        value (Optional[Union[str, Var, Method, Class]]): The value to coerce.
    Returns:
        str: The coerced type of the value
    """
    if not value:
        return "None"
    if hasattr(value, "type"):
        return value.type
    if hasattr(value, "name"):
        return value.name
    return str(value)


def _coerce_name(value: Union[str, "Var", "Method", "Class"]) -> str:
    """
    Args:
        value (Union[str, Var, Method, Class]): The value to coerce.
    Returns:
        str: The coerced name of the value
    """
    if hasattr(value, "name"):
        return value.name
    return str(value)


class NodeMeta(type):
    """Tracks instantiation of nodes"""

    _class_registry: ClassVar[List["Class"]] = []

    def __call__(cls: Type["Class"], *args, **kwargs):
        """Hooks class instantiation."""
        instance = super().__call__(*args, **kwargs)
        NodeMeta._class_registry.append(instance)
        return instance

    @classmethod
    def get_class_instances(cls) -> List["Class"]:
        """Returns all instances of Class"""
        return NodeMeta._class_registry


@dataclass
class Var:
    name: str
    type: str

    description: Optional[str] = None

    def __post_init__(self):
        """
        Attempt to coerce types.
        """
        self.name: str = _coerce_name(self.name)
        self.type: str = _coerce_type(self.type)


@dataclass
class Method:
    name: str
    type: str = field(default=None)
    params: Optional[List[Var]] = field(default_factory=list)
    description: Optional[str] = None

    is_async: bool = field(default=False, init=False)
    is_cls: bool = field(default=False, init=False)
    is_abstract: bool = field(default=False, init=False)

    def __post_init__(self):
        """
        Attempt to coerce types.
        """
        self.name: str = _coerce_name(self.name)
        self.type: str = _coerce_type(self.type)


@dataclass
class Class(metaclass=NodeMeta):
    """
    Attributes:
        name (str): The name of the class.
        properties (List[Var]): A list of public properties on the class.
        methods (List[Method]): A list of public methods on the class.
        description (Optional[str]): An optional description of the class.
        metaclass (Optional[Class]): Optionally specify a metaclass.
        ext_parent (Optional[str]): Specify a parent class from an external module. Absolute import.
        parents (List[Class]): Specify a list of parent classes.
        deps (List[Class]): A list of classes this class depends on.
    """

    name: str
    properties: List[Var] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    description: Optional[str] = None
    metaclass: Optional["Class"] = None
    ext_parent: Optional[str] = None
    parents: List["Class"] = field(init=False, default_factory=list)
    deps: List["Class"] = field(init=False, default_factory=list)

    def inherits(self, parent: "Class") -> None:
        """
        Args:
            parent (Class): Mark this class as inheriting from the parent class.
        """
        self.parents += [parent]

    def depends_on(self, dependency: "Class") -> None:
        """
        Args:
            dependency (Class): Mark this class as dependent on the provided dependency.
        """
        self.deps += [dependency]
