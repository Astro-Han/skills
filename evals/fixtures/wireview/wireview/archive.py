from .model import Event


def export_record(event: Event) -> dict[str, object]:
    return event.to_wire()
