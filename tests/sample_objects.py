"""
This module contains a sample UML layout used by the test cases.
"""
from pyviz.uml import Class, Method, Property, Param, Abstract

Country = Class("Country", properties=[Property("name", "str"), Property("population", "int")])
IPerson = Class(
    "IPerson",
    properties=[Property("name", "str"), Property("age", "int")],
    methods=[Abstract(Method("celebrate", params=[Param("amount", "int")]))],
)
Citizen = Class(
    "Citizen",
    properties=[Property("happiness", "int")],
    methods=[Method("celebrate", params=[Param("amount", "int")])],
)

