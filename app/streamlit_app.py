
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# Trimmed distance matrix (3 nearest neighbors)
distance_dict = {
  "Seif Eddine Mezned": {
    "Mohamed Amin Boukettaya": 0.02,
    "Elyes Cyril Boughedir": 0.08,
    "Emna Barbouch": 0.19,
    "Arij Aouina": 2.39,
    "Yasmine Jedidi": 0.03,
    "Youssef Mohamed Bechir": 1.48
  },
  "Mohamed Amin Boukettaya": {
    "Seif Eddine Mezned": 0.02,
    "Ahmed Said Mohamed": 2.39,
    "Mohamed Yamoun Hamdi": 0.19,
    "Emna Barbouch": 0.19,
    "Mahdi Soudani": 0.19,
    "Abdelkarim Elhamdi": 0.19
  },
  "Elyes Cyril Boughedir": {
    "Seif Eddine Mezned": 0.08,
    "Mahdi Soudani": 0.19,
    "Mohamed Yamoun Hamdi": 0.19,
    "Abdelkarim Elhamdi": 0.19,
    "Mohamed Aymen Hassini": 0.19,
    "Emna Barbouch": 0.19,
    "Nabila Ben Zineb": 1.66
  },
  "Emna Barbouch": {
    "Seif Eddine Mezned": 0.19,
    "Mohamed Amin Boukettaya": 0.19,
    "Elyes Cyril Boughedir": 0.19,
    "Yasmine Ben Ismail": 0.3,
    "Yasmine Jedidi": 0.19,
    "Mahdi Soudani": 0.2,
    "Mohamed Bettaieb Marouen": 1.33
  },
  "Mahdi Soudani": {
    "Mohamed Amin Boukettaya": 0.19,
    "Elyes Cyril Boughedir": 0.19,
    "Emna Barbouch": 0.2,
    "Yasmine Jedidi": 0.19,
    "Nabila Ben Zineb": 0.88,
    "Mohamed Aymen Hassini": 0.02
  },
  "Yasmine Jedidi": {
    "Seif Eddine Mezned": 0.03,
    "Emna Barbouch": 0.19,
    "Mahdi Soudani": 0.19,
    "Mohamed Yamoun Hamdi": 0.19,
    "Abidi Fares": 2.15,
    "Mohamed Aymen Hassini": 0.19,
    "Nour Chouchane": 2.15
  },
  "Nabila Ben Zineb": {
    "Elyes Cyril Boughedir": 1.66,
    "Mahdi Soudani": 0.88,
    "Ahmed Said Mohamed": 1.37,
    "Aymen El Hadhri": 0.35,
    "Abdelkarim Elhamdi": 2.17,
    "Mohamed Amine Zekri": 1.37,
    "Arij Aouina": 1.37,
    "Khammassi Nour": 0.35,
    "Youssef Mohamed Bechir": 0.07,
    "Mimouna Baya Chaaben": 0.88
  },
  "Mimouna Baya Chaaben": {
    "Nabila Ben Zineb": 0.88,
    "Ahmed Said Mohamed": 0.24,
    "Arij Aouina": 0.24,
    "Mohamed Aziz Souissi": 1.22,
    "Mohamed Amine Zekri": 0.93,
    "Youssef Mohamed Bechir": 1.34,
    "Yassine Ben Knani": 1.34,
    "Mourad Kochkar": 0.88,
    "Rania Ben Moussa": 1.34
  },
  "Ahmed Said Mohamed": {
    "Mohamed Amin Boukettaya": 2.39,
    "Nabila Ben Zineb": 1.37,
    "Mimouna Baya Chaaben": 0.24,
    "Mohamed Yamoun Hamdi": 2.86,
    "Yasmine Ben Ismail": 0.24,
    "Mohamed Bettaieb Marouen": 3.26
  },
  "Arij Aouina": {
    "Seif Eddine Mezned": 2.39,
    "Nabila Ben Zineb": 1.37,
    "Mimouna Baya Chaaben": 0.24,
    "Aya Hachana": 3.26,
    "Mourad Kochkar": 1.37,
    "Yasmine Ben Ismail": 0.24,
    "Ben Abda Iskander": 2.77
  },
  "Mohamed Aziz Souissi": {
    "Mimouna Baya Chaaben": 1.22,
    "Nour Chouchane": 0.2,
    "Youssef Mohamed Bechir": 2.81,
    "Yassine Ben Knani": 2.81,
    "Aya Hachana": 5.29
  },
  "Nour Chouchane": {
    "Yasmine Jedidi": 2.15,
    "Mohamed Aziz Souissi": 0.2,
    "Mohamed Amine Zekri": 0.67,
    "El Fedi Zairi": 0.3,
    "Abidi Fares": 0.2,
    "Ben Abda Iskander": 0.2,
    "Khammassi Nour": 0.56,
    "Youssef Mohamed Bechir": 2.81
  },
  "Youssef Mohamed Bechir": {
    "Seif Eddine Mezned": 1.48,
    "Nabila Ben Zineb": 0.07,
    "Mimouna Baya Chaaben": 1.34,
    "Mohamed Aziz Souissi": 2.81,
    "Nour Chouchane": 2.81,
    "Aymen El Hadhri": 4.0,
    "El Fedi Zairi": 2.81,
    "Yasmine Ben Ismail": 1.34,
    "Ben Abda Iskander": 2.81
  },
  "Yassine Ben Knani": {
    "Mimouna Baya Chaaben": 1.34,
    "Mohamed Aziz Souissi": 2.81,
    "Yasmine Ben Ismail": 1.34,
    "Aymen El Hadhri": 3.56
  },
  "Mohamed Yamoun Hamdi": {
    "Mohamed Amin Boukettaya": 0.19,
    "Elyes Cyril Boughedir": 0.19,
    "Yasmine Jedidi": 0.19,
    "Ahmed Said Mohamed": 2.86
  },
  "Aymen El Hadhri": {
    "Nabila Ben Zineb": 0.35,
    "Youssef Mohamed Bechir": 4.0,
    "Yassine Ben Knani": 3.56,
    "Mourad Kochkar": 0.35
  },
  "Mourad Kochkar": {
    "Mimouna Baya Chaaben": 0.88,
    "Arij Aouina": 1.37,
    "Aymen El Hadhri": 0.35,
    "Khammassi Nour": 0.35,
    "Yasmine Ben Ismail": 0.88,
    "El Fedi Zairi": 1.24,
    "Rania Ben Moussa": 0.15
  },
  "Abdelkarim Elhamdi": {
    "Mohamed Amin Boukettaya": 0.19,
    "Elyes Cyril Boughedir": 0.19,
    "Nabila Ben Zineb": 2.17,
    "Ben Abda Iskander": 0.12,
    "Mohamed Amine Neffati": 1.33,
    "Mohamed Bettaieb Marouen": 1.33
  },
  "Ben Abda Iskander": {
    "Arij Aouina": 2.77,
    "Nour Chouchane": 0.2,
    "Youssef Mohamed Bechir": 2.81,
    "Abdelkarim Elhamdi": 0.12
  },
  "Mohamed Amine Zekri": {
    "Nabila Ben Zineb": 1.37,
    "Mimouna Baya Chaaben": 0.93,
    "Nour Chouchane": 0.67,
    "Mohamed Amine Neffati": 2.29
  },
  "El Fedi Zairi": {
    "Nour Chouchane": 0.3,
    "Youssef Mohamed Bechir": 2.81,
    "Mourad Kochkar": 1.24,
    "Rania Ben Moussa": 0.81
  },
  "Rania Ben Moussa": {
    "Mimouna Baya Chaaben": 1.34,
    "Mourad Kochkar": 0.15,
    "El Fedi Zairi": 0.81,
    "Yasmine Ben Ismail": 1.34
  },
  "Aya Hachana": {
    "Arij Aouina": 3.26,
    "Mohamed Aziz Souissi": 5.29,
    "Mohamed Amine Neffati": 0.2,
    "Khammassi Nour": 1.96
  },
  "Mohamed Amine Neffati": {
    "Abdelkarim Elhamdi": 1.33,
    "Mohamed Amine Zekri": 2.29,
    "Aya Hachana": 0.2,
    "Mohamed Bettaieb Marouen": 0.2
  },
  "Abidi Fares": {
    "Yasmine Jedidi": 2.15,
    "Nour Chouchane": 0.2,
    "Yasmine Ben Ismail": 1.93
  },
  "Yasmine Ben Ismail": {
    "Emna Barbouch": 0.3,
    "Ahmed Said Mohamed": 0.24,
    "Arij Aouina": 0.24,
    "Youssef Mohamed Bechir": 1.34,
    "Yassine Ben Knani": 1.34,
    "Mourad Kochkar": 0.88,
    "Rania Ben Moussa": 1.34,
    "Abidi Fares": 1.93
  },
  "Mohamed Aymen Hassini": {
    "Elyes Cyril Boughedir": 0.19,
    "Mahdi Soudani": 0.02,
    "Yasmine Jedidi": 0.19
  },
  "Khammassi Nour": {
    "Nabila Ben Zineb": 0.35,
    "Nour Chouchane": 0.56,
    "Mourad Kochkar": 0.35,
    "Aya Hachana": 1.96
  },
  "Mohamed Bettaieb Marouen": {
    "Emna Barbouch": 1.33,
    "Ahmed Said Mohamed": 3.26,
    "Abdelkarim Elhamdi": 1.33,
    "Mohamed Amine Neffati": 0.2
  }
}

