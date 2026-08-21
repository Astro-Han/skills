import unittest

from feedhub.model.item import Item
from feedhub.ingest.dedupe import Deduper
from feedhub.scheduler import BatchCancelled, BatchRunner
from feedhub.store.repository import Repository


def item(item_id):
    return Item(item_id, "t" + item_id, "", "2026-03-01T00:00:00", "tech")


class TestRepository(unittest.TestCase):
    def test_reads_are_independent_objects(self):
        repository = Repository("memory")
        repository.add(item("a"))
        first = repository.get("a")
        first.title = "mutated"
        self.assertEqual(repository.get("a").title, "ta")


class TestBatchRunner(unittest.TestCase):
    def test_cancelled_batch_leaves_nothing_behind(self):
        repository = Repository("memory")
        runner = BatchRunner(repository, Deduper())

        class Cancelling(list):
            def __iter__(self):
                for index, value in enumerate(list.__iter__(self)):
                    if index == 2:
                        runner.cancel()
                    yield value

        with self.assertRaises(BatchCancelled):
            runner.run(Cancelling([item("a"), item("b"), item("c")]))
        self.assertEqual(repository.count(), 0)
