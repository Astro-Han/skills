from dataclasses import dataclass, field


@dataclass
class BatchPlan:
    items: list[int] = field(default_factory=list)

    def total_items(self) -> int:
        return sum(self.items)
