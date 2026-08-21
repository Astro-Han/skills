import unittest

from feedhub.metrics import collect_render_metrics
from feedhub.model.item import Item
from feedhub.render.digest import render_digest


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
