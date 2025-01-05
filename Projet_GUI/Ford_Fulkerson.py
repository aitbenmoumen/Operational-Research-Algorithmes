import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import tkinter as tk 
from tkinter import ttk
from tkinter import Label, Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Functions for the Ford-Fulkerson algorithm
def generate_random_graph(num_vertices, max_capacity=10):
    G = nx.DiGraph()  # Directed graph
    for i in range(num_vertices):
        for j in range(num_vertices):
            if i != j:
                capacity = random.randint(1, max_capacity)
                G.add_edge(i, j, capacity=capacity)
    return G

def bfs(capacity, flow, source, sink):
    parent = [-1] * len(capacity)
    parent[source] = -2
    queue = deque([(source, float('inf'))])
    while queue:
        u, min_cap = queue.popleft()
        for v in range(len(capacity)):
            if parent[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                parent[v] = u
                new_flow = min(min_cap, capacity[u][v] - flow[u][v])
                if v == sink:
                    return new_flow, parent
                queue.append((v, new_flow))
    return 0, parent

def ford_fulkerson(capacity, source, sink):
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    max_flow = 0
    while True:
        path_flow, parent = bfs(capacity, flow, source, sink)
        if path_flow == 0:
            break
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = u
    return max_flow, flow

def find_min_cut(capacity, flow, source):
    visited = [False] * len(capacity)
    queue = deque([source])
    visited[source] = True
    while queue:
        u = queue.popleft()
        for v in range(len(capacity)):
            if capacity[u][v] - flow[u][v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)
    return visited

def draw_graph_with_cut(G, min_cut):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))
    edges = G.edges()
    edge_colors = ['red' if min_cut[u] and not min_cut[v] else 'black' for u, v in edges]
    node_colors = ['green' if min_cut[u] else 'blue' for u in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=500, font_size=16, font_weight='bold')
    plt.show()

# Main function for GUI integration
def display_ford_fulkerson_graph():
    def on_submit():
        try:
            # Clear the previous graph, if any
            nonlocal canvas_widget
            if canvas_widget:
                canvas_widget.destroy()

            # Fetch and validate user input
            vertices = int(num_vertices.get())
            source = int(source_entry.get())
            sink = int(target_entry.get())

            if vertices <= 1:
                raise ValueError("Number of vertices must be greater than 1.")
            if source < 0 or source >= vertices:
                raise ValueError("Source must be a valid vertex index.")
            if sink < 0 or sink >= vertices:
                raise ValueError("Target must be a valid vertex index.")
            if source == sink:
                raise ValueError("Source and target cannot be the same.")

            # Generate graph and run algorithms
            G = generate_random_graph(vertices)
            capacity = [[0] * vertices for _ in range(vertices)]
            for u, v, data in G.edges(data=True):
                capacity[u][v] = data['capacity']

            max_flow, flow = ford_fulkerson(capacity, source, sink)
            min_cut = find_min_cut(capacity, flow, source)

            # Create graph visualization
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(G)
            edges = G.edges()
            edge_colors = ['red' if min_cut[u] and not min_cut[v] else 'black' for u, v in edges]
            node_colors = ['green' if min_cut[u] else 'blue' for u in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                    node_size=500, font_size=10, font_weight='bold', ax=ax)
            ax.set_title(f"Max Flow: {max_flow}", fontsize=14)

            # Embed figure in Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

        except ValueError as e:
            error_label.config(text=f"Error: {e}", fg="red")

    # Create a new window
    window = tk.Toplevel()
    window.title("Ford-Fulkerson Algorithm - Graph Visualization")
    window.geometry("800x600")

    canvas_widget = None  # Variable to track the current graph widget

    # Input prompt for vertices
    frame1 = tk.Frame(window)
    frame1.pack(pady=5)
    Label(frame1, text="Enter the number of vertices:").pack(side='left')
    num_vertices = Entry(frame1, bd=5)
    num_vertices.pack(side='left')

    # Input prompt for source
    frame2 = tk.Frame(window)
    frame2.pack(pady=5)
    Label(frame2, text="Enter the source vertex:").pack(side='left')
    source_entry = Entry(frame2, bd=5)
    source_entry.pack(side='left')

    # Input prompt for target
    frame3 = tk.Frame(window)
    frame3.pack(pady=5)
    Label(frame3, text="Enter the target vertex:").pack(side='left')
    target_entry = Entry(frame3, bd=5)
    target_entry.pack(side='left')

    # Submit button
    submit_btn = ttk.Button(window, text="Submit", command=on_submit)
    submit_btn.pack(pady=10)

    # Error label
    error_label = Label(window, text="", fg="red")
    error_label.pack()

    # Close button
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)