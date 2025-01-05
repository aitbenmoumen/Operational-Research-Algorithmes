# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 14:01:19 2025

@author: aaitb
"""

import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


# Function to generate node labels (x0, x1, ..., xn)
def generer_etiquettes_sommets(nb_sommets):
    etiquettes = [f"x{i}" for i in range(nb_sommets)]
    return etiquettes

# Function to generate a random directed graph with weighted edges
def generer_graphe_oriente(n):
    G = nx.DiGraph()
    sommets = generer_etiquettes_sommets(n)
    
    for sommet in sommets:
        G.add_node(sommet, size=800)

    # Add edges with random weights
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                poids = random.randint(1, 100)
                G.add_edge(f"x{i}", f"x{j}", weight=poids)
            else:
                poids = random.randint(1, 100)
                G.add_edge(f"x{j}", f"x{i}", weight=poids)

    return G

# Function to display the graph
def afficher_graphe(G, chemin=None):
    pos = nx.spring_layout(G, seed=42)
    node_sizes = [G.nodes[node]['size'] for node in G]

    fig = plt.Figure(figsize=(6, 5))
    ax = fig.add_subplot(111)
    
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color="lightblue",
            font_weight="bold", arrows=True, ax=ax)
    
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    
    if chemin:
        edges = [(chemin[i], chemin[i + 1]) for i in range(len(chemin) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2, arrows=True, ax=ax)

    return fig

# Bellman-Ford algorithm for shortest path
def bellman_ford_graphe(G, source, target):
    try:
        distance = nx.single_source_bellman_ford_path_length(G, source)
        chemin = nx.single_source_bellman_ford_path(G, source)[target]
        return chemin, distance[target]
    except nx.NetworkXNoPath:
        return None, None

# Function to display Bellman-Ford graph visualization in Tkinter
def display_bellman_ford_graph():
    window = tk.Toplevel()
    window.title("Bellman-Ford Algorithm - Shortest Path")
    window.geometry("1100x800")  # Larger window size

    def generate_graph():
        try:
            # Read number of vertices and generate the graph
            num_vertices = int(num_vertices_entry.get())
            G = generer_graphe_oriente(num_vertices)
            
            # Get the source and target nodes, convert to lowercase to match node labels
            source = source_entry.get().lower()  # Convert input to lowercase
            target = target_entry.get().lower()  # Convert input to lowercase
            
            # Check if source and target nodes are in the graph
            if source not in G.nodes or target not in G.nodes:
                result_label.config(text="Invalid source or target node. Please enter valid nodes.")
                return
            
            # Apply Bellman-Ford algorithm
            chemin, distance = bellman_ford_graphe(G, source, target)
            
            # Display the graph with the shortest path in red
            fig = afficher_graphe(G, chemin)
            canvas.figure = fig  # Update the figure
            canvas.draw()
            
            if chemin:
                result_label.config(text=f"Distance from {source} to {target}: {distance}")
            else:
                result_label.config(text=f"No path from {source} to {target}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")


    # Input field for number of vertices
    tk.Label(window, text="Number of Vertices:").pack(pady=5)
    num_vertices_entry = tk.Entry(window)
    num_vertices_entry.pack(pady=5)

    # Input fields for source and target nodes
    tk.Label(window, text="Source Node (e.g., x0):").pack(pady=5)
    source_entry = tk.Entry(window)
    source_entry.pack(pady=5)

    tk.Label(window, text="Target Node (e.g., x1):").pack(pady=5)
    target_entry = tk.Entry(window)
    target_entry.pack(pady=5)

    # Submit button to generate the graph
    submit_btn = ttk.Button(window, text="Submit", command=generate_graph)
    submit_btn.pack(pady=10)

    # Label to display results
    result_label = tk.Label(window, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    # Initialize figure and canvas
    fig = plt.Figure(figsize=(6, 5))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Close button
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)
