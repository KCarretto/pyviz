from typing import Dict, List, Optional, Union

from pyviz.objects import ModuleFunction, Class, Method, Param, Property


class Renderer:
    ##
    # BASIC FORMATTING
    ##

    def fmt_color(self, text: str, color: str) -> str:
        return f'<FONT COLOR="{color}">{text}</FONT>'

    def fmt_type(self, text: str) -> str:
        if not text:
            return self.fmt_color("None", "red")
        return self.fmt_color(text, "mediumseagreen")

    def fmt_attribute(self, name: str, value: str):
        if value.startswith("<"):
            return f"{name}={value}"
        else:
            return f'{name}="{value}"'

    def fmt_attributes(self, attr_map: Dict[str, str] = None, **kwargs) -> Optional[str]:
        if not attr_map:
            attr_map = {}
        attr_map.update(kwargs)

        attrs = [self.fmt_attribute(name, value) for name, value in attr_map.items()]
        if attrs:
            return f"[{' '.join(attrs)}];"

        return None

    def fmt_header(self, title: str) -> str:
        return f"\t\t|<B>{title}</B>\n\t\t\t<BR/><BR/>"

    def fmt_items(self, items: List[str], align: str = "LEFT") -> str:
        return f'\n\t\t\t<BR ALIGN="{align}"/>'.join(items)

    def fmt_section(self, title: str, items: List[str], body_align: str = "LEFT") -> Optional[str]:
        if not items:
            return None
        head = self.fmt_header(title)
        body = self.fmt_items(items)
        return f"{head}{body}"

    ##
    # OBJECT FORMATTING
    ##
    def fmt_abstract(self, label: str) -> str:
        return f"<I>{label}</I>"

    def fmt_async(self, label: str) -> str:
        return f"{self.fmt_color('async', 'magenta3')} {label}"

    def fmt_param(self, param: Param) -> str:
        if param.name.startswith("*"):
            return param.name
        return f"< {param.name}: {self.fmt_type(param.type)} >"

    def fmt_prop(self, prop: Property) -> str:
        if prop.name.startswith("*"):
            return prop.name
        return f"< {prop.name}: {self.fmt_type(prop.type)} >"

    def fmt_method(self, method: Method) -> str:
        params = ", ".join([self.fmt_param(param) for param in method.params])
        label = f"{method.name}({params})"

        if method.is_abstract:
            label = self.fmt_abstract(label)
        if method.is_async:
            label = self.fmt_async(label)

        return f"{label}: {self.fmt_type(method.return_type)}"

    ##
    # RENDERING
    #
    def render_node(self, node: Union[ModuleFunction, Class]) -> str:
        if isinstance(node, ModuleFunction):
            return self.render_module_func(node)
        return self.render_class(node)

    def render_module_func(self, func: ModuleFunction) -> str:
        pass

    def render_method(self, method: Method) -> str:
        label = self.fmt_method(method)
        method_attrs = self.fmt_attributes(label=label, shape="oval")
        return f"{method.name} {method_attrs}"

    def render_class(self, cls: Class) -> str:
        render = []
        label = "\n".join(
            [
                f"< {{<B>{cls.name}</B>",
                self.fmt_section("Properties", [self.fmt_prop(prop) for prop in cls.properties]),
                "\t} >",
            ]
        )
        cls_attrs = self.fmt_attributes(label=label, shape="record")
        render.append(f"{cls.name} {cls_attrs}")

        methods = []
        edges = []
        for method in cls.methods:
            methods.append(self.render_method(method))
            edges.append(f"{method.name} -> {cls.name} [dir=none];")
        render += methods
        render += edges

        return "\n".join(render)

