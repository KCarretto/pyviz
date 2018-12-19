"""
Stores constant configuration options.
"""
from typing import ClassVar
from enum import Enum


class ColorScheme(Enum):
    TYPE: ClassVar[str] = "mediumseagreen"
    NONE_TYPE: ClassVar[str] = "red"
    ASYNC: ClassVar[str] = "magenta3"
