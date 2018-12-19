"""
This module contains a sample UML layout used by the test cases.
"""
from pyviz import uml

Country = uml.UMLClass(
    "Country", properties=[uml.UMLProperty("name", "str"), uml.UMLProperty("population", "int")]
)
IPerson = uml.UMLClass(
    "IPerson", properties=[uml.UMLProperty("name", "str"), uml.UMLProperty("age", "int")]
)
Citizen = uml.UMLClass("Citizen", properties=[])
