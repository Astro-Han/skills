import unittest

from cartsummary.model import Cart


class CartSummaryTests(unittest.TestCase):
    def test_empty_cart(self):
        cart = Cart()
        self.assertEqual(cart.total(), 0)
        self.assertEqual(cart.item_count(), 0)


if __name__ == "__main__":
    unittest.main()
