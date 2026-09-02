class Cart:
    def __init__(self):
        self._items = {}

    def add(self, name, unit_price, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if name in self._items:
            price, existing = self._items[name]
            self._items[name] = (price, existing + qty)
        else:
            self._items[name] = (unit_price, qty)

    def remove(self, name):
        del self._items[name]

    def subtotal(self):
        return round(sum(p * q for p, q in self._items.values()), 2)

    def total(self):
        return self.subtotal()
