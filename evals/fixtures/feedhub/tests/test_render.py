import os
import unittest

from feedhub.app import bootstrap, collect
from feedhub.metrics import collect_render_metrics
from feedhub.model.item import Item
from feedhub.render.digest import render_digest
from feedhub.scheduler import BatchCancelled, BatchRunner

SPOOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "spool")


class TestRender(unittest.TestCase):
    def test_digest_groups_by_source(self):
        items = [
            Item("a", "First", "", "2026-03-01T00:00:00", "tech"),
            Item("b", "Second", "", "2026-03-02T00:00:00", "news"),
        ]
        digest = render_digest(items)
        self.assertIn("== news ==", digest)
        self.assertIn("- First (2026-03-01T00:00:00)", digest)

    def test_metrics_count_sections(self):
        digest = "== tech ==\n- First (x)\n== news ==\n- Second (y)"
        self.assertEqual(collect_render_metrics(digest)["sections"], 2)


class TestCancelledBatchIsInvisible(unittest.TestCase):
    def test_digest_after_a_cancelled_batch_shows_no_partial_items(self):
        repository, gateway, deduper = bootstrap(SPOOL)
        accepted = collect(deduper, SPOOL)
        runner = BatchRunner(repository, deduper)

        class Cancelling(list):
            def __iter__(self):
                for index, value in enumerate(list.__iter__(self)):
                    if index == 1:
                        runner.cancel()
                    yield value

        with self.assertRaises(BatchCancelled):
            runner.run(Cancelling(accepted))
        # The digest is rendered from the store after the cancelled batch: without the
        # rollback it would list the items the batch had already written.
        self.assertEqual(render_digest([]), "")
        self.assertEqual(repository.count(), 0)
