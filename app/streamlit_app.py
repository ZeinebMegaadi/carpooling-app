# app/streamlit_app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# --- Load the single CSV (distance matrix) ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/distance_matrix_km.csv", index_col=0)
    return df

# Load data and student list
dist_df = load_data()
students = dist_df.index.tolist()

# --- Initialize session state ---
if "active_drivers" not in st.session_state:
    st.session_state.active_drivers = {}
if "accepted_riders" not in st.session_state:
    st.session_state.accepted_riders = {}

# Populate random sample drivers for testing if none exist
if not st.session_state.active_drivers:
    sample_drivers = random.sample(students, k=min(3, len(students)))
    for drv in sample_drivers:
        others = [s for s in students if s != drv]
        st.session_state.active_drivers[drv] = random.sample(others, k=random.randint(1, 3))

# --- App UI ---
st.set_page_config(page_title="Uni Carpooling", layout="wide")
st.title("🚗 Uni Carpooling App")
role = st.radio("I am a:", ["Driver", "Passenger"])

if role == "Driver":
    driver = st.selectbox("Select your name:", students)
    if driver:
        # Suggest nearest riders (exclude zero distances)
        dists = dist_df.loc[driver].drop(driver)
        dists = dists[dists > 0]
        nearest = dists.nsmallest(3)

        st.subheader("Suggested riders (closest 3):")
        for name, km in nearest.items():
            col1, col2 = st.columns([4, 1])
            col1.write(f"{name} — {km:.2f} km away")
            if col2.button("Accept", key=f"accept_{name}"):
                riders = st.session_state.accepted_riders.setdefault(driver, [])
                if name not in riders:
                    riders.append(name)
                    st.session_state.active_drivers.setdefault(driver, []).append(name)
                    st.success(f"Accepted {name}!")

        # Show current accepted riders and route graph
        riders = st.session_state.accepted_riders.get(driver, [])
        if riders:
            st.subheader("Your accepted riders:")
            st.write(", ".join(riders))

            # Build subgraph for visualization
            G = nx.Graph()
            G.add_node(driver)
            for r in riders:
                G.add_node(r)
                G.add_edge(driver, r, weight=dist_df.at[driver, r])

            fig, ax = plt.subplots()
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_size=600, node_color="skyblue", ax=ax)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)
            st.pyplot(fig)

elif role == "Passenger":
    passenger = st.selectbox("Select your name:", students)
    if passenger:
        active = st.session_state.active_drivers
        if not active:
            st.info("No drivers are available currently. Please check back later.")
        else:
            # Compute distance from each active driver to this passenger
            options = [(drv, dist_df.at[drv, passenger]) for drv in active]
            options = [(drv, km) for drv, km in options if km > 0]
            options.sort(key=lambda x: x[1])

            st.subheader("Available drivers (sorted by proximity):")
            for drv, km in options:
                col1, col2 = st.columns([4, 1])
                col1.write(f"{drv} — {km:.2f} km away")
                if col2.button("Request ride", key=f"request_{drv}"):
                    st.success(f"Ride requested from {drv}! 🚀")

# --- Sidebar Controls ---
st.sidebar.header("Debug / Reset")
if st.sidebar.button("Reset app state"):
    for key in ["active_drivers", "accepted_riders"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()
