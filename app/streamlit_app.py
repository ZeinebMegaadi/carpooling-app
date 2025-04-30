# app/streamlit_app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Uni Carpooling", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    body, .stApp {
        background-color: #f7f9fc;
        color: #111111;
    }
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    h1, h2, h3, h4 {
        color: #111111;
    }
    .block-title {
        font-size: 20px;
        margin-top: 2rem;
        font-weight: bold;
        color: #111111;
    }
    .section {
        background-color: #ffffff;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        color: #111111;
    }
    button div {
        color: white !important;
    }
    .stRadio label div[data-testid="stMarkdownContainer"] > p {
        color: #111111 !important;
        font-weight: 500;
    }
    .stAlert-success {
        background-color: #0f5132 !important;
        color: #ffffff !important;
        font-weight: 700;
    }
    .stAlert-warning {
        background-color: #6a1a21 !important;
        color: #ffffff !important;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🚗 Uni Carpooling App")
st.markdown("""
### Welcome to the SMU Carpooling Assistant
Plan efficient routes to university with smart suggestions based on real distances. Visualize graph-based connections between students.
""")

# --- Load Distance Matrix ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/distance_matrix_km.csv", index_col=0)
        df.index = df.index.str.strip()
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")
        return pd.DataFrame()

dist_df = load_data()
students = dist_df.index.tolist() if not dist_df.empty else []

# --- Session State ---
if "active_drivers" not in st.session_state:
    st.session_state.active_drivers = {}
if "accepted_riders" not in st.session_state:
    st.session_state.accepted_riders = {}

# --- Constants ---
MIN_DIST = 0.01
MAX_DIST = 7.0

# --- Graph Section ---
if not dist_df.empty:
    G_full = nx.DiGraph()
    for student in students:
        dists = dist_df.loc[student].drop(labels=[student], errors='ignore').apply(lambda x: max(x, MIN_DIST))
        nearest = dists.nsmallest(3)
        for neighbor, weight in nearest.items():
            G_full.add_edge(student, neighbor, weight=weight)

    with st.expander("🔍 Full Student Graph (Closest Edges Only)"):
        st.markdown('<div class="block-title">Graph of Students with Arrows to 3 Nearest Neighbors</div>', unsafe_allow_html=True)
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
    st.markdown("<div class='block-title'>Role Selection</div>", unsafe_allow_html=True)
    role = st.radio("I am a:", ["Driver", "Passenger"])

    # --- Further logic for Driver/Passenger flows ---
    # ... (Retain previous logic here; this section hasn't changed) ...
