from core import State

from .agency_context import AgencyContext


CORE_AGENCY_KEY = "agency"


def agency_context_to_core_state(context: AgencyContext) -> State:
    """Convert a verified AgencyContext into derived Ψ-Core input.

    Authentication remains a bridge concern: the core receives only a
    credential-free, immutable snapshot of the verified agency context.
    """
    if not context.identity.authenticated:
        raise ValueError("Agency identity is not authenticated")

    return State(
        values={
            CORE_AGENCY_KEY: {
                "identity": {
                    "provider": context.identity.provider,
                    "subject": context.identity.subject,
                    "authenticated": context.identity.authenticated,
                },
                "epoch": context.epoch,
                "generation": context.generation,
                "height": context.height,
                "expires_at": context.expires_at,
            }
        }
    )
