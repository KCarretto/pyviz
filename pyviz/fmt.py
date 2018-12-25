"""
Common formatting utilities.
"""
from typing import Dict, List, Optional
import re

from pyviz.config import GraphConfig
from pyviz.structure.base import BaseNode
from pyviz.structure.objects import Class, ModuleFunction, Method


class DotFormatter:
    """
    Contains functionality for formatting strings into dot syntax.
    """

    config: GraphConfig

    def __init__(self, config: GraphConfig):
        """
        Initializes the formatter with a graph config storing attributes, colors, etc.

        Args:
            config (GraphConfig): Current graph configuration settings used for formatting.
        """
        self.config = config

    def color(self, text: str, color: str) -> str:
        """
        Wrap text in a color.

        Args:
            text (str): The text to be wrapped.
            color (str): The font color to set.
        """
        return f'<FONT COLOR="{color}">{text}</FONT>'

    def header(self, title: str) -> str:
        """
        Returns:
            str: A record header.
        """
        return f"\t\t|<B>{title}</B>\n\t\t\t<BR/><BR/>"

    def item_list(self, items: List[str], align: str = "LEFT") -> str:
        """
        Args:
            items (List[str]): A list of items to be separated by line breaks.
        Returns:
            str: A dot string representing the formatted item list.
        """
        return f'\n\t\t\t<BR ALIGN="{align}"/>'.join(items)

    def section(self, title: str, items: List[str], body_align: str = "LEFT") -> Optional[str]:
        """
        Args:
            title (str): The title for the section header.
            items (List[str]): A list of items to place in the section body.
            body_align (str): The direction to align the body items. Default: LEFT.

        Returns:
            List[str]: A list of formatted strings representing the section. None when items is empty.
        """
        if not items:
            return None
        head = self.header(title)
        body = self.item_list(items)
        return f"{head}{body}"

    def abstract(self, label: str) -> str:
        """
        Format a function to be abstract.

        Args:
            label (str): Existing string label to wrap.

        Returns:
            str: Abstract formatted version of the label.
        """
        return f"<I>{label}</I>"

    def awaitable(self, label: str) -> str:
        """
        Format a function to be asynchronous.

        Args:
            label (str): Existing string label to wrap.

        Returns:
            str: Async formatted version of the label.
        """
        async_color = self.config.colors.ASYNC
        return f"{self.color('async', color=async_color)} {label}"

    def attribute(self, name: str, value: str) -> str:
        """
        Args:
            name: The key for the mapping.
            value: The value for the mapping.

        Returns:
            str: A formatted attribute=value string.
        """
        if value.startswith("<"):
            return f"{name}={value}"
        else:
            return f'{name}="{value}"'

    def attributes(self, attr_map: Dict[str, str] = None, **kwargs) -> Optional[str]:
        """
        Args:
            attr_map(Dict[str, str]): An attribute mapping of names to values.
            **kwargs: An attribute mapping of names to values.

        Returns:
            Optional[str]: An attribute formatted [name=value] string or None if no attributes.
        """
        if not attr_map:
            attr_map = {}
        attr_map.update(kwargs)

        attrs = [self.attribute(name, value) for name, value in attr_map.items()]
        if attrs:
            return f"[{' '.join(attrs)}];"

        return None

    def attribute_list(self, attr_map: Dict[str, str]) -> List[str]:
        """
        A quick convenience wrapper for fmt.attribute.

        Args:
            attr_map(Dict[str, str]): An attribute mapping of names to values.

        Returns:
            List[str]: An attribute formatted [name=value] string list.
        """
        attrs = [self.attribute(key, value) for key, value in attr_map.items()]
        return attrs

    def color_type(self, type: Optional[str]) -> str:
        """
            Args:
                type (str): The type to render.

            Returns:
                str: A dot formatted string representing the rendered type.
            """
        colors = self.config.colors.type_map

        if not type:
            return self.color("None", colors.get("None"))
        c = colors.get(type, colors["default"])
        return self.color(type, c)

    def _render_node(self, node: BaseNode, **kwargs) -> str:
        """
        Args:
            node (BaseNode): The node to render.
            **kwargs: Attribute overrides for the node.
        Returns:
           str: The rendered node.
        """
        rendered = []
        if isinstance(node, Class):
            rendered.append(self._render_class_label(node))

            if self.config.code_flow:
                for m in node.class_methods + node.methods:
                    label = f"{self._render_node_label(m)}"
                    attributes = self.attributes(dict(label=label))
                    rendered.append(f"{node.name}_{m.name} {attributes}")
        else:
            label = self._render_node_label(node)
            kwargs["label"] = label
            attributes = self.attributes(kwargs)
            rendered.append(f"{node.name} {attributes}")
        return "\n".join(rendered)

    def _render_node_label(self, node: BaseNode) -> str:
        """
        Args:
            node (BaseNode): The node to render.

        Returns:
            str: The HTML or string representation of the nodes display label.
        """
        if isinstance(node, ModuleFunction):
            return self._render_function_label(node)
        else:
            return self._render_default_label(node)

    def _render_default_label(self, node: BaseNode) -> str:
        """
        Returns:
            str: name: Type
        """
        if node.name.startswith("*"):
            return node.name
        return f"< {node.name}: {self.color_type(node.type)} >"

    def _render_function_label(self, node: ModuleFunction) -> str:
        """
        Renders a module level function.
        """
        params = ", ".join([self._render_node_label(param) for param in node.params])
        if node.is_awaitable:
            return f"{self.awaitable(node.name)}({params}): {self.color_type(node.type)}"
        return f"< {node.name}({params}): {self.color_type(node.type)} >"

    def _render_method_label(self, node: Method) -> str:
        """
        Returns:
            str: A dot formatted function signature label.
        """
        params = ", ".join([self._render_node_label(param) for param in node.params])
        label = f"{node.name}({params})"

        if node.is_abstract:
            label = node.abstract(label)
        label = f"{label}: {self.color_type(node.type)}"
        if node.is_awaitable:
            label = self.awaitable(label)

        return f"< {label} >"

    def _render_class_label(self, node: Class) -> str:
        """
        Special render function for classes to support CodeFlow.
        """
        sections = [
            f"< {{<B>{node.name}</B>",
            self.section("Properties", [self._render_node_label(prop) for prop in node.properties]),
            self.section(
                "Abstract Class Methods",
                [self._render_node_label(prop) for prop in node.abstract_class_methods],
            ),
            self.section(
                "Abstract Methods",
                [self._render_node_label(prop) for prop in node.abstract_methods],
            ),
            self.section(
                "Class Methods", [self._render_node_label(prop) for prop in node.class_methods]
            )
            if not self.config.code_flow
            else None,
            self.section("Methods", [self._render_node_label(prop) for prop in node.methods])
            if not self.config.code_flow
            else None,
            "\t} >",
        ]
        return "\n".join(filter(lambda x: x is not None, sections))

