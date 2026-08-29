import unittest

from launchmode.api import enable
from launchmode.model import LaunchConfig


class LaunchModeTests(unittest.TestCase):
    def test_enable_updates_mode(self):
        config = LaunchConfig()
        enable(config)
        self.assertEqual(config.mode, "enabled")


if __name__ == "__main__":
    unittest.main()
