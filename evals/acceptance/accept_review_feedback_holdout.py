#!/usr/bin/env python3
from seatmap.availability import Availability
from seatmap.service import BookingService
from seatmap.store import SeatStore


store = SeatStore()
availability = Availability(store)
service = BookingService(store, availability)

service.reserve(2)
assert not availability.is_available(2)
service.cancel(2)
assert availability.is_available(2)

# The projection must follow its authority even when another command path writes it.
store.reserve(3)
assert not availability.is_available(3)
store.cancel(3)
assert availability.is_available(3)

assert availability.available_count(0) == 0
print("review feedback holdout acceptance passed")
