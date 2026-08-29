from .model import Cart


def replace_lines(cart: Cart, amounts: list[int]) -> None:
    cart.lines = list(amounts)
