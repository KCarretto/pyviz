# pyviz
A framework for designing python tools using UML and graphviz.

# Example
```
from pyviz import uml, Graph

Country = uml.UMLClass(
    "Country", properties=[uml.UMLProperty("name", "str"), uml.UMLProperty("population", "int")]
)
IPerson = uml.UMLClass(
    "IPerson", properties=[uml.UMLProperty("name", "str"), uml.UMLProperty("age", "int")]
)
Citizen = uml.UMLClass("Citizen", properties=[])

Citizen.implements(IPerson)
Country.depends_on(Citizen)

g = Graph(label="Test Graph")
g.add_nodes([Country, IPerson, Citizen])

print(g.render())
```

The above code will produce .dot formatted output to create a graph that models the code.