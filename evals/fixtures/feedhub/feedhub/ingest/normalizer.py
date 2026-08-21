"""Turns raw feed records into domain items."""

from .. import config
from ..model.item import Item


def normalize(record, source):
    return Item(
        item_id=record["id"],
        title=record["title"].strip(),
        body=record.get("body", "").strip(),
        published=_published(record),
        source=source,
    )


def _published(record):
    stamp = record["published"]
    if config.USE_LEGACY_DATES:
        day, month, year = stamp.split("/")
        return "{}-{}-{}T00:00:00".format(year, month, day)
    return stamp
