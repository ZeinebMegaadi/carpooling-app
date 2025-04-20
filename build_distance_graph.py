import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random
from google.colab import files

# Upload the distance matrix file
uploaded = files.upload()

# Step 1: Read the distance matrix CSV file
file_name = "distance_matrix_km.csv"
df = pd.read_csv(file_name, index_col=0)

# Step 2: Create a graph
G = nx.Graph()

# Step 3: Add nodes (students)
for student in df.columns:
    G.add_node(student)

# Step 4: Add edges (distances) between students
for i in df.columns:
    for j in df.columns:
        if i != j:
            distance = df.loc[i, j]
            G.add_edge(i, j, weight=distance)

# Step 5: Visualize the graph with jitter to reduce overlap
pos = nx.spring_layout(G, seed=42)

# Add jitter to overlapping nodes
for key in pos:
    pos[key][0] += random.uniform(-0.02, 0.02)
    pos[key][1] += random.uniform(-0.02, 0.02)

plt.figure(figsize=(16, 10))
nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=9)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
plt.title("Carpool Distance Graph")
plt.axis('off')
plt.show()
