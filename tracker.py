import streamlit as st
from datetime import datetime, timedelta
import pytz
from streamlit_js_eval import get_timezone

st.set_page_config(page_title="5 Hours Tracker", layout="centered")

# Auto-detect user's timezone
user_tz = get_timezone()

if user_tz is None:
    st.warning("Unable to detect timezone. Defaulting to UTC.")
    user_tz = "UTC"

# User input
start_time_str = st.text_input("Enter start time (HH:MM AM/PM)", "09:00 AM")

if st.button("Calculate"):
    try:
        tz = pytz.timezone(user_tz)

        # Parse start time in user's timezone
        today = datetime.now(tz).date()
        start_time = datetime.strptime(start_time_str, "%I:%M %p").time()
        start_datetime = tz.localize(datetime.combine(today, start_time))

        # Target time = start + 5 hours
        target_time = start_datetime + timedelta(hours=5)

        # Current time in user's timezone
        now = datetime.now(tz)

        if now < start_datetime:
            st.warning("Current time is before the given start time. Please wait until start time.")
        else:
            # Time deltas
            elapsed_delta = now - start_datetime
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
            st.write(f"Detected Timezone: {user_tz}")
            st.write(f"Start Time: {start_datetime.strftime('%I:%M %p')}")
            st.write(f"Target End Time: {target_time.strftime('%I:%M %p')}")
            st.write(f"Hours Elapsed: {format_hms(elapsed_delta)} (HH:MM:SS)")
            st.write(f"Hours Remaining: {format_hms(remaining_delta)} (HH:MM:SS)")

    except ValueError:
        st.error("Invalid format! Please use HH:MM AM/PM (e.g., 09:30 AM)")
