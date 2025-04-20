# streamlit_app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def add_university_node(G, university_coords, student_coords_df):
    G.add_node("University")
    for _, row in student_coords_df.iterrows():
        student = row['Name']
        lat, lon = row['Latitude'], row['Longitude']
        dist = np.sqrt((lat - university_coords[0])**2 + (lon - university_coords[1])**2)
        G.add_edge(student, "University", weight=dist)
    return G

def find_shortest_path(driver, passengers, G):
    paths = {
        p: {
            "path": nx.shortest_path(G, driver, p, weight="weight"),
            "distance": nx.shortest_path_length(G, driver, p, weight="weight")
        } for p in passengers
    }
    uni_path = nx.shortest_path(G, driver, "University", weight="weight")
    uni_dist = nx.shortest_path_length(G, driver, "University", weight="weight")
    return paths, uni_path, uni_dist

# App
st.title("🚗 Carpool Route Optimizer")

uploaded_coords = st.file_uploader("Upload student coordinates CSV", type="csv")
uploaded_matrix = st.file_uploader("Upload distance matrix CSV", type="csv")

if uploaded_coords and uploaded_matrix:
    coords_df = pd.read_csv(uploaded_coords)
    dist_df = pd.read_csv(uploaded_matrix, index_col=0)

    # Build Graph
    G = nx.Graph()
    for node in dist_df.columns:
        G.add_node(node)
    for i in dist_df.columns:
        for j in dist_df.columns:
            if i != j and pd.notna(dist_df.loc[i, j]):
                G.add_edge(i, j, weight=dist_df.loc[i, j])

    # Add university as a node
    university_coords = (36.8650, 10.3220)
    G = add_university_node(G, university_coords, coords_df)

    st.subheader("Graph Preview")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=6)
    st.pyplot(fig)

    driver = st.selectbox("Select Driver", dist_df.columns)
    passengers = st.multiselect("Select up to 3 Passengers", [p for p in dist_df.columns if p != driver])

    if len(passengers) > 3:
        st.warning("Please select no more than 3 passengers.")
    elif driver and passengers:
        st.subheader("🚦 Route Summary")
        shortest_paths, uni_path, uni_dist = find_shortest_path(driver, passengers, G)

        for p, result in shortest_paths.items():
            st.write(f"🧍 {p}: Path - {result['path']} | Distance: {result['distance']:.2f} km")

        st.write(f"🏫 University Path: {uni_path} | Distance: {uni_dist:.2f} km")
