from dataclasses import dataclass


@dataclass
class Delivery:
    id: str
    destination: str
    label: str
    legacy_route: str | None = None
