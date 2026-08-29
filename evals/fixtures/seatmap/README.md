# seatmap

Internal seat-booking preview. Nothing is persisted or charged.

`SeatStore` is the sole authority for reservation state. `Availability` is a live read projection over that authority; it must not retain a second reservation set. `BookingService` owns command sequencing, not reservation-state synchronization.

- Run tests: `python3 -m unittest discover -s tests -t .`
