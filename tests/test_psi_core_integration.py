import unittest

from core.engine import Engine
from core.evolution import evolutionary_psi_transition
from core.psi_transition import PsiTransition
from core.state import State
from core.uroboros import Uroboros


class PsiCoreIntegrationTests(unittest.TestCase):
    def test_evolutionary_uroboros_uses_proof_gated_psi_transition(self):
        initial = State(values={"x": "x0", "relations": ()})

        def generate(state):
            return (
                state.evolve(values={"x": "x1", "relations": ("r",)}),
                state.evolve(values={"x": "x2", "relations": ()}),
                state.evolve(values={"x": "x3", "relations": ("s", "t")}),
            )

        def test(_candidate):
            return True

        core = Uroboros.evolutionary(
            generate=generate,
            test=test,
            state=initial,
        )

        self.assertIsInstance(core.engine.transition, PsiTransition)
        evolved = core.step()
        self.assertEqual(evolved.state.to_psi().x, "x2")
        self.assertEqual(evolved.state.to_psi().relations, ())

    def test_engine_accepts_canonical_psi_transition_with_proof(self):
        transition = evolutionary_psi_transition(
            generate=lambda state: (
                state.evolve(values={"x": "next-a", "relations": ()}),
                state.evolve(values={"x": "next-b", "relations": ("r",)}),
            ),
            test=lambda _candidate: True,
        )
        engine = Engine(transition=transition)
        result = engine.step(State(values={"x": "current", "relations": ()}))
        self.assertEqual(result.to_psi().x, "next-a")

    def test_proof_gated_transition_rejects_dead_end_pool(self):
        transition = evolutionary_psi_transition(
            generate=lambda state: (
                state.evolve(values={"x": "only", "relations": ()}),
            ),
            test=lambda _candidate: True,
        )
        engine = Engine(transition=transition)
        with self.assertRaises(ValueError, msg="dead-end candidate must not evolve"):
            engine.step(State(values={"x": "current", "relations": ()}))


if __name__ == "__main__":
    unittest.main()
