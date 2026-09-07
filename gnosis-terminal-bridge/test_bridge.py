import unittest

from gnosis_terminal_bridge import GnosisTerminalBridge

class TerminalBridgeIntegrationTests(unittest.TestCase):
def setUp(self):
self.bridge = GnosisTerminalBridge(ttl_seconds=300)
self.context = {"epoch": 1, "generation": 2, "height": 1}

```
def test_initiate_verify_and_replay_rejection(self):
    result = self.bridge.initiate_challenge(self.context)

    self.assertEqual(result["status"], "CHALLENGE_ISSUED")

    challenge = result["challenge"]

    verified = self.bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        self.context["epoch"],
        self.context["generation"],
        self.context["height"],
    )

    self.assertEqual(verified["status"], "VERIFIED")

    replay = self.bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        self.context["epoch"],
        self.context["generation"],
        self.context["height"],
    )

    self.assertEqual(replay["status"], "REJECT")
    self.assertEqual(replay["reason"], "CHALLENGE_ALREADY_USED")

def test_context_mismatch_is_rejected(self):
    result = self.bridge.initiate_challenge(self.context)
    challenge = result["challenge"]

    bad_context = {
        "epoch": 1,
        "generation": 999,
        "height": 1,
    }

    result = self.bridge.verify_challenge(
        challenge["challenge_id"],
        challenge["value"],
        bad_context["epoch"],
        bad_context["generation"],
        bad_context["height"],
    )

    self.assertEqual(result["status"], "REJECT")
    self.assertEqual(result["reason"], "CONTEXT_MISMATCH")
```

if   name   == "  main  ":
unittest.main()
