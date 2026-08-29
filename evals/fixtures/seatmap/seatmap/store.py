class SeatStore:
    def __init__(self):
        self._reserved = set()

    def reserve(self, seat_id):
        self._reserved.add(seat_id)

    def cancel(self, seat_id):
        self._reserved.discard(seat_id)

    def is_reserved(self, seat_id):
        return seat_id in self._reserved
