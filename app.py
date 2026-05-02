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

# ---------------- CONFIRM ----------------
st.subheader("✅ Step 2: Confirm Booking")

seat_no = st.number_input("Enter seat number to confirm", min_value=1, step=1)

with col2:
    if st.button("Confirm Booking"):
        st.success(system.confirm_booking(seat_no))

# ---------------- CANCEL ----------------
st.subheader("❌ Cancel Ticket")

cancel_seat = st.number_input("Enter seat number to cancel", min_value=1, step=1, key="cancel")

if st.button("Cancel Ticket"):
    st.warning(system.cancel_ticket(cancel_seat))

# ---------------- UNDO ----------------
st.subheader("↩️ Undo Cancellation")

if st.button("Undo Last Cancellation"):
    st.info(system.undo_cancellation())

# ---------------- DISPLAY ----------------
st.subheader("📊 Seat Status")

seats = system.show_seats()
for s in seats:
    st.write(s)

st.subheader("⏳ Waiting List")
st.write(system.show_waiting())

st.subheader("🗂️ Cancellation Stack")
st.write(system.show_cancellations())
