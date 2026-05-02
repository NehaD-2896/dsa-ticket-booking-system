import time
from structures import BookingHistory


class TicketBookingSystem:
    def __init__(self, max_seats=10, lock_time=120):
        self.max_seats = max_seats
        self.lock_time = lock_time

        self.available_seats = set(range(1, max_seats + 1))
        self.seat_map = {}
        self.locked_seats = {}

        self.history = BookingHistory()
        self.stack = []
        self.queue = []

    def lock_seat(self, name):
        self._release_expired_locks()

        if not name:
            return "Invalid name"

        if not self.available_seats:
            self.queue.append(name)
            return f"No seats available. {name} added to waiting list"

        seat = self.available_seats.pop()
        expiry = time.time() + self.lock_time

        self.locked_seats[seat] = (name, expiry)

        return f"Seat {seat} locked for {name}"

    def confirm_booking(self, seat_no, name):
        self._release_expired_locks()

        if seat_no not in self.locked_seats:
            return "Seat not locked or expired"

        locked_name, _ = self.locked_seats[seat_no]

        if locked_name != name:
            return "This seat is locked by another user"

        self.locked_seats.pop(seat_no)
        self.seat_map[seat_no] = name
        self.history.add_record(name, seat_no, "BOOKED")

        return f"{name} successfully booked seat {seat_no}"

    def _release_expired_locks(self):
        current_time = time.time()

        expired = [
            seat for seat, (_, expiry) in self.locked_seats.items()
            if expiry < current_time
        ]

        for seat in expired:
            self.locked_seats.pop(seat)
            self.available_seats.add(seat)

    def cancel_ticket(self, seat_no):
        if seat_no not in self.seat_map:
            return "Invalid seat"

        name = self.seat_map.pop(seat_no)
        self.available_seats.add(seat_no)

        self.stack.append((name, seat_no))
        self.history.add_record(name, seat_no, "CANCELLED")

        if self.queue:
            next_user = self.queue.pop(0)
            new_seat = self.available_seats.pop()
            self.seat_map[new_seat] = next_user
            self.history.add_record(next_user, new_seat, "BOOKED")

            return f"{name} cancelled. Seat given to {next_user}"

        return f"{name} cancelled seat {seat_no}"

    def undo_cancellation(self):
        if not self.stack:
            return "No cancellations"

        name, seat_no = self.stack.pop()

        if seat_no in self.available_seats:
            self.available_seats.remove(seat_no)
            self.seat_map[seat_no] = name
            self.history.add_record(name, seat_no, "REBOOKED")

            return f"{name} restored to seat {seat_no}"

        return "Undo failed"

    def show_seats(self):
        self._release_expired_locks()

        result = []

        for i in range(1, self.max_seats + 1):
            if i in self.seat_map:
                result.append(f"{i}: Booked ({self.seat_map[i]})")
            elif i in self.locked_seats:
                name, expiry = self.locked_seats[i]
                remaining = int(expiry - time.time())
                result.append(f"{i}: Locked ({remaining}s)")
            else:
                result.append(f"{i}: Available")

        return result

    def show_waiting(self):
        return self.queue if self.queue else ["Empty"]

    def show_cancellations(self):
        return self.stack if self.stack else ["Empty"]
