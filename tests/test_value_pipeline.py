import pytest

from core.information_contract import Authorization, AuthorizationStatus, Information, ValueClass
from core.value_pipeline import OutputStatus, propose_output


def info(status=AuthorizationStatus.ALLOWED):
    return Information(
        information_id="i1",
        source="source",
        content_reference="content",
        provenance_ref="prov",
        authorization=Authorization(
            source="source",
            purpose="analysis",
            operation="read",
            destination="core",
            status=status,
        ),
    )


def test_authorized_information_can_create_output_proposal():
    proposal = propose_output(
        info(),
        value_class=ValueClass.COMMERCIAL,
        destination="commercial-surface",
    )
    assert proposal.status is OutputStatus.PROPOSED
    assert proposal.value_class is ValueClass.COMMERCIAL
    assert proposal.provenance_ref == "prov"


@pytest.mark.parametrize("status", [
    AuthorizationStatus.UNKNOWN,
    AuthorizationStatus.DENIED,
    AuthorizationStatus.EXPIRED,
    AuthorizationStatus.REVOKED,
])
def test_unauthorized_information_cannot_create_output_proposal(status):
    with pytest.raises(PermissionError):
        propose_output(
            info(status),
            value_class=ValueClass.PUBLIC,
            destination="public-surface",
        )


def test_unknown_value_is_allowed_as_classification_but_remains_proposal():
    proposal = propose_output(
        info(),
        value_class=ValueClass.UNKNOWN,
        destination="unclassified-surface",
    )
    assert proposal.status is OutputStatus.PROPOSED
    assert proposal.value_class is ValueClass.UNKNOWN
