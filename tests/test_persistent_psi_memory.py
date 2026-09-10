from core import Psi, Relation
from core.persistent_psi_memory import JsonlPsiMemory


def test_psi_memory_survives_restart(tmp_path):
    path = tmp_path / "psi.jsonl"
    memory = JsonlPsiMemory(path)
    original = Psi(
        {"x": [1, 2]},
        (Relation("a", "b", "supports"),),
    )

    memory.save(original)
    restored = JsonlPsiMemory(path).load_latest()

    assert restored == original


def test_corrupt_trailing_record_does_not_destroy_last_valid_state(tmp_path):
    path = tmp_path / "psi.jsonl"
    memory = JsonlPsiMemory(path)
    original = Psi({"x": 1}, ())
    memory.save(original)
    with path.open("a", encoding="utf-8") as handle:
        handle.write('{"x":')

    restored = JsonlPsiMemory(path).load_latest()
    assert restored == original


def test_empty_memory_returns_none(tmp_path):
    assert JsonlPsiMemory(tmp_path / "missing.jsonl").load_latest() is None
