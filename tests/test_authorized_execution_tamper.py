import pytest

from core.authorized_execution import AuthorizedExecution
from core.external_execution_request import ExternalExecutionRequest
from core.external_operation import ExternalOperation
from core.execution import CanonicalExecutor
from core.execution_contract import ExecutionInput
from core.information_contract import Authorization, AuthorizationStatus, Information
from core.psi_transition import PsiTransition
from core.state import Psi


def make_info():
    return Information(
        information_id="info-1",
        source="external",
        content_reference="content",
        provenance_ref="prov",
        authorization=Authorization(
            source="external",
            purpose="test",
            operation="request",
            destination="core",
            status=AuthorizationStatus.ALLOWED,
        ),
    )


def make_input(psi, digest="content-digest"):
    from core.execution_contract import execution_input_from_psi
    return execution_input_from_psi(
        psi, input_type="external-information", content_digest=digest
    )


def make_bridge():
    return AuthorizedExecution(
        CanonicalExecutor(
            history=__import__("core.history", fromlist=["AppendOnlyHistory"]).AppendOnlyHistory(),
            kernel_version="test",
        )
    )


def transition():
    return PsiTransition(lambda p: Psi(x=p.x + 1, relations=p.relations))


def test_information_id_tampering_is_rejected_before_transition():
    info = make_info()
    psi = Psi(x=0, relations=())
    execution_input = make_input(psi)
    request = ExternalExecutionRequest(
        information_id="forged-info",
        operation=ExternalOperation.REQUEST,
        content_digest=execution_input.content_digest,
        purpose="test",
    )
    with pytest.raises(ValueError):
        make_bridge().step(info, psi, transition(), execution_input, request)


def test_content_digest_tampering_is_rejected_before_transition():
    info = make_info()
    psi = Psi(x=0, relations=())
    execution_input = make_input(psi, "real-digest")
    request = ExternalExecutionRequest(
        information_id=info.information_id,
        operation=ExternalOperation.REQUEST,
        content_digest="forged-digest",
        purpose="test",
    )
    with pytest.raises(ValueError):
        make_bridge().step(info, psi, transition(), execution_input, request)


def test_missing_request_cannot_reach_canonical_execution():
    info = make_info()
    psi = Psi(x=0, relations=())
    execution_input = make_input(psi)
    with pytest.raises(TypeError):
        make_bridge().step(info, psi, transition(), execution_input, None)
