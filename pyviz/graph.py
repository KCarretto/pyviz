"""
This module contains graphviz helper functions.
"""
from typing import Callable, Dict, List, Union

from pyviz.base import IRenderable
from pyviz.formatting import format_attr, format_attributes


class Graph:
    _nodes: Dict[str, IRenderable]
    _attrs: Dict[str, str]

    def __init__(self, **kwargs):
        self._attrs = kwargs
        self._nodes = {}

    @property
    def nodes(self) -> Dict[str, IRenderable]:
        """
        Returns:
            Dict[str, IRenderable]: The current mapping of node name to object.
        """
        return self._nodes

    def add_node(self, node: IRenderable) -> None:
        """
        Add a node to the graph.

        Args:
            name (str): Unique name of the node.
            label (str): Text to render inside the node.
            **kwargs: Attributes to be formatted and set for the node.
        """
        self._nodes[node.name] = node

    def add_nodes(self, nodes: List[IRenderable]) -> None:
        """
        Convenience wrapper for add_node.

        Args:
            nodes (List[IRenderable]): The additional nodes to render.
        """
        for node in nodes:
            self.add_node(node)

    def render(self) -> str:
        """
        Returns:
            str: A dot formatted string representing the graph.
        """
        graph_attrs = [format_attr(name, value) for name, value in self._attrs.items()]

        nodes = ["\n\t// Objects"]
        deps = ["\n\t// Dependencies", "edge [style=dashed]\n"]
        impls = ["\n\t// Inheritance", "edge [style=dashed arrowhead=empty]\n"]

        for name, node in self._nodes.items():
            attributes = format_attributes(label=node.dot_label, **node.dot_attributes)
            nodes.append(f"{name} {attributes}\n")

            deps.append("\n".join(f"{name} -> {dep.name};" for dep in node.deps))
            impls.append("\n".join(f"{name} -> {impl.name};" for impl in node.impl))

        graph = "\n\t".join(
            filter(lambda x: x, ["digraph g {"] + graph_attrs + nodes + deps + impls)
        )

        return f"{graph}\n}}"


# def create_graph(label: str, nodes: List[IRenderable]) -> str:
#     """
#     Args:
#         label (str): The title for the graph.
#         nodes (List[IRenderable]): A list of nodes to render.
#     Returns:
#         str: The dot format string for this graph.
#     """
#     graph = pgv.AGraph(strict=False, directed=True)
#     for node in nodes:
#         graph.add_node(node.name.lower(), label=node.dot_label, **node.render_attributes)

#     return graph.string()
