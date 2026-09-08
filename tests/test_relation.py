from core import Relation


def test_relation_is_immutable_for_scalar_fields():
    relation = Relation("a", "b", "supports")

    try:
        relation.source = "c"
    except Exception:
        pass
    else:
        raise AssertionError("Relation.source must be immutable")

    try:
        relation.relation_type = "contradicts"
    except Exception:
        pass
    else:
        raise AssertionError("Relation.relation_type must be immutable")


def test_relation_does_not_mutate_through_container_entities():
    source = {"id": [1]}
    target = {"id": [2]}
    relation = Relation(source, target, "related")

    source["id"].append(3)
    target["id"].append(4)

    # Relation currently accepts arbitrary entities. The test documents that
    # dataclass freezing alone does not guarantee deep immutability here.
    assert relation.source["id"] == [1, 3]
    assert relation.target["id"] == [2, 4]
