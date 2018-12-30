"""
Define intermediary data structures that store state for objects.
"""
from dataclasses import dataclass, field
from typing import ClassVar, List, Optional, Type, TypeVar, Union

COMPONENT = Union["Class", "ModuleMethod", "Decorator"]


def _coerce_type(value: Optional[Union[str, "Var", "Method", "BaseComponent"]]) -> str:
    """
    Args:
        value (Optional[Union[str, Var, Method, BaseComponent]]): The value to coerce.
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


def _coerce_name(value: Union[str, "Var", "Method", COMPONENT]) -> str:
    """
    Args:
        value (Union[str, Var, Method, COMPONENT]): The value to coerce.
    Returns:
        str: The coerced name of the value
    """
    if hasattr(value, "name"):
        return value.name
    return str(value)


class ComponentMeta(type):
    """Tracks instantiation of nodes"""

    _class_registry: ClassVar[List["Class"]] = []
    _decorator_registry: ClassVar[List["Decorator"]] = []
    _module_method_registry: ClassVar[List["ModuleMethod"]] = []

    def __call__(cls: Type[COMPONENT], *args, **kwargs):
        """Hooks class instantiation."""
        instance = super().__call__(*args, **kwargs)
        if isinstance(instance, Class):
            ComponentMeta._class_registry.append(instance)
        elif isinstance(instance, Decorator):
            ComponentMeta._decorator_registry.append(instance)
        elif isinstance(instance, ModuleMethod):
            ComponentMeta._module_method_registry.append(instance)
        return instance

    @classmethod
    def get_class_instances(cls) -> List["Class"]:
        """Returns all instances of Class"""
        return ComponentMeta._class_registry

    @classmethod
    def get_decorator_instances(cls) -> List["Decorator"]:
        """Returns all instances of Class"""
        return ComponentMeta._decorator_registry

    @classmethod
    def get_module_method_instances(cls) -> List["ModuleMethod"]:
        """Returns all instances of Class"""
        return ComponentMeta._module_method_registry


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
class Decorator(metaclass=ComponentMeta):
    """
    Attributes:
        name(str): The name of the decorator function.
        type(str): The type to be decorated, i.e. Callable or Class.
        params(List[Var]): A list of parameters needed for the decorator.
        description (Optional[str]): An optional description of the decorator.
        module (Optional[str]): Optionally customize the module name for the decorator.
        subpackage (Optional[str]): Optionally specify a subpackage the decorator should
            be located in.
    """

    name: str
    type: str
    params: List[Var] = field(default_factory=list)
    description: Optional[str] = None
    module: Optional[str] = None
    subpackage: Optional[str] = None

    def __post_init__(self):
        """
        Attempt to coerce types.
        """
        self.name: str = _coerce_name(self.name)
        self.type: str = _coerce_type(self.type)


@dataclass
class ModuleMethod(metaclass=ComponentMeta):
    name: str
    type: str = field(default="None")
    params: Optional[List[Var]] = field(default_factory=list)
    description: Optional[str] = None
    module: Optional[str] = None
    subpackage: Optional[str] = None
    is_async: bool = field(default=False, init=False)

    def __post_init__(self):
        """
        Attempt to coerce types.
        """
        self.name: str = _coerce_name(self.name)
        self.type: str = _coerce_type(self.type)


@dataclass
class Class(metaclass=ComponentMeta):
    """
    Attributes:
        name (str): The name of the class.
        properties (List[Var]): A list of public properties on the class.
        methods (List[Method]): A list of public methods on the class.
        description (Optional[str]): An optional description of the class.
        module (Optional[str]): Optionally customize the module name for the class.
            Allows for classes to be stored in the same module.
        subpackage (Optional[str]): Optionally specify a subpackage the Class should be located in.
        metaclass (Optional[Class]): Optionally specify a metaclass.
        ext_parent (Optional[str]): Specify a parent class from an external module. Absolute import.
        parents (List[Class]): Specify a list of parent classes.
        deps (List[Class]): A list of classes this class depends on.
    """

    name: str
    properties: List[Var] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    description: Optional[str] = None
    module: Optional[str] = None
    subpackage: Optional[str] = None
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
