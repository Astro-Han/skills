from dataclasses import dataclass


@dataclass
class Event:
    kind: str
    value: int

    def to_wire(self) -> dict[str, object]:
        return {"kind": self.kind, "value": self.value}
