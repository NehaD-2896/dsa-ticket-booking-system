# 🎬 Smart Movie Ticket Booking System

A Python-based ticket booking system that simulates real-world booking platforms like BookMyShow by implementing core data structures and system design concepts.

🔗 Live Demo: https://your-app-link.streamlit.app

---

## 📌 Features

- 🎟️ Seat Locking System (prevents double booking)
- ⏳ Lock Expiry Mechanism (auto-release after timeout)
- ✅ Booking Confirmation Flow
- ❌ Ticket Cancellation
- ↩️ Undo Cancellation (Stack-based)
- ⏳ Waiting List (Queue-based)
- 📊 Real-time Seat Status Visualization
- 🧠 Efficient seat allocation using optimized data structures

---

## 🧠 Data Structures Used

| Feature                | Data Structure |
|----------------------|---------------|
| Booking History       | Linked List   |
| Cancellation Undo     | Stack         |
| Waiting List          | Queue         |
| Seat Lookup           | HashMap       |
| Seat Allocation       | Set (O(1))    |

---

## ⚙️ System Design Highlights

- Implemented **seat locking with timeout** to handle race conditions
- Ensured **user-specific booking validation**
- Designed a **two-step booking flow (Lock → Confirm)**
- Optimized seat allocation to **O(1) time complexity**
- Modular architecture separating UI and business logic

---

