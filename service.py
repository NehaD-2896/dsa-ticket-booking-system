# service.py
import threading
import time
import uuid
from datetime import date, timedelta
from structures import (
    SeatStatus, Show, Booking, BookingHistory, CATEGORY_ROWS
)

MOVIES = [
    {"id": "m1", "name": "Kalki 2898 AD",  "genre": "Sci-Fi / Action",   "duration": "3h 01m", "rating": 8.3, "lang": "Telugu", "accent": "#1e3a5f"},
    {"id": "m2", "name": "Pushpa 2",        "genre": "Action / Drama",    "duration": "3h 20m", "rating": 8.6, "lang": "Telugu", "accent": "#5f1e1e"},
    {"id": "m3", "name": "Stree 2",         "genre": "Horror / Comedy",   "duration": "2h 15m", "rating": 8.9, "lang": "Hindi",  "accent": "#1e5f3a"},
    {"id": "m4", "name": "Devara",          "genre": "Action / Thriller", "duration": "2h 57m", "rating": 7.1, "lang": "Telugu", "accent": "#3a1e5f"},
    {"id": "m5", "name": "Singham Again",   "genre": "Action / Drama",    "duration": "2h 40m", "rating": 6.8, "lang": "Hindi",  "accent": "#5f4a1e"},
    {"id": "m6", "name": "The Sabarmati Report", "genre": "Drama",        "duration": "2h 05m", "rating": 7.5, "lang": "Hindi",  "accent": "#1e4a5f"},
]

THEATERS = [
    "PVR Cinemas – Forum Mall",
    "INOX – Garuda Mall",
    "Cinepolis – Orion Mall",
]

SHOW_TIMES = ["10:00 AM", "1:30 PM", "4:45 PM", "8:15 PM"]

LOCK_TTL = 600  # 10 minutes


