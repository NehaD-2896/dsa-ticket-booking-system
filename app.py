# app.py

import streamlit as st
from service import TicketBookingSystem

if "system" not in st.session_state:
    st.session_state.system = TicketBookingSystem()

system = st.session_state.system

st.title("🎬 Smart Movie Booking System")

# Booking
name = st.text_input("Enter your name")

if st.button("Book Ticket"):
    st.success(system.book_ticket(name))

# Cancel
seat_no = st.number_input("Seat number to cancel", min_value=1, step=1)

if st.button("Cancel Ticket"):
    st.warning(system.cancel_ticket(seat_no))

# Undo
if st.button("Undo Cancellation"):
    st.info(system.undo_cancellation())

# Display
st.subheader("Seat Status")
for s in system.show_seats():
    st.write(s)

st.subheader("Waiting List")
st.write(system.show_waiting())

st.subheader("Cancellation Stack")
st.write(system.show_cancellations())
