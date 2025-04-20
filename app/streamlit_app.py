# app/streamlit_app.py

import streamlit as st
import pandas as pd

# --- Load the single CSV (distance matrix) ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/distance_matrix_km.csv", index_col=0)
    return df

# Load distances and student list
dist_df = load_data()
students = dist_df.index.tolist()

# Initialize session state for active drivers
if "active_drivers" not in st.session_state:
    st.session_state.active_drivers = {}  # { driver_name: [passenger1, passenger2, ...] }

# --- App UI ---
st.title("🚗 Uni Carpooling App")

role = st.radio("I am a:", ["Driver", "Passenger"])

if role == "Driver":
    driver = st.selectbox("Select your name:", students)
    if driver:
        # Compute three nearest other students
        dists = dist_df.loc[driver].drop(driver)
        nearest = dists.nsmallest(3)
        
        st.subheader("Suggested riders:")
        for name, km in nearest.items():
            st.write(f"- {name}  ({km:.2f} km)")

        # Accept button
        if st.button("✅ Accept these riders"):
            st.session_state.active_drivers[driver] = list(nearest.index)
            st.success(f"You’ll drive: {', '.join(nearest.index)}")

elif role == "Passenger":
    passenger = st.selectbox("Select your name:", students)
    if passenger:
        active = st.session_state.active_drivers
        if not active:
            st.info("No drivers have signed up yet. Please check back later.")
        else:
            # Compute each active driver's distance to this passenger
            options = [(drv, dist_df.at[drv, passenger]) for drv in active]
            options.sort(key=lambda x: x[1])

            st.subheader("Available drivers:")
            for drv, km in options:
                st.write(f"- {drv}  ({km:.2f} km away)")
                if st.button(f"Request ride from {drv}", key=f"request_{drv}"):
                    st.success(f"Ride requested from **{drv}**! 🚀")
