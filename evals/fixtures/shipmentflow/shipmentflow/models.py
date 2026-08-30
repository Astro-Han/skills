from dataclasses import dataclass


@dataclass
class Recipient:
    id: str
    email: str
    display_name: str
    legacy_route: str | None = None
