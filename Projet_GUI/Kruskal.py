import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import string
import time

# Function to generate node labels (A, B, ..., Z, AA, AB, ..., ZZ)
def generer_etiquettes_sommets(nb_sommets):
    alphabet = string.ascii_uppercase
    etiquettes = []
    for i in range(nb_sommets):
        etiquette = ""
        while i >= 0:
            etiquette = alphabet[i % 26] + etiquette
            i = i // 26 - 1
        etiquettes.append(etiquette)
    return etiquettes

# Function to generate a random graph with weighted edges
def generer_graphe(nb_sommets):
    sommets = generer_etiquettes_sommets(nb_sommets)
    aretes = []
    for i in range(nb_sommets):
        for j in range(i + 1, nb_sommets):
            poids = random.randint(1, 1000)  # Random weights between 1 and 1000
            aretes.append((sommets[i], sommets[j], poids))
    return sommets, aretes

# Kruskal's algorithm
def kruskal(sommets, aretes):
    aretes_triees = sorted(aretes, key=lambda x: x[2])
    parent = {s: s for s in sommets}
    rank = {s: 0 for s in sommets}
    
    def find(s):
        if parent[s] != s:
            parent[s] = find(parent[s])
        return parent[s]

    def union(s1, s2):
        root1 = find(s1)
        root2 = find(s2)
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    arbre_couvrant_min = []
    cout_total = 0

    for sommet_u, sommet_v, poids in aretes_triees:
        if find(sommet_u) != find(sommet_v):
            union(sommet_u, sommet_v)
            arbre_couvrant_min.append((sommet_u, sommet_v, poids))
            cout_total += poids
    return arbre_couvrant_min, cout_total

# Function to visualize the graph
def visualiser_graphe(fig, sommets, aretes, acm=None, titre="Graphe"):
    G = nx.Graph()
    for sommet_u, sommet_v, poids in aretes:
        G.add_edge(sommet_u, sommet_v, weight=poids)

    pos = nx.spring_layout(G, seed=42)

    # Clear the figure
    fig.clear()
    ax = fig.add_subplot(111)

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold', edge_color='gray', ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f'{poids}' for u, v, poids in aretes}, ax=ax)
    
    if acm:
        acm_edges = [(u, v) for u, v, _ in acm]
        nx.draw_networkx_edges(G, pos, edgelist=acm_edges, width=3, edge_color='blue', ax=ax)
    
    ax.set_title(titre)
    fig.tight_layout()

# Function to display Kruskal algorithm visualization in Tkinter
def display_kruskal_graph():
    window = tk.Toplevel()
    window.title("Kruskal Algorithm - Minimum Spanning Tree")
    window.geometry("1000x800")  # Increase window size
    
    # Configure window to adjust dynamically
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    def generate_graph():
        try:
            num_vertices = int(num_vertices_entry.get())
            sommets, aretes = generer_graphe(num_vertices)
            
            start_time = time.time()
            acm, cout_total = kruskal(sommets, aretes)
            end_time = time.time()

            # Visualize the graph with MST
            visualiser_graphe(fig, sommets, aretes, acm=acm, titre=f"Minimum Spanning Tree (Cost: {cout_total})")
            canvas.draw()
            
            result_label.config(text=f"Total Cost: {cout_total} | Execution Time: {end_time - start_time:.4f} seconds")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    # Input field for number of vertices
    tk.Label(window, text="Number of Vertices:").pack(pady=5)
    num_vertices_entry = tk.Entry(window)
    num_vertices_entry.pack(pady=5)

    # Submit button
    submit_btn = ttk.Button(window, text="Submit", command=generate_graph)
    submit_btn.pack(pady=10)

    # Label to display results (smaller font size)
    result_label = tk.Label(window, text="", font=("Arial", 10))  # Smaller font size
    result_label.pack(pady=10, fill=tk.BOTH, expand=True)

    # Initialize figure and canvas
    fig = plt.Figure(figsize=(6, 5))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Close button
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)
