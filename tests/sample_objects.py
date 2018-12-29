"""
This module contains a sample UML layout used by the test cases.
"""
from pyviz import Var, Method, Class, Abstract

Country = Class("Country", properties=[Var("name", "str"), Var("population", "int")])
IPerson = Class(
    "IPerson",
    description="An interface for people, by people.",
    properties=[Var("name", "str"), Var("age", "int")],
    methods=[Abstract(Method("celebrate", params=[Var("amount", "int"), Var("time", "int")]))],
)
Citizen = Class(
    "Citizen",
    properties=[Var("happiness", "int")],
    methods=[
        Method("celebrate", params=[Var("amount", "int"), Var("time", "int")]),
        Method("pay_taxes", params=[Var("income", "int"), Var("state", "str")], type="int"),
    ],
)
Citizen.inherits(IPerson)