students = list(distance_dict.keys())

def create_graph(dist_dict):
    G = nx.Graph()
    for i in dist_dict:
        for j in dist_dict[i]:
            if i != j:
                G.add_edge(i, j, weight=dist_dict[i][j])
    return G

G = create_graph(distance_dict)

# Positions fixed for consistent graph display
pos = nx.spring_layout(G, seed=42)

# Session state
if 'role' not in st.session_state:
    st.session_state.role = None
if 'requests' not in st.session_state:
    st.session_state.requests = {}
if 'accepted' not in st.session_state:
    st.session_state.accepted = {}
if 'declined' not in st.session_state:
    st.session_state.declined = {}

st.title("🚗 SMU Carpooling App")

current_user = st.selectbox("Select your name:", students)

if "role" not in st.session_state or st.session_state.role is None:
    st.session_state.role = st.selectbox("Choose your role:", ["Driver", "Passenger"], index=0)

random.seed(42)
drivers = random.sample([s for s in students if s != current_user], min(7, len(students)-1))

# --------- GRAPH 1: everyone, 3 closest edges each ---------
st.markdown("### 🌐 All Students: Each Connected to 3 Nearest Neighbors")
fig1, ax1 = plt.subplots(figsize=(10, 8))
nx.draw(G, pos, with_labels=True, node_size=500, font_size=8, ax=ax1)
edge_labels = {(u, v): f"{d['weight']:.1f} km" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1, font_size=7)
st.pyplot(fig1)

