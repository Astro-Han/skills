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

    def test_subtotal_two_items(self):
        cart = Cart()
        cart.add("milk", 1.20)
        cart.add("eggs", 4.80)
        self.assertEqual(cart.subtotal(), 6.00)

    def test_subtotal_three_items(self):
        cart = Cart()
        cart.add("milk", 1.20)
        cart.add("eggs", 4.80)
        cart.add("jam", 2.00)
        self.assertEqual(cart.subtotal(), 8.00)

    def test_total_matches_subtotal_again(self):
        cart = Cart()
        cart.add("milk", 1.20, qty=3)
        self.assertEqual(cart.total(), cart.subtotal())

    def test_items_stored_internally(self):
        cart = Cart()
        cart.add("apple", 2.50, qty=2)
        self.assertEqual(cart._items, {"apple": (2.50, 2)})

    def test_subtotal_matches_computed_sum(self):
        cart = Cart()
        cart.add("apple", 2.50, qty=2)
        cart.add("bread", 3.00)
        expected = round(sum(p * q for p, q in cart._items.values()), 2)
        self.assertEqual(cart.subtotal(), expected)

    def test_subtotal_is_float(self):
        cart = Cart()
        cart.add("apple", 2.50)
        self.assertIsInstance(cart.subtotal(), float)

    def test_add_many_items_nonempty(self):
        cart = Cart()
        for i in range(5):
            cart.add("item-{}".format(i), 1.00)
        self.assertTrue(cart.subtotal() > 0)


if __name__ == "__main__":
    unittest.main()
