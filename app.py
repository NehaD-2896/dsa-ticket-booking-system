import streamlit as st
from data_structures.priority_queue import BookingQueue

# Initialize the booking system in the "session" so it doesn't reset on every click
if 'system' not in st.session_state:
    st.session_state.system = BookingQueue()
    st.session_state.history = []

st.set_page_config(page_title="Amazon Ticket System", page_icon="🎟️")

st.title("🎟️ Movie Ticket Booking System")
st.markdown("---")

# Sidebar for adding customers
st.sidebar.header("New Booking")
name = st.sidebar.text_input("Customer Name")
is_prime = st.sidebar.checkbox("Is Prime Member?")

if st.sidebar.button("Add to Queue"):
    if name:
        priority = 1 if is_prime else 2
        st.session_state.system.add_customer(name, priority)
        st.session_state.history.append(f"✅ Added {name} ({'Prime' if is_prime else 'Regular'})")
        st.sidebar.success(f"Added {name}!")
    else:
        st.sidebar.error("Please enter a name.")

# Main area for serving customers
col1, col2 = st.columns(2)

with col1:
    st.header("Process Queue")
    if st.button("Serve Next Customer"):
        result = st.session_state.system.serve_next()
        st.session_state.history.append(f"🚀 {result}")
        st.info(result)

with col2:
    st.header("Activity Log")
    for log in reversed(st.session_state.history):
        st.write(log)
