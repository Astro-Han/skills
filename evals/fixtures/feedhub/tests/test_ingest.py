import os
import unittest

from feedhub import config
from feedhub.app import bootstrap, collect
from feedhub.ingest import fetcher

SPOOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "spool")


class TestIngest(unittest.TestCase):
    def test_discover_skips_non_feed_files(self):
        found = [os.path.basename(p) for p in fetcher.discover(SPOOL)]
        self.assertEqual(found, ["news.feed.json", "tech.feed.json"])

    def test_collect_drops_cross_feed_duplicates(self):
        repository, _, deduper = bootstrap(SPOOL)
        accepted = collect(deduper, SPOOL)
        self.assertEqual([item.item_id for item in accepted], ["n-1", "t-1", "t-2"])
        self.assertEqual(deduper.count(), 3)

    def test_max_items_caps_a_run(self):
        original = config.MAX_ITEMS
        config.MAX_ITEMS = 1
        try:
            repository, _, deduper = bootstrap(SPOOL)
            accepted = collect(deduper, SPOOL)
            self.assertEqual(len(accepted), 1)
        finally:
            config.MAX_ITEMS = original
