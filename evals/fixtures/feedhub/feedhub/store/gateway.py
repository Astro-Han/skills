"""Access layer between the application and the repository."""

from ..model.dto import from_dto, to_dto


class StoreGateway:
    def __init__(self, repository):
        self._repository = repository

    def save(self, dto):
        self._repository.add(from_dto(dto))

    def load(self, item_id):
        item = self._repository.get(item_id)
        return to_dto(item) if item else None

    def load_all(self):
        return [to_dto(item) for item in self._repository.all_items()]

    def size(self):
        return self._repository.count()
