import pytest

from core.information_contract import Authorization, AuthorizationStatus, Information
from core.information_gate import admit_information


def make_info(status):
    return Information(
        information_id="integration-1",
        source="external",
        content_reference="content",
        provenance_ref="prov",
        authorization=Authorization(
            source="external",
            purpose="task",
            operation="read",
            destination="core",
            status=status,
        ),
    )


def process(information):
    admitted = admit_information(information)
    return ("processed", admitted.information_id)


def test_authorized_information_reaches_processing_entry():
    assert process(make_info(AuthorizationStatus.ALLOWED)) == (
        "processed",
        "integration-1",
    )


@pytest.mark.parametrize(
    "status",
    [
        AuthorizationStatus.UNKNOWN,
        AuthorizationStatus.DENIED,
        AuthorizationStatus.EXPIRED,
        AuthorizationStatus.REVOKED,
    ],
)
def test_unauthorized_information_cannot_reach_processing_entry(status):
    with pytest.raises(PermissionError):
        process(make_info(status))
