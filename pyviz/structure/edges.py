"""
Define various edge types.
"""
from typing import Dict

from pyviz.structure.base import BaseEdge


class TypeDependency(BaseEdge):
    """
    A dependency that exists because of type annotations.

    Starts at dependent node, goes to dependency node.
    """

    def attributes(self) -> Dict[str, str]:
        """
        TypeDependency attributes
        """
        return {"style": "dotted", "color": "plum1"}


class Inheritance(BaseEdge):
    """
    An edge from child class to parent class.
    """

    def attributes(self) -> Dict[str, str]:
        """
        Inheritance attributes
        """
        return {"style": "dashed", "color": "plum1"}


class CodeFlow(BaseEdge):
    """
    An edge from caller to method.
    """

    def attributes(self) -> Dict[str, str]:
        """
        CodeFlow attributes
        """
        return {"style": "dashed", "color": "red"}
