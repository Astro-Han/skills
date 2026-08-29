import unittest

from handlekit.api import register
from handlekit.handles import canonicalize
from handlekit.importer import import_row


class TestHandleKit(unittest.TestCase):
    def test_canonicalize_trims_whitespace(self):
        self.assertEqual(canonicalize("  Ada  "), "Ada")

    def test_api_uses_canonicalization(self):
        self.assertEqual(register("  Ada  "), "Ada")

    def test_importer_uses_canonicalization(self):
        self.assertEqual(import_row({"handle": "  Ada  "}), "Ada")

    def test_empty_handle_is_empty(self):
        self.assertEqual(canonicalize(""), "")


if __name__ == "__main__":
    unittest.main()
