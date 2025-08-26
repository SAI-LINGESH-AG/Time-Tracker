import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="5 Hours Tracker", layout="centered")

# User input
start_time_str = st.text_input("Enter start time (HH:MM AM/PM)", "09:00 AM")

if st.button("Calculate"):
    try:
        # Parse start time
        start_time = datetime.strptime(start_time_str, "%I:%M %p")

        # Target time = start + 5 hours
        target_time = start_time + timedelta(hours=5)

        # Current time (today’s clock)
        now = datetime.now().replace(year=start_time.year, month=start_time.month, day=start_time.day)

        # Check validity
        if now < start_time:
            st.warning("Current time is before the given start time. Please wait until start time.")
        else:
            # Time differences
            elapsed_delta = now - start_time
            remaining_delta = target_time - now

            if remaining_delta.total_seconds() < 0:
                remaining_delta = timedelta(0)

            # Format helper
            def format_hms(td):
                total_seconds = int(td.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            # Show results
            st.write(f"Start Time: {start_time.strftime('%I:%M %p')}")
            st.write(f"Target End Time: {target_time.strftime('%I:%M %p')}")
            st.write(f"Hours Elapsed: {format_hms(elapsed_delta)}")
            st.write(f"Hours Remaining: {format_hms(remaining_delta)}")

    except ValueError:
        st.error("Invalid format! Please use HH:MM AM/PM (e.g., 09:30 AM)")
