"""Protected memory boundary: immutable kernel, explicit mutable workspace."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class KernelMemory:
    values: tuple[tuple[str, Any], ...] = ()
    def as_mapping(self) -> Mapping[str, Any]:
        return dict(self.values)

@dataclass(frozen=True)
class Workspace:
    values: tuple[tuple[str, Any], ...] = ()
    def set(self, key: str, value: Any) -> "Workspace":
        data = dict(self.values)
        data[key] = value
        return Workspace(tuple(sorted(data.items())))

@dataclass(frozen=True)
class MemoryView:
    kernel: KernelMemory
    workspace: Workspace
    def mutate_workspace(self, key: str, value: Any) -> "MemoryView":
        return MemoryView(self.kernel, self.workspace.set(key, value))
