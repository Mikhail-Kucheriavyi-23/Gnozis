import pytest
from core.history import TransitionRecord
from core.provenance import Provenance, attach_provenance

def rec():
    return TransitionRecord(0, "", "s0", "k1", "c0", True, "e0")

def test_complete_provenance_attaches_without_mutation():
    record = rec()
    out = attach_provenance(record, Provenance("c0", "e0", "k1", ("source-1",)))
    assert out == record

def test_provenance_mismatch_is_rejected():
    with pytest.raises(ValueError, match="evidence"):
        attach_provenance(rec(), Provenance("c0", "wrong", "k1"))

def test_incomplete_provenance_is_rejected():
    with pytest.raises(ValueError, match="incomplete"):
        attach_provenance(rec(), Provenance("c0", "", "k1"))
