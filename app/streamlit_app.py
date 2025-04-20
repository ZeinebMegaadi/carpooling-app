# app/streamlit_app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="Uni Carpooling", layout="wide")
st.title("🚗 Uni Carpooling App")
st.markdown("**Leveraging Graph Theory for Smart Carpool Matching**")

# --- Load Distance Matrix ---
@st.cache_data
def load_data():
    return pd.read_csv("data/distance_matrix_km.csv", index_col=0)

dist_df = load_data()
students = dist_df.index.tolist()

# --- Session State for Active Drivers and Accepted Riders ---
if "active_drivers" not in st.session_state:
    st.session_state.active_drivers = {}
if "accepted_riders" not in st.session_state:
    st.session_state.accepted_riders = {}

# --- Constants for Distance Filtering ---
MIN_DIST = 0.01
MAX_DIST = 7.0

# --- Build Full Student Graph ---
G_full = nx.Graph()
for i in students:
    for j in students:
        if i != j:
            d = max(dist_df.at[i, j], MIN_DIST)
            G_full.add_edge(i, j, weight=d)

# --- Display Full Graph for Professor ---
with st.expander("🔍 Full Student Graph"):
    st.subheader("Full Graph of All Students")
    fig_full, ax_full = plt.subplots(figsize=(6, 6))
    pos_full = nx.spring_layout(G_full, seed=42)
    nx.draw(G_full, pos_full, node_size=40, node_color='lightblue', with_labels=False, ax=ax_full)
    ax_full.set_axis_off()
    st.pyplot(fig_full)

# --- Role Selection ---
role = st.radio("I am a:", ["Driver", "Passenger"])

# --- Driver Flow ---
if role == "Driver":
    driver = st.selectbox("Select your name:", students)
    if driver:
        # Compute nearest riders within MAX_DIST
        dists = dist_df.loc[driver].drop(driver).apply(lambda x: max(x, MIN_DIST))
        dists = dists[dists <= MAX_DIST]
        nearest = dists.nsmallest(3)

        st.subheader("Suggested Riders (closest first)")
        for name, km in nearest.items():
            cols = st.columns([4, 1])
            cols[0].write(f"**{name}** — {km:.2f} km")
            if cols[1].button("Accept", key=f"accept_{name}"):
                st.session_state.accepted_riders.setdefault(driver, []).append(name)
                st.session_state.active_drivers.setdefault(driver, []).append(name)
                st.success(f"Accepted {name}")

        # Show shortest-path subgraph for this driver
        if driver in st.session_state.accepted_riders:
            riders = st.session_state.accepted_riders[driver]
            st.subheader("📈 Shortest-Path Graph for Your Route")
            G_route = nx.Graph()
            # Add driver and riders to subgraph
            G_route.add_node(driver)
            for r in riders:
                G_route.add_node(r)
                G_route.add_edge(driver, r, weight=dist_df.at[driver, r])

            fig_route, ax_route = plt.subplots(figsize=(5, 5))
            pos_route = nx.spring_layout(G_route, seed=24)
            nx.draw(G_route, pos_route, node_size=200,
                    node_color=['green'] + ['orange'] * len(riders),
                    with_labels=True, font_weight='bold', ax=ax_route)
            edge_labels = {(driver, r): f"{dist_df.at[driver, r]:.2f} km" for r in riders}
            nx.draw_networkx_edge_labels(G_route, pos_route, edge_labels=edge_labels, font_size=8, ax=ax_route)
            ax_route.set_axis_off()
            st.pyplot(fig_route)

# --- Passenger Flow ---
elif role == "Passenger":
    passenger = st.selectbox("Select your name:", students)
    if passenger:
        active = st.session_state.active_drivers
        if not active:
            st.info("No drivers available at the moment. Please check back soon.")
        else:
            st.subheader("Available Drivers Near You")
            # Compute and filter distances
            options = [(drv, max(dist_df.at[drv, passenger], MIN_DIST)) for drv in active]
            options = [opt for opt in options if opt[1] <= MAX_DIST]
            options.sort(key=lambda x: x[1])
            for drv, km in options:
                cols = st.columns([4, 1])
                cols[0].write(f"**{drv}** — {km:.2f} km away")
                if cols[1].button("Request Ride", key=f"req_{drv}"):
                    st.success(f"Ride requested from {drv}! 🚀")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("Reset App State"):
        for key in ["active_drivers", "accepted_riders"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
