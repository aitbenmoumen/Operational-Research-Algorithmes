import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import heapq

def generate_graph(num_nodes, max_weight=100):
    graph = nx.Graph()
    nodes = [f"X{i+1}" for i in range(num_nodes)]
    graph.add_nodes_from(nodes)
    
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, max_weight)
            graph.add_edge(nodes[i], nodes[j], weight=weight)
    return graph

def dijkstra(graph, start_node):
    priority_queue = [(0, start_node)]
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0
    paths = {node: [] for node in graph.nodes()}
    paths[start_node] = [start_node]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        
        visited.add(current_node)
        
        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + edge_weight
            
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (new_distance, neighbor))
    
    return distances, paths

def plot_graph(fig, graph, paths=None, start_node=None, title="Graphe Initial"):
    # Clear the figure and create new axes
    fig.clf()
    ax = fig.add_subplot(111)
    
    # Configure the plot appearance
    ax.set_facecolor('#303030')
    fig.patch.set_facecolor('#303030')
    
    # Calculate layout
    pos = nx.spring_layout(graph, seed=42)
    
    # Determine edges in shortest paths
    edges_in_paths = []
    if paths:
        edges_in_paths = [(u, v) for path in paths.values() for u, v in zip(path, path[1:])]
    
    # Draw edges
    nx.draw_networkx_edges(
        graph, pos, ax=ax,
        edge_color=['#3F51B5' if (u, v) in edges_in_paths or (v, u) in edges_in_paths else '#666666' for u, v in graph.edges()],
        width=[2 if (u, v) in edges_in_paths or (v, u) in edges_in_paths else 1 for u, v in graph.edges()]
    )
    
    # Draw nodes
    node_colors = ['#4CAF50' if n == start_node else '#2196F3' for n in graph.nodes()] if start_node else ['#2196F3' for n in graph.nodes()]
    nx.draw_networkx_nodes(
        graph, pos, ax=ax,
        node_color=node_colors,
        node_size=500
    )
    
    # Draw labels
    nx.draw_networkx_labels(
        graph, pos, ax=ax,
        font_size=10,
        font_weight='bold',
        font_color='white'
    )
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(
        graph, pos, ax=ax,
        edge_labels=edge_labels,
        font_size=8,
        font_color='white'
    )
    
    ax.set_title(title, color='white', pad=20, fontsize=14)
    ax.set_axis_off()
    fig.tight_layout()
    
def display_paths_table(distances, paths):
    result = ""
    result += "Plus Courts Chemins depuis le Nœud de Départ:\n\n"
    
    for dest, distance in sorted(distances.items()):
        path_str = ' → '.join(paths[dest])
        result += f"Vers {dest}: Distance = {distance}\n"
        result += f"Chemin: {path_str}\n\n"
    
    return result

def display_dijkstra_graph():
    window = tk.Toplevel()
    window.title("Algorithme de Dijkstra - Plus Courts Chemins")
    window.geometry("1000x800")
    window.configure(bg="#303030")
    
    # Initialize graph with default values
    default_nodes = 5
    initial_graph = generate_graph(default_nodes)
    
    # Style configuration
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Custom.TButton",
        background="#3F51B5",
        foreground="white",
        font=("Calibri", 12, "bold"),
        padding=(20, 10),
        borderwidth=0,
    )
    style.map(
        "Custom.TButton",
        background=[("active", "#5C6BC0")],
        foreground=[("active", "white")],
    )
    
    # Create main container
    container = tk.Frame(window, bg="#303030")
    container.pack(expand=True, fill="both", padx=40, pady=20)
    
    # Create frames
    title_frame = tk.Frame(container, bg="#303030")
    title_frame.pack(fill="x", pady=(0, 20))
    
    content_frame = tk.Frame(container, bg="#303030")
    content_frame.pack(fill="both", expand=True)
    
    # Graph frame (left side)
    graph_frame = tk.Frame(content_frame, bg="#303030")
    graph_frame.pack(side="left", fill="both", expand=True)
    
    # Create figure and canvas
    fig = Figure(figsize=(6, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Results frame (right side)
    results_frame = tk.Frame(content_frame, bg="#303030")
    results_frame.pack(side="right", fill="both", padx=10)
    
    # Input frame
    input_frame = tk.Frame(container, bg="#303030")
    input_frame.pack(fill="x", pady=10)
    
    # Add input fields
    nodes_label = tk.Label(input_frame, text="Nombre de Nœuds:", bg="#303030", fg="white")
    nodes_label.grid(row=0, column=0, padx=5)
    
    num_nodes_entry = tk.Entry(input_frame, bg="white", fg="black")
    num_nodes_entry.insert(0, str(default_nodes))
    num_nodes_entry.grid(row=0, column=1, padx=5)
    
    start_label = tk.Label(input_frame, text="Nœud de Départ:", bg="#303030", fg="white")
    start_label.grid(row=0, column=2, padx=5)
    
    start_node_entry = tk.Entry(input_frame, bg="white", fg="black")
    start_node_entry.insert(0, "X1")
    start_node_entry.grid(row=0, column=3, padx=5)
    
    result_text = tk.Text(results_frame, bg="#404040", fg="white", height=20, width=40)
    result_text.pack(fill="both", expand=True)
    
    def update_graph():
        try:
            num_nodes = int(num_nodes_entry.get())
            start_node = start_node_entry.get().strip()
            
            if num_nodes <= 0:
                raise ValueError("Le nombre de nœuds doit être positif")
            
            if not start_node.startswith('X') or not start_node[1:].isdigit() or int(start_node[1:]) > num_nodes:
                raise ValueError(f"Le nœud de départ doit être entre X1 et X{num_nodes}")
            
            graph = generate_graph(num_nodes)
            distances, paths = dijkstra(graph, start_node)
            
            # Update the plot
            plot_graph(fig, graph, paths, start_node, f"Plus Courts Chemins depuis {start_node}")
            canvas.draw()
            
            # Update results
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, display_paths_table(distances, paths))
            
        except ValueError as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Erreur: {str(e)}")
    
    # Add button
    update_button = ttk.Button(container, text="Générer", command=update_graph, style="Custom.TButton")
    update_button.pack(pady=10)
    
    # Initial graph display
    plot_graph(fig, initial_graph)
    canvas.draw()
    
    window.mainloop()