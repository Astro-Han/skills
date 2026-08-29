import unittest

from quoteview.api import preview
from quoteview.importer import preview_row
from quoteview.model import LineItem
from quoteview.quote import Quote


class TestQuoteView(unittest.TestCase):
    def test_api_preview(self):
        self.assertEqual(preview("widget", 2.5, 4), 10.0)

    def test_csv_preview(self):
        row = {"name": "widget", "unit_price": "2.50", "quantity": "4"}
        self.assertEqual(preview_row(row), 10.0)

    def test_empty_quote_is_zero(self):
        self.assertEqual(Quote([]).total(), 0)

    def test_line_item_fields(self):
        item = LineItem("widget", 2.5, 4)
        self.assertEqual((item.name, item.unit_price, item.quantity), ("widget", 2.5, 4))


if __name__ == "__main__":
    unittest.main()
