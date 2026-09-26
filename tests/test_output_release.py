import pytest

from core.destination_authorization import DestinationAuthorization
from core.information_contract import ValueClass
from core.output_release import OutputReleaseGate
from core.value_pipeline import OutputProposal, OutputStatus


def proposal(value_class=ValueClass.PUBLIC, destination="public"):
    return OutputProposal(
        information_id="i1",
        value_class=value_class,
        destination=destination,
        content_reference="content",
        provenance_ref="prov",
    )


def gate():
    return OutputReleaseGate(
        DestinationAuthorization(
            destination="public",
            allowed_value_classes=frozenset({ValueClass.PUBLIC}),
            purpose="public release",
        )
    )


def test_authorized_proposal_can_cross_release_gate():
    released = gate().release(proposal(), release_id="r1")
    assert released.release_id == "r1"


def test_wrong_destination_cannot_cross_release_gate():
    with pytest.raises(PermissionError):
        gate().release(proposal(destination="commercial"), release_id="r1")


def test_wrong_value_class_cannot_cross_release_gate():
    with pytest.raises(PermissionError):
        gate().release(proposal(ValueClass.PERSONAL), release_id="r1")


def test_release_requires_nonempty_release_id():
    with pytest.raises(ValueError):
        gate().release(proposal(), release_id="")
