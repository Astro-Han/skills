import unittest

from pricer.discounts import apply_discounts


class TestApplyDiscounts(unittest.TestCase):
    def test_no_coupons(self):
        self.assertEqual(apply_discounts(100.0, []), 100.0)

    def test_single_percent_coupon(self):
        self.assertEqual(apply_discounts(100.0, [("percent", 10)]), 90.0)

    def test_single_flat_coupon(self):
        self.assertEqual(apply_discounts(100.0, [("flat", 15)]), 85.0)

    def test_total_never_negative(self):
        self.assertEqual(apply_discounts(10.0, [("flat", 25)]), 0.0)

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):
            apply_discounts(100.0, [("bogus", 1)])


if __name__ == "__main__":
    unittest.main()
