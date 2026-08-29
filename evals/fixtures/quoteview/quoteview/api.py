from .model import LineItem
from .quote import Quote


def preview(name, unit_price, quantity):
    return Quote([LineItem(name, unit_price, quantity)]).total()