# --------- GRAPH 2: driver + 3 nearest neighbors ---------
st.markdown("### 🚘 Visualize Any Driver's Nearby Passengers")
selected_driver = st.selectbox("Select driver to visualize:", drivers)
fig2, ax2 = plt.subplots(figsize=(10, 8))
shortest_graph = nx.Graph()
dists = distance_dict[selected_driver]
nearest = sorted(dists.items(), key=lambda x: x[1])[:4]
for p, _ in nearest:
    if p != selected_driver:
        path = nx.shortest_path(G, source=selected_driver, target=p, weight='weight')
        nx.add_path(shortest_graph, path)

colors = ['red' if n == selected_driver else 'green' for n in shortest_graph.nodes()]
nx.draw(shortest_graph, pos, with_labels=True, node_size=500, font_size=8, ax=ax2, node_color=colors)
edge_labels2 = {(u, v): f"{G[u][v]['weight']:.1f} km" for u, v in shortest_graph.edges() if G.has_edge(u, v)}
nx.draw_networkx_edge_labels(shortest_graph, pos, edge_labels=edge_labels2, ax=ax2, font_size=7)
ax2.set_title("Red = Driver | Green = Nearby Passengers")
st.pyplot(fig2)

# --------- INTERACTIVE: Passenger request -> driver accept/decline ---------
if st.session_state.role == "Passenger":
    available_drivers = [d for d in drivers if d != current_user]
    selected_driver = st.selectbox("Send carpool request to:", available_drivers)
    if st.button("Send Request"):
        st.session_state.requests.setdefault(selected_driver, []).append(current_user)
        st.success(f"Request sent to {selected_driver}")

elif st.session_state.role == "Driver":
    st.markdown(f"### 📥 Carpool Requests for Driver **{current_user}**")
    requests = st.session_state.requests.get(current_user, [])
    if requests:
        for passenger in requests:
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                st.write(f"Passenger: **{passenger}**")
            with col2:
                if st.button(f"✅ Accept {passenger}", key=f"acc_{passenger}"):
                    st.session_state.accepted.setdefault(current_user, []).append(passenger)
                    st.success(f"Accepted {passenger}")
            with col3:
                if st.button(f"❌ Decline {passenger}", key=f"dec_{passenger}"):
                    st.session_state.declined.setdefault(current_user, []).append(passenger)
                    st.warning(f"Declined {passenger}")
    else:
        st.info("No requests yet.")

    # --------- GRAPH 3: accepted passengers only ---------
    if current_user in st.session_state.accepted and st.session_state.accepted[current_user]:
        st.markdown("### 🗺️ Confirmed Carpool Group")
        fig3, ax3 = plt.subplots(figsize=(10, 8))
        final_graph = nx.Graph()
        for p in st.session_state.accepted[current_user]:
            path = nx.shortest_path(G, source=current_user, target=p, weight='weight')
            nx.add_path(final_graph, path)
        color_map = ['red' if n == current_user else 'green' for n in final_graph.nodes()]
        nx.draw(final_graph, pos, with_labels=True, node_size=500, font_size=8, ax=ax3, node_color=color_map)
        edge_labels3 = {(u, v): f"{G[u][v]['weight']:.1f} km" for u, v in final_graph.edges() if G.has_edge(u, v)}
        nx.draw_networkx_edge_labels(final_graph, pos, edge_labels=edge_labels3, ax=ax3, font_size=7)
        ax3.set_title("Red = Driver | Green = Accepted Passengers")
        st.pyplot(fig3)

st.markdown("---")
st.caption("SMU Carpooling App | 3 Graph Views + Accept/Decline Logic")
