import unittest

from profilefmt.display import label
from profilefmt.model import Profile


class TestProfileFormat(unittest.TestCase):
    def test_initial_region_label(self):
        self.assertEqual(label(Profile("us")), "US")

    def test_blank_region_label_is_blank(self):
        self.assertEqual(label(Profile("")), "")


if __name__ == "__main__":
    unittest.main()
