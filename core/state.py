from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .relation import Relation


_MISSING = object()


def _freeze_standard(value: Any) -> Any:
    """Freeze standard mutable containers without imposing semantics on arbitrary objects."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_standard(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_standard(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_standard(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(_freeze_standard(item) for item in value)
    return value


@dataclass(frozen=True)
class State:
    """Immutable computational representation of the current Ψ = (X, R).

    ``values`` is the existing implementation representation associated with X.
    ``relations`` is the implementation representation associated with R. The
    tuple is an immutable container; it does not imply that mathematical R is
    ordered. Arbitrary objects stored inside values or Relation endpoints are
    not recursively frozen and remain outside this structural immutability
    guarantee.
    """

    values: Mapping[str, Any] = field(default_factory=dict)
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.values, Mapping):
            raise TypeError("values must be a mapping.")
        object.__setattr__(self, "values", _freeze_standard(self.values))
        object.__setattr__(self, "relations", tuple(self.relations))

        for relation in self.relations:
            if not isinstance(relation, Relation):
                raise TypeError("relations must contain Relation instances.")

    def evolve(
        self,
        *,
        values: Mapping[str, Any] | object = _MISSING,
        relations: Any = _MISSING,
    ) -> "State":
        """Create a new State, replacing only explicitly supplied components.

        ``relations=()`` explicitly represents R = ∅. ``None`` is not treated
        as omitted or as an empty relation structure. Calling evolve without a
        replacement is intentionally rejected.
        """
        if values is _MISSING and relations is _MISSING:
            raise TypeError("evolve() requires values and/or relations.")

        if values is _MISSING:
            new_values = self.values
        else:
            if not isinstance(values, Mapping):
                raise TypeError("values must be a mapping.")
            new_values = values

        if relations is _MISSING:
            new_relations = self.relations
        else:
            if relations is None:
                raise TypeError("relations must be an iterable of Relation, not None.")
            new_relations = tuple(relations)

        return State(values=new_values, relations=new_relations)
