from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, TypeVar
from collections import OrderedDict

import re

# TODO: Node registry
# TODO: Finish implementing code flow


class BaseNode(ABC):
    """
    Attribute interface that stores a name, type, and description.
    """

    name: str
    type: Optional[str] = None
    description: Optional[str] = None

    def __init__(
        self,
        name: str,
        type: Optional[Union[str, "BaseNode"]] = None,
        description: Optional[str] = None,
        **kwargs,
    ):
        self.name = name
        if isinstance(type, BaseNode):
            self.type = type.type
        else:
            self.type = type
        self.description = description

        for name, attr in kwargs.items():
            setattr(self, name, attr)


T = TypeVar("SelfCallableNode", bound="CallableNode")
TCallableNode = TypeVar("TCallableNode", bound="CallableNode")


class CallableNode(BaseNode):
    """
    Represents a node that is callable and can call other callables.
    """

    _code_flow: List[TCallableNode]

    def calls(self: T, node: TCallableNode) -> T:
        """
        Args:
            node(TCallableNode): Track that this node calls the given node.
        Returns:
            T: self
        """
        self._code_flow.append(node)


class BaseEdge:
    """
    Represents an edge between two nodes.
    """

    # TODO: Types
    def __init__(self, start, end):
        """
        Store the edge.
        """
        self.start = start
        self.end = end


_first_cap_re = re.compile("(.)([A-Z][a-z]+)")
_all_cap_re = re.compile("([a-z0-9])([A-Z])")


def to_underscore(name: str) -> str:
    """
    Converts a camelCase string to underscore_format.
    """
    s1 = _first_cap_re.sub(r"\1_\2", name)
    return _all_cap_re.sub(r"\1_\2", s1).lower()
