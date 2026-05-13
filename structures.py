# structures.py
import uuid
from enum import Enum
from datetime import datetime


class SeatStatus(Enum):
    AVAILABLE = "available"
    LOCKED    = "locked"
    BOOKED    = "booked"


class SeatCategory(Enum):
    NORMAL    = "NORMAL"
    PREMIUM   = "PREMIUM"
    RECLINER  = "RECLINER"


SEAT_PRICES = {
    SeatCategory.NORMAL:   150,
    SeatCategory.PREMIUM:  250,
    SeatCategory.RECLINER: 400,
}

CATEGORY_ROWS = {
    "A": SeatCategory.RECLINER,
    "B": SeatCategory.RECLINER,
    "C": SeatCategory.PREMIUM,
    "D": SeatCategory.PREMIUM,
    "E": SeatCategory.NORMAL,
    "F": SeatCategory.NORMAL,
    "G": SeatCategory.NORMAL,
}


class Seat:
    def __init__(self, row, number, category):
        self.id          = f"{row}{number}"
        self.row         = row
        self.number      = number
        self.category    = category
        self.price       = SEAT_PRICES[category]
        self.status      = SeatStatus.AVAILABLE
        self.locked_by   = None   # session_id
        self.lock_expiry = None   # unix timestamp
        self.booked_by   = None


class Show:
    def __init__(self, show_id, movie_id, movie_name, theater, date, show_time):
        self.id         = show_id
        self.movie_id   = movie_id
        self.movie_name = movie_name
        self.theater    = theater
        self.date       = date
        self.time       = show_time
        self.seats      = self._create_seats()

    def _create_seats(self):
        seats = {}
        for row, cat in CATEGORY_ROWS.items():
            for num in range(1, 11):
                s = Seat(row, num, cat)
                seats[s.id] = s
        return seats


class Booking:
    def __init__(self, user_name, show_id, seat_ids, total_price):
        self.id          = str(uuid.uuid4())[:8].upper()
        self.user_name   = user_name
        self.show_id     = show_id
        self.seat_ids    = seat_ids
        self.total_price = total_price
        self.status      = "CONFIRMED"
        self.booked_at   = datetime.now()
        self.cancelled_at= None
        self.refund_amount = 0


# ── Linked-list history ──────────────────────────────────────────────────────
class HistoryNode:
    def __init__(self, booking_id, user, action, detail):
        self.booking_id = booking_id
        self.user       = user
        self.action     = action
        self.detail     = detail
        self.timestamp  = datetime.now()
        self.next       = None


class BookingHistory:
    def __init__(self):
        self.head = None

    def add(self, booking_id, user, action, detail=""):
        node      = HistoryNode(booking_id, user, action, detail)
        node.next = self.head
        self.head = node

    def get_recent(self, limit=100):
        result, node = [], self.head
        while node and len(result) < limit:
            result.append({
                "booking_id": node.booking_id,
                "user":       node.user,
                "action":     node.action,
                "detail":     node.detail,
                "time":       node.timestamp.strftime("%d %b %H:%M"),
            })
            node = node.next
        return result
