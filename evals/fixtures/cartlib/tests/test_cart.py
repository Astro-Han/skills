import unittest

from cartlib.cart import Cart


class TestCart(unittest.TestCase):
    def test_subtotal_sums_items(self):
        cart = Cart()
        cart.add("apple", 2.50, qty=2)
        cart.add("bread", 3.00)
        self.assertEqual(cart.subtotal(), 8.00)

    def test_adding_same_item_accumulates_quantity(self):
        cart = Cart()
        cart.add("apple", 2.50)
        cart.add("apple", 2.50, qty=2)
        self.assertEqual(cart.subtotal(), 7.50)

    def test_remove_existing_item(self):
        cart = Cart()
        cart.add("apple", 2.50)
        cart.remove("apple")
        self.assertEqual(cart.subtotal(), 0.00)

    def test_rejects_non_positive_quantity(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add("apple", 2.50, qty=0)

    def test_total_matches_subtotal(self):
        cart = Cart()
        cart.add("bread", 3.00)
        self.assertEqual(cart.total(), 3.00)


if __name__ == "__main__":
    unittest.main()
