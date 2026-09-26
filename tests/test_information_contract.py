import pytest

from core.information_contract import (
    Authorization,
    AuthorizationStatus,
    Information,
    ValueClass,
)


def make_info(status: AuthorizationStatus) -> Information:
    return Information(
        information_id="i1",
        source="test-source",
        content_reference="content-1",
        provenance_ref="prov-1",
        authorization=Authorization(
            source="test-source",
            purpose="test",
            operation="read",
            destination="core",
            status=status,
        ),
        value_class=ValueClass.UNKNOWN,
        payload={"x": 1},
    )


def test_allowed_information_passes_authorization():
    make_info(AuthorizationStatus.ALLOWED).require_authorized()


@pytest.mark.parametrize(
    "status",
    [
        AuthorizationStatus.UNKNOWN,
        AuthorizationStatus.DENIED,
        AuthorizationStatus.EXPIRED,
        AuthorizationStatus.REVOKED,
    ],
)
def test_non_allowed_information_fails_closed(status):
    with pytest.raises(PermissionError):
        make_info(status).require_authorized()


def test_unknown_value_is_not_permission():
    info = make_info(AuthorizationStatus.ALLOWED)
    assert info.value_class is ValueClass.UNKNOWN
    info.require_authorized()
