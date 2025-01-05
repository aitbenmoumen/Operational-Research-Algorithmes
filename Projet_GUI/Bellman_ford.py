import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import string
import time

def generate_vertex_labels(num_vertices):
    return [chr(ord('A') + i) for i in range(num_vertices)]  # Use A, B, C... for labels

def generate_directed_graph(n):
    G = nx.DiGraph()
    vertices = generate_vertex_labels(n)
    
    # Add nodes
    for vertex in vertices:
        G.add_node(vertex)

    # Add edges with random weights
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.3:  # 30% chance of edge creation
                weight = random.randint(1, 100)
                G.add_edge(vertices[i], vertices[j], weight=weight)

    return G

def display_graph(G, path=None):
    plt.clf()  # Clear the current figure
    fig = plt.Figure(figsize=(8, 6))  # Increased figure size for better visibility
    ax = fig.add_subplot(111)
    
    # Use a circular layout with more spacing
    pos = nx.circular_layout(G, scale=0.9)  # Increased scale for better spacing
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=1000,  # Increased node size
                          ax=ax)
    
    # Draw node labels with increased font size
    nx.draw_networkx_labels(G, pos, 
                           font_size=12,  # Increased font size
                           font_weight='bold',
                           font_family='sans-serif')
    
    # Draw edges
    edges = G.edges()
    nx.draw_networkx_edges(G, pos, 
                          edgelist=edges,
                          arrows=True,
                          edge_color='gray',
                          width=1,
                          ax=ax)
    
    # Draw edge weights with better positioning
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, 
                                edge_labels=edge_labels,
                                font_size=10,  # Increased font size
                                label_pos=0.5)  # Center the label on the edge
    
    # Highlight the shortest path if provided
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(G, pos,
                             edgelist=path_edges,
                             edge_color='red',
                             width=2,
                             arrows=True,
                             ax=ax)
    
    # Set axis limits to center the graph
    ax.set_axis_off()
    ax.margins(0.2)  # Add margins around the graph
    fig.tight_layout()
    
    return fig

def bellman_ford_graph(G, source, target):
    try:
        distance = nx.single_source_bellman_ford_path_length(G, source)
        path = nx.single_source_bellman_ford_path(G, source)[target]
        return path, distance[target]
    except nx.NetworkXNoPath:
        return None, None

def display_bellman_ford_graph():
    window = tk.Toplevel()
    window.title("Bellman-Ford Algorithm - Shortest Path")
    window.geometry("1000x800")
    
    # Create a main frame to center the content
    main_frame = ttk.Frame(window)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
    def generate_graph():
        try:
            start_time = time.time()
            
            num_vertices = int(num_vertices_entry.get())
            if num_vertices < 2:
                result_label.config(text="Please enter at least 2 vertices")
                return
                
            G = generate_directed_graph(num_vertices)
            source = source_entry.get().strip().upper()  # Convert to uppercase
            target = target_entry.get().strip().upper()  # Convert to uppercase
            
            if source not in G.nodes or target not in G.nodes:
                result_label.config(text="Invalid source or target node. Use format 'A', 'B', etc.")
                return
            
            path, distance = bellman_ford_graph(G, source, target)
            end_time = time.time()
            
            if path:
                fig = display_graph(G, path)
                canvas.figure = fig
                canvas.draw()
                result_label.config(
                    text=f"Distance from {source} to {target}: {distance} | Execution Time: {end_time - start_time:.4f} seconds"
                )
            else:
                fig = display_graph(G)
                canvas.figure = fig
                canvas.draw()
                result_label.config(
                    text=f"No path exists from {source} to {target} | Execution Time: {end_time - start_time:.4f} seconds"
                )
                
        except ValueError:
            result_label.config(text="Please enter valid numeric values")

    # Input fields in a centered frame
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill='x', pady=10)

    tk.Label(input_frame, text="Number of Vertices:").pack(pady=5)
    num_vertices_entry = tk.Entry(input_frame, justify='center', width=30)
    num_vertices_entry.pack(pady=5)

    tk.Label(input_frame, text="Source Node (e.g., A):").pack(pady=5)
    source_entry = tk.Entry(input_frame, justify='center', width=30)
    source_entry.pack(pady=5)

    tk.Label(input_frame, text="Target Node (e.g., B):").pack(pady=5)
    target_entry = tk.Entry(input_frame, justify='center', width=30)
    target_entry.pack(pady=5)

    # Submit button
    submit_btn = ttk.Button(input_frame, text="Submit", command=generate_graph)
    submit_btn.pack(pady=10)

    # Result label
    result_label = tk.Label(main_frame, text="", font=("Arial", 10))
    result_label.pack(pady=10)

    # Canvas in a frame for centering
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.pack(expand=True, fill='both')
    
    fig = plt.Figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)

    # Close button
    close_btn = ttk.Button(main_frame, text="Close", command=window.destroy)
    close_btn.pack(pady=10)