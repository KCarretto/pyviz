"""
This module contains graphviz helper functions.
"""
from typing import Callable, Dict, List, NamedTuple, Optional, Union

from pyviz.structure.base import BaseNode
from pyviz.structure.objects import Class, ModuleFunction

from pyviz.config import GraphConfig
from pyviz.fmt import DotFormatter


class Graph:
    _config: GraphConfig
    _fmt: DotFormatter
    _nodes: Dict[str, BaseNode]

    def __init__(self, config: GraphConfig):
        self._config = config
        self._fmt = DotFormatter(self._config)
        self._nodes = {}

    @property
    def config(self) -> GraphConfig:
        """
        Returns:
            GraphConfig: The config used by this instance.
        """
        return self._config

    @property
    def fmt(self) -> DotFormatter:
        """
        Returns:
            DotFormatter: An instance of a dot formatter configured for this graph.
        """
        return self._fmt

    @property
    def nodes(self) -> Dict[str, BaseNode]:
        """
        Returns:
            Dict[str, BaseNode]: The current mapping of node name to object.
        """
        return self._nodes

    def add_node(self, node: BaseNode) -> None:
        """
        Add a node to the graph.

        Args:
            name (str): Unique name of the node.
            label (str): Text to render inside the node.
            **kwargs: Attributes to be formatted and set for the node.
        """
        self._nodes[node.name] = node

    def add_nodes(self, nodes: List[BaseNode]) -> None:
        """
        Convenience wrapper for add_node.

        Args:
            nodes (List[BaseNode]): The additional nodes to render.
        """
        for node in nodes:
            self.add_node(node)

    def render(self) -> str:
        """
        Returns:
            str: A dot formatted string representing the graph.
        """
        graph_attrs = self.fmt.attribute_list(self.config.attributes.graph)
        node_attrs = self.fmt.attributes(self.config.attributes.default_node)
        edge_attrs = self.fmt.attributes(self.config.attributes.default_edge)
        #       dep_attrs = self.fmt.attributes(self.config.attributes.dependency_edge)
        #       impl_attrs = self.fmt.attributes(self.config.attributes.inheritance_edge)

        default_node_attr = f"node {node_attrs}" if node_attrs else None
        default_edge_attr = f"edge {edge_attrs}" if edge_attrs else None
        #        dep_edge_attr = f"edge {dep_attrs}" if dep_attrs else None
        #        impl_edge_attr = f"edge {impl_attrs}" if impl_attrs else None

        attribute_header = graph_attrs + [default_node_attr, default_edge_attr]

        nodes = [self.fmt._render_node(node) for node in self._nodes.values()]

        # deps.append("\n".join(f"{name} -> {dep.name};" for dep in node.deps))
        # impls.append("\n".join(f"{name} -> {impl.name};" for impl in node.impl))

        graph = "\n\t".join(
            # filter(lambda x: x, ["digraph g {"] + graph_attrs + nodes + deps + impls)
            filter(lambda x: x, ["digraph g {"] + attribute_header + nodes)
        )

        return f"{graph}\n}}"

