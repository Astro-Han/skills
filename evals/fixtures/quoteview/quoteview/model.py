from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    name: str
    unit_price: float
    quantity: int
