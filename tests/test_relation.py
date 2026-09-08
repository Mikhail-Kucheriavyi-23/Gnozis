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


def test_relation_does_not_alias_mutable_container_entities():
    source = {"id": [1]}
    target = {"id": [2]}
    relation = Relation(source, target, "related")

    source["id"].append(3)
    target["id"].append(4)

    assert tuple(relation.source["id"]) == (1,)
    assert tuple(relation.target["id"]) == (2,)


def test_relation_nested_entities_are_immutable():
    relation = Relation({"id": [1]}, {"id": {2}}, "related")

    try:
        relation.source["id"].append(3)
    except AttributeError:
        pass
    else:
        raise AssertionError("Relation source list must be immutable")

    try:
        relation.target["id"].add(3)
    except AttributeError:
        pass
    else:
        raise AssertionError("Relation target set must be immutable")
