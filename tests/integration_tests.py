from typing import Tuple

from pyviz import ClassDotRenderer, Var, Method, Class, Abstract, Async, Cls
from pyviz.types import LIST, DICT


def test_create_graph():
    """
    Ensure field descriptors work properly. Depends on gen_example.
    """

    g = ClassDotRenderer(label="Test")
    g.classes = sample_classes()

    # Citizen.inherits(IPerson)
    # Country.depends_on(Citizen)

    lines = g.render().split("\n")

    def assert_contains(term: str):
        assert any(term in line for line in lines)

    assert lines[0] == "digraph g {"
    assert lines[-1] == "}"

    # assert_contains('label="PyViz Graph"')
    # assert_contains("Country -> Citizen")
    # assert_contains("Citizen -> IPerson")
    # assert_contains("Country [label=< {<B>Country</B>")
    assert_contains("|<B>Properties</B>")


def sample_classes() -> Tuple[Class]:

    v1 = Var("v1", "str")
    v2 = Var("v2", "int")
    v3 = Var("v3", LIST("str"))
    p1 = Var("v1_dct", DICT("str", v1))
    p2 = Var("p2", "bool")

    do_one = Method("do_one", params=[v1, v2])
    do_two = Method("do_two", params=[v1, v2], type=v3)
    do_three = Cls(Method("do_3", params=[v1, v2, v3], type=v1))

    gen_one = Async(Method("gen_one", params=[v1, v2]))

    abc_one = Abstract(do_one)
    abc_two = Abstract(do_two)
    abc_three = Abstract(do_three)

    I = A = Class(
        "I",
        description="Interface I",
        ext_parent="typing_extensions.Protocol",
        properties=[p1],
        methods=[abc_one, abc_two, abc_three],
    )

    A = Class("A", description="Class A", properties=[p1, v3], methods=[abc_one, abc_two, do_three])
    B = Class(
        "B", description="Class B", properties=[p1, v3, p2], methods=[abc_one, do_two, do_three]
    )
    C = Class("C", description="Class C", properties=[v1, v2], methods=[gen_one])

    A.inherits(I)
    B.inherits(A)
    C.depends_on(A)
    B.depends_on(C)

    return (I, A, B, C)


if __name__ == "__main__":
    g = ClassDotRenderer(name="graph_test", label="Test")
    sample_classes()
    print(g.render())
