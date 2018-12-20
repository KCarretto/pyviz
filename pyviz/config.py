"""
Stores configuration NamedTuples for graph generation.
"""
from typing import Dict, NamedTuple, Optional


class GraphColors(NamedTuple):
    """
    This object stores data about the colors to use for display.
    """

    type_map: Dict[str, str] = {"None": "red", "default": "mediumseagreen"}
    ASYNC: str = "magenta3"


class GraphAttributes(NamedTuple):
    """
    This object stores global attributes that can be applied to the graph.
    """

    graph: Optional[Dict[str, str]] = dict(label="PyViz Graph", labelloc="top")
    default_edge: Optional[Dict[str, str]] = {}
    default_node: Optional[Dict[str, str]] = {}
    dependency_edge: Dict[str, str] = dict(style="dashed")
    inheritance_edge: Dict[str, str] = dict(style="dashed", arrowhead="empty")


class UMLAttributes(NamedTuple):
    """
    This object stores um attributes that are specific to a UML type.
    """

    uml_global: Optional[Dict[str, str]] = None
    uml_constant: Optional[Dict[str, str]] = None
    uml_module_function: Optional[Dict[str, str]] = dict(shape="component")
    uml_class: Optional[Dict[str, str]] = dict(shape="record")


class GraphConfig(NamedTuple):
    colors: GraphColors
    attributes: GraphAttributes
    uml_attributes: UMLAttributes

    @classmethod
    def default(cls) -> "GraphConfig":
        """
        Returns:
            GraphConfig: A graph config initialized with default settings.
        """
        colors = GraphColors()
        attributes = GraphAttributes()
        uml_attributes = UMLAttributes()

        return cls(colors=colors, attributes=attributes, uml_attributes=uml_attributes)
