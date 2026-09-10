from datetime import datetime, timezone

import pytest

from core import InMemoryStore, Observation, WebObservationSource
from core.persistent_memory import JsonlObservationStore


def _observation(value: object) -> Observation:
    return Observation(
        source="test",
        payload=value,
        observed_at=datetime.now(timezone.utc),
        provenance={"kind": "unit-test"},
    )


def test_in_memory_store_is_append_only_and_typed():
    store = InMemoryStore()
    first = _observation({"n": 1})
    second = _observation({"n": 2})
    store.remember(first)
    store.remember(second)

    assert store.recall(limit=1) == (second,)
    assert store.snapshot() == (first, second)
    with pytest.raises(TypeError):
        store.remember("not-an-observation")


def test_jsonl_memory_survives_reopen(tmp_path):
    path = tmp_path / "observations.jsonl"
    store = JsonlObservationStore(path)
    original = _observation({"nested": [1, 2, 3]})
    store.remember(original)

    reopened = JsonlObservationStore(path)
    restored = reopened.recall(limit=10)

    assert len(restored) == 1
    assert restored[0].source == original.source
    assert restored[0].payload == {"nested": [1, 2, 3]}
    assert restored[0].provenance == {"kind": "unit-test"}


def test_web_adapter_rejects_local_destinations():
    source = WebObservationSource()
    for url in ("http://localhost/", "http://127.0.0.1/", "http://[::1]/"):
        with pytest.raises(ValueError):
            source.fetch(url)


def test_web_adapter_rejects_credentials_and_redirects_at_contract_level():
    source = WebObservationSource()
    with pytest.raises(ValueError):
        source.fetch("https://user:password@example.com/")
