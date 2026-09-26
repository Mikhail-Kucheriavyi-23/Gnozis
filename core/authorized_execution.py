"""External-information execution bridge.

Authorization is checked before the existing canonical executor is reached.
The canonical state-transition authority remains unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass

from .execution import CanonicalExecutor, ExecutionResult
from .execution_contract import ExecutionInput
from .information_contract import Information
from .psi_transition import PsiTransition
from .state import Psi


@dataclass(frozen=True)
class AuthorizedExecution:
    executor: CanonicalExecutor

    def step(
        self,
        information: Information,
        psi: Psi,
        transition: PsiTransition,
        execution_input: ExecutionInput,
        *,
        test=None,
    ) -> ExecutionResult:
        """Authorize external information before canonical execution."""
        if not isinstance(information, Information):
            raise TypeError("information must be Information.")

        information.require_authorized()

        return self.executor.step(
            psi,
            transition,
            execution_input,
            test=test,
        )
