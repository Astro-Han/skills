from .model import LineItem
from .quote import Quote


def preview_row(row):
    item = LineItem(row["name"], float(row["unit_price"]), int(row["quantity"]))
    return Quote([item]).total()
