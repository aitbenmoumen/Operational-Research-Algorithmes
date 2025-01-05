import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import heapq

# Function to generate an undirected graph with random weights
def generate_graph(num_nodes, max_weight=100):
    graph = nx.Graph()
    nodes = [f"X{i+1}" for i in range(num_nodes)]
    graph.add_nodes_from(nodes)

    # Randomly add edges with weights between nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = random.randint(1, max_weight)
            graph.add_edge(nodes[i], nodes[j], weight=weight)

    return graph

# Standard Dijkstra's algorithm function
def dijkstra(graph, start_node):
    priority_queue = [(0, start_node)]  # (distance, node)
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0
    paths = {node: [] for node in graph.nodes()}
    paths[start_node] = [start_node]
    visited = set()

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if already visited
        if current_node in visited:
            continue

        # Mark the node as visited
        visited.add(current_node)

        # Check all neighbors of the current node
        for neighbor in graph.neighbors(current_node):
            edge_weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + edge_weight

            # Update distances and path if a shorter path is found
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                paths[neighbor] = paths[current_node] + [neighbor]
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, paths

# Function to plot the graph with shortest paths highlighted
def plot_graph(fig, graph, paths, start_node, title):
    pos = nx.spring_layout(graph, seed=42)

    # Identify edges in the shortest paths and color them red
    edges_in_paths = [(u, v) for path in paths.values() for u, v in zip(path, path[1:])]
    edge_colors = ['red' if (u, v) in edges_in_paths or (v, u) in edges_in_paths else 'black' for u, v in graph.edges()]

    node_colors = ['lightblue' if n == start_node else 'lightgrey' for n in graph.nodes()]

    # Clear figure and set new subplot
    fig.clear()
    ax = fig.add_subplot(111)

    # Draw the graph
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
            node_size=500, font_size=10, ax=ax)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): f"{d['weight']}" for u, v, d in graph.edges(data=True)}, ax=ax)

    ax.set_title(title)
    fig.tight_layout()

# Function to display the shortest paths and their weights in the GUI
def display_paths_table(distances, paths):
    result_text = "Shortest Paths from Start Node:\n"
    result_text += f"{'Destination':<12}{'Path Weight':<10}{'Path'}\n"
    result_text += "="*40 + "\n"
    
    for dest, distance in distances.items():
        result_text += f"{dest:<12}{distance:<10}{' -> '.join(paths[dest])}\n"

    return result_text

# Function to run the Dijkstra algorithm and display the results
def display_dijkstra_graph():
    window = tk.Toplevel()
    window.title("Dijkstra Algorithm - Shortest Paths")

    def generate_and_run():
        try:
            num_nodes = int(num_nodes_entry.get())
            start_node = start_node_entry.get().strip()

            if start_node not in [f"X{i+1}" for i in range(num_nodes)]:
                result_label.config(text="Invalid starting node.")
                return

            graph = generate_graph(num_nodes)
            distances, paths = dijkstra(graph, start_node)

            # Plot the graph with shortest paths
            plot_graph(fig, graph, paths, start_node, title=f"Shortest Paths from {start_node}")
            canvas.draw()

            # Display the paths and weights in the result label
            result_text = display_paths_table(distances, paths)
            result_label.config(text=result_text)

        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")

    # Input field for number of nodes
    tk.Label(window, text="Number of Nodes:").pack(pady=5)
    num_nodes_entry = tk.Entry(window)
    num_nodes_entry.pack(pady=5)

    # Input field for the start node
    tk.Label(window, text="Start Node (e.g., X1 to Xn):").pack(pady=5)
    start_node_entry = tk.Entry(window)
    start_node_entry.pack(pady=5)

    # Submit button
    submit_btn = ttk.Button(window, text="Submit", command=generate_and_run)
    submit_btn.pack(pady=10)

    # Label to display the results with smaller font
    result_label = tk.Label(window, text="", font=("Arial", 8), justify="left", anchor="w")
    result_label.pack(pady=10, fill=tk.BOTH, expand=True)

    # Initialize figure and canvas
    fig = plt.Figure(figsize=(6, 5))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Adjust the window size automatically with the canvas
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Close button
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)