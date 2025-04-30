import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load distance matrix
df = pd.read_csv("distance_matrix_km.csv", index_col=0)
students = list(df.index)

# Create Graph
def create_graph(df):
    G = nx.Graph()
    for i in df.index:
        for j in df.columns:
            if i != j:
                G.add_edge(i, j, weight=df.loc[i, j])
    return G

G = create_graph(df)

# Session state for role and requests
if 'role' not in st.session_state:
    st.session_state.role = None
if 'requests' not in st.session_state:
    st.session_state.requests = {}
if 'accepted' not in st.session_state:
    st.session_state.accepted = {}

st.title("🚗 SMU Carpooling Network App")

# Select user
current_user = st.selectbox("Select your name:", students)

# Select role
if st.session_state.role is None:
    st.session_state.role = st.radio("Are you a driver or a passenger?", ["Driver", "Passenger"])

# Randomly select 3 drivers
random.seed(42)
drivers = random.sample(students, 7)
drivers_set = set(drivers)

st.markdown("### 👥 Carpool Network Graph (All Students)")
fig1, ax1 = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, ax=ax1)
st.pyplot(fig1)

# Passenger functionality
if st.session_state.role == "Passenger":
    available_drivers = [d for d in drivers if d != current_user]
    selected_driver = st.selectbox("Select a driver to request carpool with:", available_drivers)
    if st.button("Send Request"):
        st.session_state.requests.setdefault(selected_driver, []).append(current_user)
        st.success(f"Request sent to {selected_driver}")

# Driver functionality
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

# Display shortest path graph (Driver + Accepted Passengers)
if st.session_state.role == "Driver" and current_user in st.session_state.accepted:
    passengers = st.session_state.accepted[current_user]
    st.markdown("### 🗺️ Shortest Path Graph to Passengers")
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    shortest_path_graph = nx.Graph()
    for p in passengers:
        path = nx.shortest_path(G, source=current_user, target=p, weight='weight')
        nx.add_path(shortest_path_graph, path)
    nx.draw(shortest_path_graph, pos, with_labels=True, node_size=500, font_size=8, ax=ax2, edge_color='green')
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("SMU Carpooling App using Graph Theory | Developed with Streamlit")
