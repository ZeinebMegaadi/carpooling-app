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


    body {
        background-color: #f7f9fc;
        color: #111111;
    }
    .stApp {
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
    
/* Ensure button text is visible */
button[kind="secondary"] div,
button[kind="primary"] div,
button div {
    color: white !important;
}
/* Ensure radio labels are dark */
.css-1a32fsj span,
.css-16idsys span,
.stRadio label {
    color: #111111 !important;
}

/* Force black text on radio buttons */
.stRadio label div[data-testid="stMarkdownContainer"] > p {
    color: #111111 !important;
    font-weight: 500;
}

/* Fix message colors */
.css-1cpxqw2 {  /* st.success */
    background-color: #0f5132 !important;
    color: #ffffff !important;
    font-weight: 700;
}
.css-1wivap2 {  /* st.warning used as decline */
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
        return df
    except Exception as e:
        st.error(f"❌ Failed to load CSV: {e}")
        return pd.DataFrame()

dist_df = load_data()
students = dist_df.index.tolist()

# --- Session State ---
if "active_drivers" not in st.session_state:
    st.session_state.active_drivers = {}
if "accepted_riders" not in st.session_state:
    st.session_state.accepted_riders = {}

# --- Constants ---
MIN_DIST = 0.01
MAX_DIST = 7.0

# --- Build Graph ---
G_full = nx.DiGraph()
for student in students:
    dists = dist_df.loc[student].drop(student).apply(lambda x: max(x, MIN_DIST))
    nearest = dists.nsmallest(3)
    for neighbor, weight in nearest.items():
        G_full.add_edge(student, neighbor, weight=weight)

# --- Full Graph Display ---
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

# --- Shortest Path Tree ---
with st.expander("🧭 Shortest Path Tree Graph"):
    st.markdown("<div class='block-title'>Shortest Path Tree from a Starting Student</div>", unsafe_allow_html=True)
    selected = st.selectbox("Select a student to build shortest path tree from:", students, key="spt_selector")
    if selected:
        G_spt = nx.Graph()
        for target in students:
            if selected != target:
                try:
                    path = nx.shortest_path(G_full, source=selected, target=target, weight='weight')
                    for u, v in zip(path[:-1], path[1:]):
                        weight = max(dist_df.at[u, v], MIN_DIST)
                        G_spt.add_edge(u, v, weight=weight)
                except nx.NetworkXNoPath:
                    pass
        fig_spt, ax_spt = plt.subplots(figsize=(8, 8))
        pos_spt = nx.spring_layout(G_spt, seed=42)
        node_colors = ['red' if node == selected else 'green' for node in G_spt.nodes()]
        nx.draw(G_spt, pos_spt, node_size=300, node_color=node_colors, with_labels=True, font_size=8, ax=ax_spt)
        edge_labels = nx.get_edge_attributes(G_spt, 'weight')
        nx.draw_networkx_edge_labels(G_spt, pos_spt, edge_labels={k: f"{v:.2f}" for k, v in edge_labels.items()}, font_size=6, ax=ax_spt)
        red_patch = plt.Line2D([0], [0], marker='o', color='w', label='Driver (Red)', markerfacecolor='red', markersize=10)
        green_patch = plt.Line2D([0], [0], marker='o', color='w', label='Passenger (Green)', markerfacecolor='green', markersize=10)
        ax_spt.legend(handles=[red_patch, green_patch], loc='upper right')
        ax_spt.set_axis_off()
        st.pyplot(fig_spt)

# --- Driver Flow ---
if role == "Driver":
    st.markdown("<div class='block-title'>Suggested Riders</div>", unsafe_allow_html=True)
    driver = st.selectbox("Select your name:", students)
    if driver:
        dists = dist_df.loc[driver].drop(driver).apply(lambda x: max(x, MIN_DIST))
        dists = dists[dists <= MAX_DIST]
        nearest = dists.nsmallest(3)
        accepted_riders = st.session_state.accepted_riders.setdefault(driver, [])
        for name, km in nearest.items():
            cols = st.columns([3, 1, 1])
            cols[0].write(f"**{name}** — {km:.2f} km")
            if name in accepted_riders:
                if cols[2].button("Decline", key=f"decline_{name}"):
                    accepted_riders.remove(name)
                    if name in st.session_state.active_drivers.get(driver, []):
                        st.session_state.active_drivers[driver].remove(name)
                    st.warning(f"Declined {name}")
            else:
                if cols[1].button("Accept", key=f"accept_{name}"):
                    accepted_riders.append(name)
                    st.session_state.active_drivers.setdefault(driver, []).append(name)
                    st.success(f"Accepted {name}")
        if accepted_riders:
            st.markdown("<div class='block-title'>📈 Your Route to University</div>", unsafe_allow_html=True)
            G_route = nx.Graph()
            G_route.add_node(driver)
            for r in accepted_riders:
                G_route.add_node(r)
                G_route.add_edge(driver, r, weight=dist_df.at[driver, r])
            fig_route, ax_route = plt.subplots(figsize=(6, 6))
            pos_route = nx.spring_layout(G_route, seed=24)
            node_colors = ['red'] + ['green'] * len(accepted_riders)
            nx.draw(G_route, pos_route, node_size=400, node_color=node_colors,
                    with_labels=True, font_weight='bold', font_size=8, ax=ax_route)
            edge_labels = {(driver, r): f"{dist_df.at[driver, r]:.2f} km" for r in accepted_riders}
            nx.draw_networkx_edge_labels(G_route, pos_route, edge_labels=edge_labels, font_size=8, ax=ax_route)
            ax_route.set_axis_off()
            st.pyplot(fig_route)

# --- Passenger Flow ---
elif role == "Passenger":
    st.markdown("<div class='block-title'>Available Drivers</div>", unsafe_allow_html=True)
    passenger = st.selectbox("Select your name:", students)
    if passenger:
        active = st.session_state.active_drivers
        if not active:
            st.info("No drivers available at the moment. Please check back soon.")
        else:
            options = [(drv, max(dist_df.at[drv, passenger], MIN_DIST)) for drv in active]
            options = [opt for opt in options if opt[1] <= MAX_DIST]
            options.sort(key=lambda x: x[1])
            for drv, km in options:
                cols = st.columns([4, 1])
                cols[0].write(f"**{drv}** — {km:.2f} km away")
                if cols[1].button("Request Ride", key=f"req_{drv}"):
                    st.success(f"Ride requested from {drv}! 🚀")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("Reset App State"):
        for key in ["active_drivers", "accepted_riders"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
        
