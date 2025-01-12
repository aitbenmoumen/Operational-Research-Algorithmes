import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import tkinter as tk 
from tkinter import ttk
from tkinter import Label, Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ModernDarkTheme:
    # Colors
    BG_COLOR = "#1e1e1e"  # Dark background
    SECONDARY_BG = "#252526"  # Slightly lighter background
    TEXT_COLOR = "#ffffff"  # White text
    SECONDARY_TEXT = "#cccccc"  # Slightly dimmed text
    ACCENT_COLOR = "#007acc"  # Blue accent
    ACCENT_HOVER = "#0098ff"  # Lighter blue for hover
    ERROR_COLOR = "#f44336"  # Error red
    SUCCESS_COLOR = "#4caf50"  # Success green
    
    # Fonts
    MAIN_FONT = ("Segoe UI", 12)
    TITLE_FONT = ("Segoe UI", 24, "bold")
    SUBTITLE_FONT = ("Segoe UI", 14)
    
    
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


# Theme Configuration Class


# [Your existing algorithm functions remain unchanged: generate_random_graph, bfs, ford_fulkerson, find_min_cut, draw_graph_with_cut]

def display_ford_fulkerson_graph():
    def on_submit():
        try:
            # Clear previous graph
            nonlocal canvas_widget
            if canvas_widget:
                canvas_widget.destroy()

            # Get and validate input
            vertices = int(num_vertices.get())
            source = int(source_entry.get())
            sink = int(target_entry.get())

            # Validation
            if vertices <= 1:
                raise ValueError("Nombre des sommet doit etre > 1.")
            if source < 0 or source >= vertices:
                raise ValueError("Source must be a valid vertex index.")
            if sink < 0 or sink >= vertices:
                raise ValueError("Target must be a valid vertex index.")
            if source == sink:
                raise ValueError("Source and target cannot be the same.")

            # Generate graph and run algorithm
            G = generate_random_graph(vertices)
            capacity = [[0] * vertices for _ in range(vertices)]
            for u, v, data in G.edges(data=True):
                capacity[u][v] = data['capacity']

            max_flow, flow = ford_fulkerson(capacity, source, sink)
            min_cut = find_min_cut(capacity, flow, source)

            # Create styled visualization
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor(ModernDarkTheme.BG_COLOR)
            ax.set_facecolor(ModernDarkTheme.SECONDARY_BG)
            
            pos = nx.spring_layout(G)
            edges = G.edges()
            edge_colors = ['#ff4444' if min_cut[u] and not min_cut[v] else '#666666' for u, v in edges]
            node_colors = ['#4CAF50' if min_cut[u] else '#2196F3' for u in G.nodes()]
            
            nx.draw(G, pos, with_labels=True, 
                   node_color=node_colors,
                   edge_color=edge_colors,
                   node_size=500,
                   font_size=10,
                   font_weight='bold',
                   font_color='white',
                   ax=ax)
            
            # Add timestamp to the graph
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            ax.set_title(f"Max Flow: {max_flow}\n{current_time}", 
                        fontsize=14,
                        color=ModernDarkTheme.TEXT_COLOR,
                        pad=20)

            # Update canvas
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        except ValueError as e:
            error_label.config(text=f"Error: {e}", fg=ModernDarkTheme.ERROR_COLOR)

    # Window Setup
    window = tk.Toplevel()
    window.title("Ford-Fulkerson Algorithm Visualization")
    window.geometry("1000x800")
    window.configure(bg=ModernDarkTheme.BG_COLOR)

    # Style Configuration
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Modern.TButton",
        background=ModernDarkTheme.ACCENT_COLOR,
        foreground=ModernDarkTheme.TEXT_COLOR,
        font=ModernDarkTheme.MAIN_FONT,
        padding=(20, 10),
        borderwidth=0
    )
    style.map(
        "Modern.TButton",
        background=[("active", ModernDarkTheme.ACCENT_HOVER)],
        foreground=[("active", ModernDarkTheme.TEXT_COLOR)]
    )

    # Title Section
    title_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    title_frame.pack(fill="x", pady=20)
    
    Label(title_frame,
          text="Ford-Fulkerson Algorithm",
          font=ModernDarkTheme.TITLE_FONT,
          bg=ModernDarkTheme.BG_COLOR,
          fg=ModernDarkTheme.TEXT_COLOR).pack()
    
    Label(title_frame,
          text="Problemes de flots",
          font=ModernDarkTheme.SUBTITLE_FONT,
          bg=ModernDarkTheme.BG_COLOR,
          fg=ModernDarkTheme.SECONDARY_TEXT).pack()

    # Input Section with styling
    input_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    input_frame.pack(fill="x", padx=40, pady=20)

    def create_input_field(parent, label_text):
        frame = tk.Frame(parent, bg=ModernDarkTheme.BG_COLOR)
        frame.pack(fill="x", pady=5)
        Label(frame,
              text=label_text,
              font=ModernDarkTheme.MAIN_FONT,
              bg=ModernDarkTheme.BG_COLOR,
              fg=ModernDarkTheme.TEXT_COLOR).pack(side="left")
        entry = Entry(frame,
                     font=ModernDarkTheme.MAIN_FONT,
                     bg=ModernDarkTheme.SECONDARY_BG,
                     fg=ModernDarkTheme.TEXT_COLOR,
                     insertbackground=ModernDarkTheme.TEXT_COLOR,
                     relief="flat",
                     width=10)
        entry.pack(side="left", padx=10)
        return entry

    # Create input fields
    num_vertices = create_input_field(input_frame, "Nombre de sommets :")
    source_entry = create_input_field(input_frame, "Sommet source:")
    target_entry = create_input_field(input_frame, "Sommet cible:")

    # Button Section
    button_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    button_frame.pack(pady=10)
    
    submit_btn = ttk.Button(button_frame,
                           text="Generate Graph",
                           style="Modern.TButton",
                           command=on_submit)
    submit_btn.pack(side="left", padx=5)
    
    close_btn = ttk.Button(button_frame,
                          text="Close",
                          style="Modern.TButton",
                          command=window.destroy)
    close_btn.pack(side="left", padx=5)

    # Error Label
    error_label = Label(window,
                       text="",
                       font=ModernDarkTheme.MAIN_FONT,
                       bg=ModernDarkTheme.BG_COLOR,
                       fg=ModernDarkTheme.ERROR_COLOR)
    error_label.pack(pady=10)

    # Graph Frame
    graph_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas_widget = None

    # Center window on screen
    window_width = 1000
    window_height = 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Add user info and timestamp
    footer_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    footer_frame.pack(fill="x", pady=5)
    
    Label(footer_frame,
          text=f"User: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')} - aitbenmoumen",
          font=("Segoe UI", 8),
          bg=ModernDarkTheme.BG_COLOR,
          fg=ModernDarkTheme.SECONDARY_TEXT).pack(side="right", padx=10)

    