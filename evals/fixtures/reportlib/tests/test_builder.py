import unittest

from reportlib.builder import ReportBuilder
from reportlib.render import render_text


class TestReportBuilder(unittest.TestCase):
    def test_build_contains_added_sections(self):
        report = ReportBuilder("Q1").add_section("sales", [1, 2]).build()
        self.assertEqual(report["title"], "Q1")
        self.assertEqual(report["sections"], [("sales", [1, 2])])

    def test_render_lists_sections_with_row_counts(self):
        report = {"title": "Q2", "sections": [("sales", [1, 2, 3])]}
        self.assertEqual(render_text(report), "# Q2\n## sales (3 rows)")


if __name__ == "__main__":
    unittest.main()
