import pytest

from core.external_execution_request import ExternalExecutionRequest
from core.external_operation import ExternalOperation
from core.information_contract import Authorization, AuthorizationStatus, Information


def info(status):
    return Information(
        information_id="i1",
        source="external",
        content_reference="content",
        provenance_ref="prov",
        authorization=Authorization(
            source="external",
            purpose="test",
            operation="request",
            destination="core",
            status=status,
        ),
    )


def test_execution_request_requires_explicit_authorization():
    request = ExternalExecutionRequest.from_information(
        info(AuthorizationStatus.ALLOWED),
        operation=ExternalOperation.REQUEST,
        content_digest="digest",
        purpose="explicit test execution",
    )
    assert request.information_id == "i1"


@pytest.mark.parametrize("status", [
    AuthorizationStatus.UNKNOWN,
    AuthorizationStatus.DENIED,
    AuthorizationStatus.EXPIRED,
    AuthorizationStatus.REVOKED,
])
def test_execution_request_fails_closed(status):
    with pytest.raises(PermissionError):
        ExternalExecutionRequest.from_information(
            info(status),
            operation=ExternalOperation.REQUEST,
            content_digest="digest",
            purpose="explicit test execution",
        )
