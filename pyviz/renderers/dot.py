"""
Collection of renderers that transform the datamodel into .dot files renderable by graphviz.
"""
from typing import Any, Dict, List, Optional
from dataclasses import asdict

from pyviz.renderers.renderer import IRenderer
from pyviz.datamodel import NodeMeta, Var, Method, Class


class GraphvizRenderer(IRenderer):
    """
    Baseclass for Graphviz renderers.
    """

    @property
    def graph_defaults(self) -> Dict[str, str]:
        return {"labelloc": "top"}


class ClassDotRenderer(GraphvizRenderer):
    """
    Render a Graphviz graph from Classes.
    """

    template_name: str = "class_graph.j2"
    template_dir: str = "graphviz"

    graph_attributes: Dict[str, str]

    def __init__(self, graph_attributes: Optional[Dict[str, str]] = None, **kwargs):
        self.classes = []
        self.graph_attributes = self.graph_defaults
        self.graph_attributes.update(graph_attributes if graph_attributes else {})
        self.graph_attributes.update(kwargs)
        super().__init__()

    def get_attributes(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: A map of template attributes needed to render a graphviz graph.
        """
        if not self.classes:
            self.classes = NodeMeta.get_class_instances()
        return {"graph": self.graph_attributes, "classes": [asdict(obj) for obj in self.classes]}

