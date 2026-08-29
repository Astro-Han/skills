from .model import LineItem


class Quote:
    def __init__(self, items: list[LineItem]):
        self.items = items

    def total(self):
        return round(sum(item.unit_price * item.quantity for item in self.items), 2)
