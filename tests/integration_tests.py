from pyviz import Graph, GraphConfig
from tests.sample_objects import Country, IPerson, Citizen


def test_create_graph():
    """
    Ensure field descriptors work properly. Depends on gen_example.
    """

    config = GraphConfig.default()

    g = Graph(config)
    g.add_nodes([Country, IPerson, Citizen])

    Citizen.implements(IPerson)
    Country.depends_on(Citizen)

    lines = g.render().split("\n")

    def assert_contains(term: str):
        assert any(term in line for line in lines)

    assert lines[0] == "digraph g {"
    assert lines[-1] == "}"

    assert_contains('label="PyViz Graph"')
    assert_contains("Country -> Citizen")
    assert_contains("Citizen -> IPerson")
    assert_contains("Country [label=< {<B>Country</B>")
    assert_contains("|<B>Properties</B>")


if __name__ == "__main__":
    config = GraphConfig.default()

    g = Graph(config)
    g.add_nodes([Country, IPerson, Citizen])

    Citizen.implements(IPerson)
    Country.depends_on(Citizen)

    print(g.render())
