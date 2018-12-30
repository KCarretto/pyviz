"""
Collection of renderers that transform the datamodel into .dot files renderable by graphviz.
"""
from typing import Any, Dict, List, Optional, ClassVar
from dataclasses import asdict

from pyviz.renderers.renderer import IRenderer
from pyviz.datamodel import ComponentMeta, Var, Method, Class, ModuleMethod, Decorator


class GraphvizRenderer(IRenderer):
    """
    Baseclass for Graphviz renderers.
    """

    @property
    def graph_defaults(self) -> Dict[str, str]:
        return {"labelloc": "top"}


class CodeDotRenderer(GraphvizRenderer):
    """
    Render a Graphviz graph representing python code structure from the datamodel.
    """

    template_name: ClassVar[str] = "code_graph.j2"
    template_dir: ClassVar[str] = "graphviz"

    graph_attributes: Dict[str, str]
    classes: List[Class]
    module_methods: List[ModuleMethod]
    decorators: List[Decorator]

    def __init__(self, graph_attributes: Optional[Dict[str, str]] = None, **kwargs):
        self.classes = []
        self.module_methods = []
        self.decorators = []
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
            self.classes = ComponentMeta.get_class_instances()
        if not self.module_methods:
            self.module_methods = ComponentMeta.get_module_method_instances()
        if not self.decorators:
            self.decorators = ComponentMeta.get_decorator_instances()

        attrs = {
            "graph": self.graph_attributes,
            "classes": [],
            "module_methods": [],
            "decorators": [],
            "subpackages": {},  # Map of subpackage name to node name, regardless of node type
        }

        # Build Classes
        for node in self.classes:
            attrs["classes"].append(asdict(node))
            if node.subpackage:
                if not attrs["subpackages"].get(node.subpackage):
                    attrs["subpackages"][node.subpackage] = []
                attrs["subpackages"][node.subpackage].append(node.name)

        # Build Module Methods
        for node in self.module_methods:
            attrs["module_methods"].append(asdict(node))
            if node.subpackage:
                if not attrs["subpackages"].get(node.subpackage):
                    attrs["subpackages"][node.subpackage] = []
                attrs["subpackages"][node.subpackage].append(node.name)

        # Build Decorators
        for node in self.decorators:
            attrs["decorators"].append(asdict(node))
            if node.subpackage:
                if not attrs["subpackages"].get(node.subpackage):
                    attrs["subpackages"][node.subpackage] = []
                attrs["subpackages"][node.subpackage].append(node.name)

        return attrs
