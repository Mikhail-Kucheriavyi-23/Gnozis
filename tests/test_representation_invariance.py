from core.state import State


def psi_signature(state):
    return (
        state.values["x"],
        frozenset(tuple(edge) for edge in state.values["relations"]),
    )


def transition(state):
    return state.evolve(values={
        "x": state.values["x"] + len(state.values["relations"]),
        "relations": tuple(sorted(state.values["relations"])),
    })


def test_equivalent_relation_order_has_equivalent_transition():
    a = State(values={"x": 5, "relations": (("a", "b"), ("b", "c"))})
    b = State(values={"x": 5, "relations": (("b", "c"), ("a", "b"))})

    assert psi_signature(a) == psi_signature(b)
    assert psi_signature(transition(a)) == psi_signature(transition(b))


def test_equivalent_node_renaming_preserves_structure_under_canonicalization():
    a = State(values={"x": 5, "relations": (("a", "b"), ("b", "c"))})
    b = State(values={"x": 5, "relations": (("u", "v"), ("v", "w"))})

    def canonical_edges(state):
        edges = state.values["relations"]
        nodes = sorted({n for edge in edges for n in edge})
        mapping = {node: i for i, node in enumerate(nodes)}
        return frozenset((mapping[u], mapping[v]) for u, v in edges)

    assert canonical_edges(a) == canonical_edges(b)


def test_representation_invariance_is_explicitly_required_for_psi_signature():
    a = State(values={"x": 2, "relations": (("a", "b"),)})
    b = State(values={"x": 2, "relations": (("b", "a"),)})

    # This test deliberately documents that directed and undirected
    # semantics must not be conflated. Reversal is NOT equivalent here.
    assert psi_signature(a) != psi_signature(b)
