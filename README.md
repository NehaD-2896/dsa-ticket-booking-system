
# CineBook — Movie Ticket Booking System

A full-stack web application that replicates core BookMyShow functionality — browse movies, pick showtimes, select seats, and book tickets with real-time concurrent seat locking.

Live Demo: (https://dsa-ticket-booking-system.onrender.com)

---

## Features

- Browse 6 movies across 3 theaters and 3 dates
- Visual seat map with Recliner / Premium / Normal categories
- **Concurrent seat locking** — seats held for 10 minutes during checkout
- **Thread-safe booking** — simultaneous users can't double-book the same seat
- Booking confirmation with unique ID
- Cancel bookings with full refund
- Activity log using a custom linked list history structure
- Auto-expiry of abandoned locks via background thread

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python, Flask                     |
| Server    | Gunicorn (gthread worker)         |
| Frontend  | Vanilla HTML/CSS/JavaScript (SPA) |
| Deploy    | Render                            |

No database — all state is held in-memory using custom data structures.

---

## Data Structures Used

| Structure        | Where                  | Why                                      |
|------------------|------------------------|------------------------------------------|
| Dictionary       | `seat_map`, `bookings` | O(1) seat/booking lookup by ID           |
| Set              | `available_seats`      | O(1) add/remove for availability         |
| Stack (list)     | `stack`                | Undo last cancellation (LIFO)            |
| Queue (list)     | `queue`                | Waiting list — first come, first served  |
| Linked List      | `BookingHistory`       | Append-only audit log of all actions     |
| Threading Lock   | `threading.Lock()`     | Mutual exclusion for concurrent bookings |

---

## API Endpoints

| Method | Endpoint                  | Description                        |
|--------|---------------------------|------------------------------------|
| GET    | `/api/movies`             | List all movies                    |
| GET    | `/api/shows/<movie_id>`   | Get showtimes grouped by date/theater |
| GET    | `/api/seatmap/<show_id>`  | Get seat layout and availability   |
| POST   | `/api/lock`               | Atomically lock selected seats     |
| POST   | `/api/confirm`            | Confirm booking after lock         |
| POST   | `/api/cancel/<booking_id>`| Cancel a confirmed booking         |
| GET    | `/api/bookings`           | List all bookings                  |
| GET    | `/api/history`            | Activity log                       |

---

## Booking Flow

```
Browse Movies → Select Date/Theater/Time → Choose Seats
    → Lock Seats (10 min timer) → Enter Name → Confirm → Booking ID
```

---

## Concurrency Model

Gunicorn runs with **1 process, 4 threads** (`--worker-class gthread --threads 4`).
All seat state is protected by a single `threading.Lock()`. When two users try to book the same seat simultaneously, one gets the lock and succeeds; the other is rejected with a "seat no longer available" message.

---

## Running Locally

```bash
pip install flask gunicorn
python main.py
# Visit http://localhost:5000
```

---

## Deployment

Hosted on Render (free tier).
Start command:
```
gunicorn main:app --workers 1 --worker-class gthread --threads 4
```
