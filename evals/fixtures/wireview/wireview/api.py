import json

from .model import Event


def export_json(event: Event) -> str:
    return json.dumps(event.to_wire(), sort_keys=True)
