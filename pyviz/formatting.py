"""
Common utilities.
"""
from typing import List, Optional
from pyviz.conf import ColorScheme


def color(text: str, color: str) -> str:
    """
    Wrap text in a color.

    Args:
        text (str): The text to be wrapped.
        color (str): The font color to set.
    """
    return f'<FONT COLOR="{color}">{text}</FONT>'


def type_color(text: Optional[str]) -> str:
    """
    Color a type with additional logic.

    Args:
        text (str): The text to evaluate and color.

    Returns:
        str: The formatted type string.
    """
    if text:
        return color(text, ColorScheme.TYPE.value)
    return color("None", ColorScheme.NONE_TYPE.value)


def header(title: str) -> str:
    """
    Returns:
        str: A record header.
    """
    return f"\t\t|<B>{title}</B>\n\t\t\t<BR/><BR/>"


def item_list(items: List[str], align: str = "LEFT") -> str:
    """
    Args:
        items (List[str]): A list of items to be separated by line breaks.
    Returns:
        str: A dot string representing the formatted item list.
    """
    return f'\n\t\t\t<BR ALIGN="{align}"/>'.join(items)


def section(title: str, items: List[str], body_align: str = "LEFT") -> Optional[str]:
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
    head = header(title)
    body = item_list(items)
    return f"{head}{body}"


def format_abstract(label: str) -> str:
    """
    Format a function to be abstract.

    Args:
        label (str): Existing string label to wrap.

    Returns:
        str: Abstract formatted version of the label.
    """
    return f"<I>{label}</I>"


def format_async(label: str) -> str:
    """
    Format a function to be asynchronous.

    Args:
        label (str): Existing string label to wrap.

    Returns:
        str: Async formatted version of the label.
    """
    return f"{color('async', color=ColorScheme.ASYNC)} {label}"


def format_attr(name: str, value: str) -> str:
    """
    Args:
        name: The key for the mapping.
        value: The value for the mapping.

    Returns:
        str: A formatted [ attribute=value ] string.
    """
    if value.startswith("<"):
        return f"{name}={value}"
    else:
        return f'{name}="{value}"'


def format_attributes(**kwargs) -> str:
    """
    Args:
        **kwargs: An attribute mapping of names to values.

    Returns:
    """
    attrs = [format_attr(name, value) for name, value in kwargs.items()]
    return f"[{' '.join(attrs)}];"
