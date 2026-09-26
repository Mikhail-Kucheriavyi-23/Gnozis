import pytest

from core.information_contract import Authorization, AuthorizationStatus, Information
from core.information_gate import admit_information


def info(status):
    return Information(
        information_id="i1",
        source="source",
        content_reference="content",
        provenance_ref="prov",
        authorization=Authorization(
            source="source",
            purpose="task",
            operation="read",
            destination="core",
            status=status,
        ),
    )


def test_gate_admits_allowed_information():
    item = info(AuthorizationStatus.ALLOWED)
    assert admit_information(item) is item


@pytest.mark.parametrize(
    "status",
    [
        AuthorizationStatus.UNKNOWN,
        AuthorizationStatus.DENIED,
        AuthorizationStatus.EXPIRED,
        AuthorizationStatus.REVOKED,
    ],
)
def test_gate_rejects_every_non_allowed_status(status):
    with pytest.raises(PermissionError):
        admit_information(info(status))
