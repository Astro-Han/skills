from dataclasses import dataclass, field


@dataclass
class Cart:
    lines: list[int] = field(default_factory=list)
    cached_total: int = 0

    def total(self) -> int:
        return self.cached_total

    def item_count(self) -> int:
        return len(self.lines)
