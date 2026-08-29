import unittest

from batchplan.api import preview
from batchplan.importer import preview_row
from batchplan.model import BatchPlan


class BatchPlanTests(unittest.TestCase):
    def test_positive_sizes(self):
        self.assertEqual(preview("4"), 4)
        self.assertEqual(preview_row({"batch_size": "7"}), 7)

    def test_total_items(self):
        self.assertEqual(BatchPlan([2, 3]).total_items(), 5)
        self.assertEqual(BatchPlan().total_items(), 0)


if __name__ == "__main__":
    unittest.main()
