from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AgencyIdentity:
    provider: str
    subject: str
    authenticated: bool = True


@dataclass(frozen=True)
class AgencyContext:
    identity: AgencyIdentity
    epoch: int
    generation: int
    height: int
    expires_at: int

    def to_dict(self) -> dict:
        return asdict(self)
