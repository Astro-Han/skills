import unittest

from stocksync.report import format_drift
from stocksync.store import Store
from stocksync.sync import run_cycle


class TestStore(unittest.TestCase):
    def test_receive_and_quantity(self):
        store = Store()
        store.receive("apples", 10)
        store.receive("apples", 5)
        self.assertEqual(store.quantity("apples"), 15)

    def test_ship_reduces_quantity(self):
        store = Store()
        store.receive("apples", 10)
        store.ship("apples", 4)
        self.assertEqual(store.quantity("apples"), 6)

    def test_ship_rejects_insufficient_stock(self):
        store = Store()
        store.receive("apples", 1)
        with self.assertRaises(ValueError):
            store.ship("apples", 2)

    def test_snapshot_contains_items(self):
        store = Store()
        store.receive("apples", 10)
        self.assertEqual(store.snapshot()["apples"]["qty"], 10)


class TestSync(unittest.TestCase):
    def test_run_cycle_applies_deltas_to_store(self):
        store = Store()
        store.receive("apples", 10)
        run_cycle(store, [("apples", 5)])
        self.assertEqual(store.quantity("apples"), 15)


class TestReport(unittest.TestCase):
    def test_format_drift(self):
        text = format_drift({"apples": 3, "bananas": -2, "pears": 0})
        self.assertEqual(
            text, "drift report\n  apples: +3\n  bananas: -2\n  pears: 0")


if __name__ == "__main__":
    unittest.main()
