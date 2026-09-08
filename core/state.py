from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .relation import Relation


_MISSING = object()


class _FrozenDict(dict):
    """JSON-compatible dict that rejects public mutation operations."""

    def _immutable(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("immutable mapping")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    pop = _immutable
    popitem = _immutable
    setdefault = _immutable
    update = _immutable
    __ior__ = _immutable


class _FrozenList(list):
    """JSON-compatible list that rejects public mutation operations."""

    def _immutable(self, *args: Any, **kwargs: Any) -> None:
        raise TypeError("immutable sequence")

    __setitem__ = _immutable
    __delitem__ = _immutable
    __iadd__ = _immutable
    __imul__ = _immutable
    append = _immutable
    clear = _immutable
    extend = _immutable
    insert = _immutable
    pop = _immutable
    remove = _immutable
    reverse = _immutable
    sort = _immutable


def _freeze_standard(value: Any, active: set[int] | None = None) -> Any:
    """Freeze standard containers without imposing semantics on arbitrary objects."""
    if active is None:
        active = set()

    if isinstance(value, (Mapping, list, tuple, set, frozenset)):
        value_id = id(value)
        if value_id in active:
            raise ValueError("cyclic standard container is not supported")
        active.add(value_id)
        try:
            if isinstance(value, Mapping):
                return _FrozenDict(
                    {
                        key: _freeze_standard(item, active)
                        for key, item in value.items()
                    }
                )
            if isinstance(value, list):
                return _FrozenList(
                    _freeze_standard(item, active) for item in value
                )
            if isinstance(value, tuple):
                return tuple(_freeze_standard(item, active) for item in value)
            return frozenset(_freeze_standard(item, active) for item in value)
        finally:
            active.remove(value_id)

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

    Standard containers nested inside ``values`` are normalized to protected
    immutable-style representations. Mappings and lists retain JSON-compatible
    behavior; sets become frozensets and therefore are not JSON-serializable by
    the standard library. Cyclic standard containers are rejected. Other
    arbitrary objects are left unchanged.
    """

    values: Mapping[str, Any] = field(default_factory=dict)
    relations: tuple[Relation, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.values, Mapping):
            raise TypeError("values must be a mapping.")
        object.__setattr__(self, "values", _freeze_standard(self.values))

        try:
            normalized_relations = tuple(self.relations)
        except TypeError as exc:
            raise TypeError("relations must be iterable.") from exc

        for relation in normalized_relations:
            if not isinstance(relation, Relation):
                raise TypeError("relations must contain Relation instances.")

        object.__setattr__(self, "relations", normalized_relations)

    def evolve(
        self,
        *,
        values: Mapping[str, Any] | object = _MISSING,
        relations: Iterable[Relation] | object = _MISSING,
    ) -> "State":
        """Create a new State, replacing only explicitly supplied components.

        ``relations=()`` explicitly represents R = ∅. ``None`` is not treated
        as omitted or as an empty relation structure. Calling evolve without a
        replacement is intentionally rejected.
        """
        if values is _MISSING and relations is _MISSING:
            raise TypeError("evolve() requires values and/or relations.")

        new_values = self.values if values is _MISSING else values
        if not isinstance(new_values, Mapping):
            raise TypeError("values must be a mapping.")

        if relations is _MISSING:
            new_relations = self.relations
        else:
            if relations is None:
                raise TypeError("relations must be an iterable of Relation, not None.")
            new_relations = relations

        return State(values=new_values, relations=new_relations)
