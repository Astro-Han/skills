import unittest

from credrotate.model import Credential


class CredentialTests(unittest.TestCase):
    def test_active(self):
        self.assertTrue(Credential("a").active())
        self.assertFalse(Credential("").active())


if __name__ == "__main__":
    unittest.main()
