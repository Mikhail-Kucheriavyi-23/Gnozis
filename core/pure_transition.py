"""Compatibility aliases for the canonical Psi transition boundary.

The implementation lives in ``core.psi_transition``. Keeping aliases here
prevents two competing definitions of the fundamental operator.
"""

from .psi_transition import Psi, PsiFunction, PsiTransition, make_psi_transition

PureTransition = PsiFunction

__all__ = ["Psi", "PsiFunction", "PsiTransition", "PureTransition", "make_psi_transition"]
