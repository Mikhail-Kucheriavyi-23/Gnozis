import unittest

from core.engine import Engine
from core.evolution import evolutionary_psi_transition
from core.psi_transition import PsiTransition
from core.state import State
from core.uroboros import Uroboros


class PsiCoreIntegrationTests(unittest.TestCase):
    def test_evolutionary_uroboros_uses_psi_transition(self):
        initial = State(values={"x": "x0", "relations": ()})

        def generate(state):
            return (
                state.evolve(values={"x": "x1", "relations": ("r",)}),
                state.evolve(values={"x": "x2", "relations": ()}),
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

    def test_engine_accepts_canonical_psi_transition_directly(self):
        transition = evolutionary_psi_transition(
            generate=lambda state: (state.evolve(values={"x": "next", "relations": ()}),),
            test=lambda _candidate: True,
        )
        engine = Engine(transition=transition)
        result = engine.step(State(values={"x": "current", "relations": ()}))
        self.assertEqual(result.to_psi().x, "next")


if __name__ == "__main__":
    unittest.main()
