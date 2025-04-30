import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load and clean distance matrix
df = pd.read_csv("distance_matrix_km.csv", index_col=0)
df.index = df.index.str.strip()
df.columns = df.columns.str.strip()
students = list(df.index)

# Create graph from distance matrix
def create_graph(df):
    G = nx.Graph()
    for i in df.index:
        for j in df.columns:
            if i != j:
                try:
                    G.add_edge(i, j, weight=float(df.loc[i, j]))
                except KeyError:
                    continue
    return G

G = create_graph(df)

# Session state
if 'role' not in st.session_state:
    st.session_state.role = None
if 'requests' not in st.session_state:
    st.session_state.requests = {}
if 'accepted' not in st.session_state:
    st.session_state.accepted = {}

st.title("🚗 SMU Carpooling Network App")

# User selection
current_user = st.selectbox("Select your name:", students)

# Role selection
if st.session_state.role is None:
    st.session_state.role = st.radio("Are you a driver or a passenger?", ["Driver", "Passenger"])

# Random drivers
random.seed(42)
drivers = random.sample([s for s in students if s != current_user], min(7, len(students)-1))

st.markdown("### 👥 Carpool Network Graph (All Students)")
fig1, ax1 = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, ax=ax1)
st.pyplot(fig1)

# Passenger logic
if st.session_state.role == "Passenger":
    available_drivers = [d for d in drivers if d != current_user]
    selected_driver = st.selectbox("Select a driver to request carpool with:", available_drivers)
    if st.button("Send Request"):
        st.session_state.requests.setdefault(selected_driver, []).append(current_user)
        st.success(f"Request sent to {selected_driver}")

# Driver logic
if st.session_state.role == "Driver":
    st.markdown(f"### 🚘 Welcome Driver: **{current_user}**")
    requests = st.session_state.requests.get(current_user, [])
    if requests:
        for passenger in requests:
            col1, col2 = st.columns([2,1])
            with col1:
                st.write(f"Passenger request from: {passenger}")
            with col2:
                if st.button(f"Accept {passenger}"):
                    st.session_state.accepted.setdefault(current_user, []).append(passenger)
                    st.success(f"Accepted {passenger}")
    else:
        st.info("No requests yet.")

# Show shortest path
if st.session_state.role == "Driver" and current_user in st.session_state.accepted:
    passengers = st.session_state.accepted[current_user]
    st.markdown("### 🗺️ Shortest Path Graph to Passengers")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    shortest_path_graph = nx.Graph()
    for p in passengers:
        try:
            path = nx.shortest_path(G, source=current_user, target=p, weight='weight')
            nx.add_path(shortest_path_graph, path)
        except nx.NetworkXNoPath:
            st.warning(f"No path between {current_user} and {p}")
    nx.draw(shortest_path_graph, pos, with_labels=True, node_size=500, font_size=8, ax=ax2, edge_color='green')
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("SMU Carpooling App using Graph Theory | Developed with Streamlit")
