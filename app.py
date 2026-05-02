# app.py

import streamlit as st
from service import TicketBookingSystem

# INIT
if "system" not in st.session_state:
    st.session_state.system = TicketBookingSystem()

if "locked_seat" not in st.session_state:
    st.session_state.locked_seat = None

system = st.session_state.system

st.set_page_config(page_title="Smart Booking", page_icon="🎬")

st.title("🎬 Smart Movie Ticket Booking System")

# ---------------- LOCK ----------------
st.subheader("🎟️ Step 1: Lock Seat")

name = st.text_input("Enter your name")

if st.button("Lock Seat"):
    result = system.lock_seat(name)

    if "Seat" in result:
        seat = int(result.split()[1])
        st.session_state.locked_seat = seat

    st.success(result)

# ---------------- CONFIRM ----------------
st.subheader("✅ Step 2: Confirm Booking")

seat_no = st.number_input(
    "Enter seat number to confirm",
    value=st.session_state.locked_seat if st.session_state.locked_seat else 1,
    min_value=1
)

if st.button("Confirm Booking"):
    st.success(system.confirm_booking(seat_no, name))

# ---------------- CANCEL ----------------
st.subheader("❌ Cancel Ticket")

cancel_seat = st.number_input("Seat number to cancel", min_value=1, key="cancel")

if st.button("Cancel Ticket"):
    st.warning(system.cancel_ticket(cancel_seat))

# ---------------- UNDO ----------------
st.subheader("↩️ Undo Cancellation")

if st.button("Undo Last Cancellation"):
    st.info(system.undo_cancellation())

# ---------------- SEATS ----------------
st.subheader("📊 Seat Status")

cols = st.columns(5)
seats = system.show_seats()

for i, seat in enumerate(seats):
    col = cols[i % 5]

    if "Booked" in seat:
        col.markdown(f"🔴 {seat}")
    elif "Locked" in seat:
        col.markdown(f"🟡 {seat}")
    else:
        col.markdown(f"🟢 {seat}")

# ---------------- WAITING ----------------
st.subheader("⏳ Waiting List")

waiting = system.show_waiting()

if waiting == ["Empty"]:
    st.info("No users in waiting list")
else:
    for i, user in enumerate(waiting, 1):
        st.write(f"{i}. {user}")

# ---------------- STACK ----------------
st.subheader("🗂️ Cancellation Stack")

stack = system.show_cancellations()

if stack == ["Empty"]:
    st.info("No cancellations yet")
else:
    for i, (name, seat) in enumerate(reversed(stack), 1):
        st.write(f"{i}. {name} (Seat {seat})")
