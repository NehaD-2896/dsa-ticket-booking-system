# service.py

from structures import BookingHistory


class TicketBookingSystem:
    def __init__(self, max_seats=10):
        self.max_seats = max_seats

        # O(1) seat allocation
        self.available_seats = set(range(1, max_seats + 1))
        self.seat_map = {}  # seat_no → name

        self.history = BookingHistory()

        # Stack for cancellations
        self.stack = []

        # Queue for waiting list
        self.queue = []

    # ---------------- BOOK ----------------
    def book_ticket(self, name):
        if not name:
            return "Invalid name"

        if self.available_seats:
            seat = self.available_seats.pop()
            self.seat_map[seat] = name

            self.history.add_record(name, seat, "BOOKED")

            return f"Seat {seat} booked for {name}"

        else:
            self.queue.append(name)
            return f"No seats available. {name} added to waiting list"

    # ---------------- CANCEL ----------------
    def cancel_ticket(self, seat_no):
        if seat_no not in self.seat_map:
            return "Invalid seat or already free"

        name = self.seat_map.pop(seat_no)
        self.available_seats.add(seat_no)

        self.stack.append((name, seat_no))
        self.history.add_record(name, seat_no, "CANCELLED")

        msg = f"Seat {seat_no} cancelled for {name}"

        # Auto-assign to waiting list
        if self.queue:
            next_person = self.queue.pop(0)
            new_seat = self.available_seats.pop()
            self.seat_map[new_seat] = next_person

            self.history.add_record(next_person, new_seat, "BOOKED")

            msg += f"\nSeat {new_seat} assigned to waiting user {next_person}"

        return msg

    # ---------------- UNDO ----------------
    def undo_cancellation(self):
        if not self.stack:
            return "No cancellations to undo"

        name, seat_no = self.stack.pop()

        if self.available_seats:
            self.available_seats.remove(seat_no)
            self.seat_map[seat_no] = name

            self.history.add_record(name, seat_no, "REBOOKED")

            return f"Undo successful: {name} got seat {seat_no}"

        return "Undo failed: seat not available"

    # ---------------- VIEW ----------------
    def show_seats(self):
        result = []
        for i in range(1, self.max_seats + 1):
            if i in self.seat_map:
                result.append(f"{i}: Booked ({self.seat_map[i]})")
            else:
                result.append(f"{i}: Available")
        return result

    def show_waiting(self):
        return self.queue if self.queue else ["Waiting list empty"]

    def show_cancellations(self):
        return self.stack if self.stack else ["No cancellations"]
