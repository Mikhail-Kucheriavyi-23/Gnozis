import pytest

from core.destination_authorization import DestinationAuthorization
from core.information_contract import ValueClass
from core.value_pipeline import OutputProposal


def proposal(value_class, destination="surface"):
    return OutputProposal(
        information_id="i1",
        value_class=value_class,
        destination=destination,
        content_reference="content",
        provenance_ref="prov",
    )


def test_destination_authorization_allows_matching_value_class_and_destination():
    auth = DestinationAuthorization(
        destination="surface",
        allowed_value_classes=frozenset({ValueClass.PUBLIC}),
        purpose="public release",
    )
    auth.require_allowed(proposal(ValueClass.PUBLIC))


def test_destination_authorization_rejects_wrong_value_class():
    auth = DestinationAuthorization(
        destination="surface",
        allowed_value_classes=frozenset({ValueClass.PUBLIC}),
        purpose="public release",
    )
    with pytest.raises(PermissionError):
        auth.require_allowed(proposal(ValueClass.PERSONAL))


def test_destination_authorization_rejects_wrong_destination():
    auth = DestinationAuthorization(
        destination="surface",
        allowed_value_classes=frozenset({ValueClass.PUBLIC}),
        purpose="public release",
    )
    with pytest.raises(PermissionError):
        auth.require_allowed(proposal(ValueClass.PUBLIC, destination="other"))
