import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="5 Hours Tracker", layout="centered")

# User inputs
start_time_str = st.text_input("Enter start time (HH:MM AM/PM)", "09:00 AM")
check_time_str = st.text_input("Enter check time (HH:MM AM/PM)", "11:00 AM")

if st.button("Calculate"):
    try:
        # Parse both times (no date attached, just time)
        start_time = datetime.strptime(start_time_str, "%I:%M %p")
        check_time = datetime.strptime(check_time_str, "%I:%M %p")

        # Target end = start + 5 hours
        target_time = start_time + timedelta(hours=5)

        # Calculate elapsed and remaining
        elapsed = (check_time - start_time).total_seconds()
        remaining = (target_time - check_time).total_seconds()

        # If check_time is before start_time, assume it's on the next day
        if elapsed < 0:
            elapsed += 24 * 3600
            remaining = (5 * 3600) - elapsed

        if remaining < 0:
            remaining = 0

        # Format helper
        def format_hms(seconds):
            seconds = int(seconds)
            hours, remainder = divmod(seconds, 3600)
            minutes, secs = divmod(remainder, 60)
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"

        # Display results
        st.write(f"Start Time: {start_time.strftime('%I:%M %p')}")
        st.write(f"Target End Time: {target_time.strftime('%I:%M %p')}")
        st.write(f"Hours Elapsed: {format_hms(elapsed)}")
        st.write(f"Hours Remaining: {format_hms(remaining)}")

    except ValueError:
        st.error("Invalid format! Please use HH:MM AM/PM (e.g., 09:30 AM)")
