class Availability:
    def __init__(self, store):
        self._store = store
        self._reserved_cache = set()

    def remember(self, seat_id):
        self._reserved_cache.add(seat_id)

    def forget(self, seat_id):
        self._reserved_cache.discard(seat_id)

    def is_available(self, seat_id):
        return seat_id not in self._reserved_cache

    def available_count(self, capacity):
        return sum(1 for seat_id in range(capacity) if self.is_available(seat_id))
