import unittest

from gnosis_terminal_bridge import GnosisTerminalBridge


class TerminalBridgeIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.bridge = GnosisTerminalBridge(ttl_seconds=300)
        self.context = {"epoch": 1, "generation": 2, "height": 1}

    def test_initiate_verify_and_replay_rejection(self):
        challenge = self.bridge.initiate_challenge(self.context)
        self.assertEqual(challenge["status"], "CHALLENGE")
        self.assertEqual(challenge["context"], self.context)
        self.assertTrue(challenge["challenge"])

        verified = self.bridge.verify_challenge(
            challenge["challenge"], self.context
        )
        self.assertEqual(verified["status"], "VERIFIED")
        self.assertEqual(verified["context"], self.context)
        self.assertEqual(verified["agency"]["authority"], "user_authenticated")

        replay = self.bridge.verify_challenge(
            challenge["challenge"], self.context
        )
        self.assertEqual(replay["status"], "REJECTED")
        self.assertEqual(replay["reason"], "REPLAY_DETECTED")

    def test_context_mismatch_is_rejected(self):
        challenge = self.bridge.initiate_challenge(self.context)
        bad_context = {"epoch": 1, "generation": 2, "height": 2}

        result = self.bridge.verify_challenge(
            challenge["challenge"], bad_context
        )
        self.assertEqual(result["status"], "REJECTED")
        self.assertEqual(result["reason"], "CONTEXT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
