from research.spt_experiment import SPTExperiment


def test_spt_mvp_clears_episodic_memory_and_records_transfer():
    structure = ["r0"]
    memory = ["episode"]

    def train(_input):
        structure.append("r1")
        memory.append("training-episode")

    experiment = SPTExperiment(
        train=train,
        snapshot_structure=lambda: tuple(structure),
        clear_episodic_memory=lambda: memory.clear(),
        episodic_memory=lambda: tuple(memory),
        evaluate=lambda _input: 1.0 if "r1" in structure else 0.0,
        seed=7,
        training_hash="train-7",
        novel_input_hash="novel-7",
    )

    result = experiment.run({"task": "train"}, {"task": "novel"})

    assert result.structure_before == ("r0",)
    assert result.structure_after == ("r0", "r1")
    assert result.structure_changed is True
    assert result.episodic_memory_after_clear == ()
    assert result.score_before == 0.0
    assert result.score_after == 1.0
    assert result.transfer_delta == 1.0
