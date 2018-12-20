"""
This module contains graphviz helper functions.
"""
from typing import Callable, Dict, List, NamedTuple, Optional, Union

from pyviz.base import IRenderable
from pyviz.config import GraphConfig
from pyviz.fmt import DotFormatter


class Graph:
    _config: GraphConfig
    _fmt: DotFormatter
    _nodes: Dict[str, IRenderable]

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
        graph_attrs = self.fmt.attribute_list(self.config.attributes.graph)
        node_attrs = self.fmt.attributes(self.config.attributes.default_node)
        edge_attrs = self.fmt.attributes(self.config.attributes.default_edge)
        dep_attrs = self.fmt.attributes(self.config.attributes.dependency_edge)
        impl_attrs = self.fmt.attributes(self.config.attributes.inheritance_edge)

        default_node_attr = f"node {node_attrs}" if node_attrs else None
        default_edge_attr = f"edge {edge_attrs}" if edge_attrs else None
        dep_edge_attr = f"edge {dep_attrs}" if dep_attrs else None
        impl_edge_attr = f"edge {impl_attrs}" if impl_attrs else None

        nodes = [default_node_attr, default_edge_attr, "\n\t// Objects"]
        deps = ["\n\t// Dependencies", dep_edge_attr]
        impls = ["\n\t// Inheritance", impl_edge_attr]

        for name, node in self._nodes.items():
            nodes.append(self._render_node(node))

            deps.append("\n".join(f"{name} -> {dep.name};" for dep in node.deps))
            impls.append("\n".join(f"{name} -> {impl.name};" for impl in node.impl))

        graph = "\n\t".join(
            filter(lambda x: x, ["digraph g {"] + graph_attrs + nodes + deps + impls)
        )

        return f"{graph}\n}}"

    def _render_node(self, node: IRenderable) -> str:
        """
        Render the data from a given node using attributes found in our config. Allows for specific
        overrides if the node implements the get_attributes method.

        Args:
            node (IRenderable): The node to be rendered.
        Returns:
            str: The dot formatted string for the node.
        """
        attr_override = node.get_attributes(self.config.uml_attributes)
        if not attr_override:
            attr_override = {}
        attributes = self.fmt.attributes(label=node.render_label(self.fmt), **attr_override)
        return f"{node.name} {attributes}"
