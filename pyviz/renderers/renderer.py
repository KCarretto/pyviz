"""
Render datamodel using jinja2.
"""
from typing import Any, ClassVar, Dict, List, Type, Optional
from typing_extensions import Protocol
from os.path import join

import jinja2

from pyviz.datamodel import Var, Method, Class


class IRenderer(Protocol):
    """
    Defines a protocol for renderers.
    """

    template_name: ClassVar[str]
    template_dir: ClassVar[str]

    def get_attributes(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: Keyword arguments that will be passed to the template render function.
        """
        raise NotImplementedError("Renderers must implement get_attributes")

    def render(self: "Renderer") -> str:
        """
        Render the given renderer.
        """
        loader = jinja2.PackageLoader(
            package_name="pyviz", package_path=join(f"renderers/templates/", self.template_dir)
        )
        env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
        template = env.get_template(self.template_name)
        return template.render(**self.get_attributes())
