from .model import Cart


def add_line(cart: Cart, amount: int) -> None:
    cart.lines.append(amount)
