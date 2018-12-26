"""
This module contains graphviz helper functions.
"""
from typing import Callable, Dict, List, NamedTuple, Optional, Union

from pyviz.objects import Class, ModuleFunction
from pyviz.render import Renderer


class Graph:
    _renderer: Renderer
    _nodes: Dict[str, Union[Class, ModuleFunction]]

    def __init__(self):
        self._renderer = Renderer()
        self._nodes = {}

    @property
    def nodes(self) -> Dict[str, Union[Class, ModuleFunction]]:
        """
        Returns:
            Dict[str, BaseNode]: The current mapping of node name to object.
        """
        return self._nodes

    def add_node(self, node: Union[Class, ModuleFunction]) -> None:
        """
        Add a node to the graph.

        Args:
            name (str): Unique name of the node.
            label (str): Text to render inside the node.
            **kwargs: Attributes to be formatted and set for the node.
        """
        self._nodes[node.name] = node

    def add_nodes(self, nodes: List[Union[Class, ModuleFunction]]) -> None:
        """
        Convenience wrapper for add_node.
        """
        for node in nodes:
            self.add_node(node)

    def render(self) -> str:
        """
        Returns:
            str: A dot formatted string representing the graph.
        """
        nodes = [self._renderer.render_node(node) for node in self._nodes.values()]

        graph = "\n\t".join(filter(lambda x: x, ["digraph g {"] + nodes))

        return f"{graph}\n}}"

