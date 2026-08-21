"""The domain representation of a feed item."""

from dataclasses import dataclass


@dataclass
class Item:
    item_id: str
    title: str
    body: str
    published: str
    source: str
