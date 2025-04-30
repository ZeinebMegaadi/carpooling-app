# app/streamlit_app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# --- Custom Styling ---
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    h1, h2, h3, h4 {
        color: #00416d;
    }
    .css-1d391kg, .css-1q8dd3e {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Page Config ---
st.set_page_config(page_title="Uni Carpooling", layout="wide")
st.title("🚗 Uni Carpooling App")
st.markdown("""
### Welcome to the SMU Carpooling Assistant
Plan efficient routes to university with smart suggestions based on real distances. Visualize graph-based connections between students.
""")

# --- Load Distance Matrix ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/distance_matrix_km.csv", index_col=0)
    df.index = df.index.str.strip()
    df.columns = df.columns.str.strip()
    return df

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

# --- Build Graph with Only Nearest Edges ---
G_full = nx.DiGraph()
for student in students:
    dists = dist_df.loc[student].drop(labels=[student], errors='ignore').apply(lambda x: max(x, MIN_DIST))
    nearest = dists.nsmallest(3)
    for neighbor, weight in nearest.items():
        G_full.add_edge(student, neighbor, weight=weight)

# --- Display Directional Graph of Closest Connections ---
with st.expander("🔍 Full Student Graph (Closest Edges Only)"):
    st.subheader("Graph of Students with Arrows to 3 Nearest Neighbors")
    fig_full, ax_full = plt.subplots(figsize=(9, 9))
    pos_full = nx.spring_layout(G_full, seed=42)
    weights = np.array([G_full[u][v]['weight'] for u, v in G_full.edges()])
    norm = plt.Normalize(weights.min(), weights.max())
    colors = cm.viridis(norm(weights))
    nx.draw_networkx_nodes(G_full, pos_full, node_size=350, node_color='lightblue', ax=ax_full)
    nx.draw_networkx_labels(G_full, pos_full, font_size=8, ax=ax_full)
    nx.draw_networkx_edges(G_full, pos_full, edge_color=colors, edge_cmap=cm.viridis, arrows=True, width=2, ax=ax_full)
    edge_labels = {(u, v): f"{G_full[u][v]['weight']:.2f}" for u, v in G_full.edges()}
    nx.draw_networkx_edge_labels(G_full, pos_full, edge_labels=edge_labels, font_size=6, ax=ax_full)
    ax_full.set_axis_off()
    st.pyplot(fig_full)

# --- Role Selection ---
role = st.radio("I am a:", ["Driver", "Passenger"])

# Continue your logic...
