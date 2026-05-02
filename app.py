# app.py

import streamlit as st
from service import TicketBookingSystem

# ---------------- INIT ----------------
if "system" not in st.session_state:
    st.session_state.system = TicketBookingSystem()

system = st.session_state.system

st.set_page_config(page_title="Smart Movie Booking", page_icon="🎬")

st.title("🎬 Smart Movie Ticket Booking System")

# ---------------- LOCK & CONFIRM ----------------
st.subheader("🎟️ Step 1: Lock Seat")

name = st.text_input("Enter your name")

col1, col2 = st.columns(2)

with col1:
    if st.button("Lock Seat"):
        if name.strip():
            st.success(system.lock_seat(name))
        else:
            st.error("Please enter a valid name")

result = system.lock_seat(name)
st.success(result)
st.toast("Seat locked! Complete booking within time ⏳")

# ---------------- CONFIRM ----------------
st.subheader("✅ Step 2: Confirm Booking")

seat_no = st.number_input("Enter seat number to confirm", min_value=1, step=1)

with col2:
    if st.button("Confirm Booking"):
        st.success(system.confirm_booking(seat_no))

# ---------------- CANCEL ----------------
st.subheader("🗂️ Cancellation Stack")

stack = system.show_cancellations()

if stack == ["Empty"] or stack == ["No cancellations"]:
    st.info("No cancellations yet")
else:
    for i, (name, seat) in enumerate(reversed(stack), 1):
        st.write(f"{i}. {name} (Seat {seat})")

# ---------------- UNDO ----------------
st.subheader("↩️ Undo Cancellation")

if st.button("Undo Last Cancellation"):
    st.info(system.undo_cancellation())

# ---------------- DISPLAY ----------------
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

st.subheader("⏳ Waiting List")

waiting = system.show_waiting()

if waiting == ["Empty"] or waiting == ["Waiting list empty"]:
    st.info("No users in waiting list")
else:
    for i, user in enumerate(waiting, 1):
        st.write(f"{i}. {user}")
