import unittest

from seatmap.availability import Availability
from seatmap.service import BookingService
from seatmap.store import SeatStore


class TestSeatMap(unittest.TestCase):
    def setUp(self):
        self.store = SeatStore()
        self.availability = Availability(self.store)
        self.service = BookingService(self.store, self.availability)

    def test_new_seat_is_available(self):
        self.assertTrue(self.availability.is_available(3))

    def test_capacity_counts_seats(self):
        self.assertEqual(self.availability.available_count(4), 4)

    def test_zero_capacity_has_zero_available_seats(self):
        self.assertEqual(self.availability.available_count(0), 0)


if __name__ == "__main__":
    unittest.main()
