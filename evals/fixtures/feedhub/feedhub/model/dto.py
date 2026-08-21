"""Transport representation used when items cross the store gateway."""

from dataclasses import dataclass

from .item import Item


@dataclass
class ItemDTO:
    item_id: str
    title: str
    body: str
    published: str
    source: str


def to_dto(item):
    return ItemDTO(item.item_id, item.title, item.body, item.published, item.source)


def from_dto(dto):
    return Item(dto.item_id, dto.title, dto.body, dto.published, dto.source)