class BookingService:
    def __init__(self):
        self._lock    = threading.Lock()
        self.shows    = {}
        self.bookings = {}
        self.history  = BookingHistory()
        self._init_shows()
        threading.Thread(target=self._cleanup_loop, daemon=True).start()

    # ── Seed shows ──────────────────────────────────────────────────────────
    def _init_shows(self):
        sid = 1
        today = date.today()
        for movie in MOVIES:
            for offset in range(3):          # today + 2 days
                show_date = (today + timedelta(days=offset)).strftime("%d %b")
                for theater in THEATERS:
                    for show_time in SHOW_TIMES:
                        show_id = f"S{sid:04d}"
                        self.shows[show_id] = Show(
                            show_id, movie["id"], movie["name"],
                            theater, show_date, show_time
                        )
                        sid += 1

    # ── Public API ──────────────────────────────────────────────────────────
    def get_movies(self):
        return MOVIES

    def get_shows_for_movie(self, movie_id):
        grouped = {}          # date → theater → [show_info]
        for show in self.shows.values():
            if show.movie_id != movie_id:
                continue
            self._expire_locks(show)
            avail = sum(1 for s in show.seats.values()
                        if s.status == SeatStatus.AVAILABLE)
            grouped.setdefault(show.date, {}).setdefault(show.theater, []).append({
                "id":        show.id,
                "time":      show.time,
                "available": avail,
                "total":     len(show.seats),
            })
        return grouped

    def get_seat_map(self, show_id):
        show = self.shows.get(show_id)
        if not show:
            return None
        with self._lock:
            self._expire_locks(show)
        rows = {}
        for seat in show.seats.values():
            rows.setdefault(seat.row, []).append({
                "id":       seat.id,
                "number":   seat.number,
                "category": seat.category.value,
                "price":    seat.price,
                "status":   seat.status.value,
            })
        for row in rows.values():
            row.sort(key=lambda s: s["number"])
        return {
            "show_id": show_id,
            "movie":   show.movie_name,
            "theater": show.theater,
            "date":    show.date,
            "time":    show.time,
            "rows":    dict(sorted(rows.items())),
        }

    def lock_seats(self, show_id, seat_ids, user_name):
        """Atomically lock requested seats; fail fast if any unavailable."""
        with self._lock:
            show = self.shows.get(show_id)
            if not show:
                return {"success": False, "message": "Show not found"}
            self._expire_locks(show)

            # Validate ALL seats before touching any
            for sid in seat_ids:
                seat = show.seats.get(sid)
                if not seat:
                    return {"success": False, "message": f"Seat {sid} not found"}
                if seat.status != SeatStatus.AVAILABLE:
                    return {"success": False,
                            "message": f"Seat {sid} is no longer available. Please re-select."}

            session_id = str(uuid.uuid4())
            expiry     = time.time() + LOCK_TTL
            total      = 0
            for sid in seat_ids:
                seat             = show.seats[sid]
                seat.status      = SeatStatus.LOCKED
                seat.locked_by   = session_id
                seat.lock_expiry = expiry
                total           += seat.price

            return {
                "success":    True,
                "session_id": session_id,
                "seat_ids":   seat_ids,
                "total":      total,
                "expires_in": LOCK_TTL,
            }

    def confirm_booking(self, show_id, session_id, user_name, seat_ids):
        with self._lock:
            show = self.shows.get(show_id)
            if not show:
                return {"success": False, "message": "Show not found"}

            for sid in seat_ids:
                seat = show.seats.get(sid)
                if (not seat
                        or seat.status != SeatStatus.LOCKED
                        or seat.locked_by != session_id):
                    return {"success": False,
                            "message": "Session expired or seat conflict. Please start over."}

            total   = sum(show.seats[sid].price for sid in seat_ids)
            booking = Booking(user_name, show_id, seat_ids, total)
            for sid in seat_ids:
                seat             = show.seats[sid]
                seat.status      = SeatStatus.BOOKED
                seat.locked_by   = None
                seat.lock_expiry = None
                seat.booked_by   = user_name

            self.bookings[booking.id] = booking
            self.history.add(
                booking.id, user_name, "BOOKED",
                f"{show.movie_name} | {show.date} {show.time} | {', '.join(seat_ids)}"
            )
            return {
                "success":    True,
                "booking_id": booking.id,
                "seats":      seat_ids,
                "total":      total,
                "movie":      show.movie_name,
                "theater":    show.theater,
                "date":       show.date,
                "time":       show.time,
            }

    def cancel_booking(self, booking_id):
        with self._lock:
            booking = self.bookings.get(booking_id)
            if not booking:
                return {"success": False, "message": "Booking not found"}
            if booking.status == "CANCELLED":
                return {"success": False, "message": "Already cancelled"}

            show   = self.shows.get(booking.show_id)
            refund = booking.total_price   # full refund (demo policy)

            if show:
                for sid in booking.seat_ids:
                    seat = show.seats.get(sid)
                    if seat:
                        seat.status    = SeatStatus.AVAILABLE
                        seat.booked_by = None

            booking.status        = "CANCELLED"
            booking.refund_amount = refund
            self.history.add(booking_id, booking.user_name, "CANCELLED",
                             f"Refund ₹{refund}")
            return {"success": True, "booking_id": booking_id, "refund": refund}

    def get_all_bookings(self):
        result = []
        for b in self.bookings.values():
            show = self.shows.get(b.show_id)
            result.append({
                "id":        b.id,
                "user":      b.user_name,
                "movie":     show.movie_name  if show else "—",
                "theater":   show.theater     if show else "—",
                "date":      show.date        if show else "—",
                "time":      show.time        if show else "—",
                "seats":     b.seat_ids,
                "total":     b.total_price,
                "status":    b.status,
                "refund":    b.refund_amount,
                "booked_at": b.booked_at.strftime("%d %b %H:%M"),
            })
        return sorted(result, key=lambda x: x["booked_at"], reverse=True)

    def get_history(self):
        return self.history.get_recent()

    # ── Internals ───────────────────────────────────────────────────────────
    def _expire_locks(self, show):
        now = time.time()
        for seat in show.seats.values():
            if (seat.status == SeatStatus.LOCKED
                    and seat.lock_expiry
                    and seat.lock_expiry < now):
                seat.status      = SeatStatus.AVAILABLE
                seat.locked_by   = None
                seat.lock_expiry = None

    def _cleanup_loop(self):
        while True:
            time.sleep(30)
            with self._lock:
                for show in self.shows.values():
                    self._expire_locks(show)
