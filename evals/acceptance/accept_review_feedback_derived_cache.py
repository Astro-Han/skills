from dataclasses import fields

from cartsummary.api import add_line
from cartsummary.importer import replace_lines
from cartsummary.model import Cart


assert [field.name for field in fields(Cart)] == ["lines"]
cart = Cart()
add_line(cart, 4)
add_line(cart, 7)
assert cart.total() == 11
replace_lines(cart, [3, 8, 9])
assert cart.total() == 20
assert Cart().item_count() == 0
