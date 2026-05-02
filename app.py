movies = ["Doctor Strange", "Avatar 2", "Batman", "Spider-Man"]
selected_movie = st.sidebar.selectbox("Select Movie", movies)

import streamlit as st
# Changed this line to match your filename 'structures.py'
from structures import BookingQueue 

if 'system' not in st.session_state:
    st.session_state.system = BookingQueue()
    st.session_state.history = []

st.set_page_config(page_title="Amazon Ticket System", page_icon="🎟️")

st.title("🎟️ Movie Ticket Booking System")

# Sidebar
st.sidebar.header("New Booking")
name = st.sidebar.text_input("Customer Name")
is_prime = st.sidebar.checkbox("Is Prime Member?")

if st.sidebar.button("Add to Queue"):
    if name:
        priority = 1 if is_prime else 2
        st.session_state.system.add_customer(name, priority)
        st.session_state.history.append(f"✅ Added {name} ({'Prime' if is_prime else 'Regular'})")
        st.sidebar.success(f"Added {name}!")

# Main logic
if st.button("Serve Next Customer"):
    result = st.session_state.system.serve_next()
    st.session_state.history.append(f"🚀 {result}")
    st.info(result)

st.header("Activity Log")
for log in reversed(st.session_state.history):
    st.write(log)
