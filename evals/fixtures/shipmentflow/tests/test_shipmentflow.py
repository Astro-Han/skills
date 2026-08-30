import unittest

from shipmentflow.compat import export_recipient
from shipmentflow.identity import create_recipient


class ShipmentFlowTests(unittest.TestCase):
    def test_recipient_fields_are_exported(self):
        recipient = create_recipient("r1", "a@example.com", "Alice")
        self.assertEqual(export_recipient(recipient)["email"], "a@example.com")

    def test_surrounding_whitespace_is_removed(self):
        recipient = create_recipient("r1", " a@example.com ", " Alice ")
        self.assertEqual(recipient.email, "a@example.com")
        self.assertEqual(recipient.display_name, "alice")


if __name__ == "__main__":
    unittest.main()
