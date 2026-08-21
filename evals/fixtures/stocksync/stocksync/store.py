class Store:
    def __init__(self):
        self._items = {}

    def receive(self, name, qty):
        item = self._items.setdefault(name, {"qty": 0})
        item["qty"] += qty

    def ship(self, name, qty):
        item = self._items.get(name)
        if item is None or item["qty"] < qty:
            raise ValueError("insufficient stock for " + name)
        item["qty"] -= qty

    def quantity(self, name):
        return self._items.get(name, {"qty": 0})["qty"]

    def snapshot(self):
        return self._items
