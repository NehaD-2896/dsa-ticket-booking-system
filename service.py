import time
from structures import BookingHistory


class TicketBookingSystem:
    def __init__(self, max_seats=10, lock_time=120):
        self.max_seats = max_seats
        self.lock_time = lock_time  # seconds

        self.available_seats = set(range(1, max_seats + 1))
        self.seat_map = {}          # confirmed bookings
        self.locked_seats = {}      # seat_no → (name, expiry_time)

        self.history = BookingHistory()
        self.stack = []
        self.queue = []

    # ---------------- LOCK SEAT ----------------
    def lock_seat(self, name):
        self._release_expired_locks()

        if not self.available_seats:
            self.queue.append(name)
            return f"No seats available. {name} added to waiting list"

        seat = self.available_seats.pop()
        expiry = time.time() + self.lock_time

        self.locked_seats[seat] = (name, expiry)

        return f"Seat {seat} locked for {name} (expires in {self.lock_time}s)"

    # ---------------- CONFIRM ----------------
    def confirm_booking(self, seat_no):
        self._release_expired_locks()

        if seat_no not in self.locked_seats:
            return "Seat not locked or lock expired"

        name, expiry = self.locked_seats.pop(seat_no)

        self.seat_map[seat_no] = name
        self.history.add_record(name, seat_no, "BOOKED")

        return f"Booking confirmed: {name} got seat {seat_no}"

    # ---------------- AUTO RELEASE ----------------
    def _release_expired_locks(self):
        current_time = time.time()

        expired = [
            seat for seat, (_, expiry) in self.locked_seats.items()
            if expiry < current_time
        ]

        for seat in expired:
            name, _ = self.locked_seats.pop(seat)
            self.available_seats.add(seat)

    # ---------------- CANCEL ----------------
    def cancel_ticket(self, seat_no):
        if seat_no not in self.seat_map:
            return "Invalid seat or not booked"

        name = self.seat_map.pop(seat_no)
        self.available_seats.add(seat_no)

        self.stack.append((name, seat_no))
        self.history.add_record(name, seat_no, "CANCELLED")

        msg = f"Seat {seat_no} cancelled for {name}"

        # assign to waiting list
        if self.queue:
            next_person = self.queue.pop(0)
            new_seat = self.available_seats.pop()
            self.seat_map[new_seat] = next_person
            self.history.add_record(next_person, new_seat, "BOOKED")

            msg += f"\nSeat {new_seat} assigned to {next_person}"

        return msg

    # ---------------- UNDO ----------------
    def undo_cancellation(self):
        if not self.stack:
            return "No cancellations"

        name, seat_no = self.stack.pop()

        if seat_no in self.available_seats:
            self.available_seats.remove(seat_no)
            self.seat_map[seat_no] = name
            self.history.add_record(name, seat_no, "REBOOKED")

            return f"{name} got seat {seat_no} back"

        return "Undo failed"

    # ---------------- DISPLAY ----------------
    def show_seats(self):
        self._release_expired_locks()

        result = []

        for i in range(1, self.max_seats + 1):
            if i in self.seat_map:
                result.append(f"{i}: Booked ({self.seat_map[i]})")
            elif i in self.locked_seats:
                name, expiry = self.locked_seats[i]
                remaining = int(expiry - time.time())
                result.append(f"{i}: Locked by {name} ({remaining}s left)")
            else:
                result.append(f"{i}: Available")

        return result

    def show_waiting(self):
        return self.queue if self.queue else ["Empty"]

    def show_cancellations(self):
        return self.stack if self.stack else ["Empty"]
