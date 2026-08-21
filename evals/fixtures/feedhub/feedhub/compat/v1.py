"""Reader for snapshots written by feedhub 1.x.

2.x has no writer for this format. Deployments upgrading from 1.x still carry a
snapshot.v1.json next to their spool directory and expect its contents to survive.
"""

import json

from ..model.item import Item


def read_v1_snapshot(path):
    with open(path) as handle:
        payload = json.load(handle)
    return [
        Item(
            item_id=entry["uid"],
            title=entry["headline"],
            body=entry.get("text", ""),
            published=entry["date"],
            source=entry.get("feed", "unknown"),
        )
        for entry in payload.get("entries", [])
    ]
