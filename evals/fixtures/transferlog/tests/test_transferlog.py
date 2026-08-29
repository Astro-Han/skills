import unittest

from transferlog.api import commit
from transferlog.ledger import Ledger


class TransferLogTests(unittest.TestCase):
    def test_positive_commit(self):
        ledger = Ledger()
        commit(ledger, 4)
        self.assertEqual(ledger.count(), 1)

    def test_empty_count(self):
        self.assertEqual(Ledger().count(), 0)


if __name__ == "__main__":
    unittest.main()
