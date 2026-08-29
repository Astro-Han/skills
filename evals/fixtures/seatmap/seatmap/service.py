class BookingService:
    def __init__(self, store, availability):
        self._store = store
        self._availability = availability

    def reserve(self, seat_id):
        self._store.reserve(seat_id)

    def cancel(self, seat_id):
        self._store.cancel(seat_id)
