import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import time

def generate_vertex_labels(num_vertices):
    return [chr(ord('A') + i) for i in range(num_vertices)]

def generate_directed_graph(n):
    G = nx.DiGraph()
    vertices = generate_vertex_labels(n)
    
    for vertex in vertices:
        G.add_node(vertex)

    for i in range(n):
        for j in range(n):
            if i != j and random.random() < 0.3:
                weight = random.randint(1, 100)
                G.add_edge(vertices[i], vertices[j], weight=weight)

    return G

def display_graph(fig, G, path=None, title="Graphe Initial"):
    fig.clf()
    ax = fig.add_subplot(111)
    
    # Configure colors and style
    ax.set_facecolor('#303030')
    fig.patch.set_facecolor('#303030')
    
    # Use circular layout for better edge visibility
    pos = nx.circular_layout(G, scale=0.9)
    
    # Draw edges
    edges = G.edges()
    nx.draw_networkx_edges(
        G, pos,
        edge_color=['#666666'],
        width=1,
        arrows=True,
        arrowsize=20,
        ax=ax
    )
    
    # Highlight path if provided
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(
            G, pos,
            edgelist=path_edges,
            edge_color='#3F51B5',
            width=2,
            arrows=True,
            arrowsize=20,
            ax=ax
        )
    
    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_color='#2196F3',
        node_size=1000,
        ax=ax
    )
    
    # Draw node labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold',
        font_color='white'
    )
    
    # Draw edge weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=10,
        font_color='white',
        bbox=dict(facecolor='#303030', edgecolor='none', alpha=0.7)
    )
    
    ax.set_title(title, color='white', pad=20, fontsize=14)
    ax.set_axis_off()
    fig.tight_layout()

def bellman_ford_graph(G, source, target):
    try:
        distance = nx.single_source_bellman_ford_path_length(G, source)
        path = nx.single_source_bellman_ford_path(G, source)[target]
        return path, distance[target]
    except nx.NetworkXNoPath:
        return None, None

def display_bellman_ford_graph():
    window = tk.Toplevel()
    window.title("Algorithme de Bellman-Ford - Plus Courts Chemins")
    window.geometry("1000x800")
    window.configure(bg="#303030")
    
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
    
    # Title section
    title_frame = tk.Frame(container, bg="#303030")
    title_frame.pack(fill="x", pady=(0, 20))
    
    title_label = tk.Label(
        title_frame,
        text="Algorithme de Bellman-Ford",
        font=("Calibri", 24, "bold"),
        bg="#303030",
        fg="#F0F8FF",
    )
    title_label.pack(pady=(0, 5))
    
    subtitle_label = tk.Label(
        title_frame,
        text="Plus Courts Chemins",
        font=("Calibri", 14),
        bg="#303030",
        fg="#AAAAAA",
    )
    subtitle_label.pack()
    
    # Input section
    input_frame = tk.Frame(container, bg="#303030")
    input_frame.pack(fill="x", pady=10)
    
    # Vertices input
    vertices_label = tk.Label(
        input_frame,
        text="Nombre de Sommets:",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF"
    )
    vertices_label.pack(pady=5)
    
    num_vertices_entry = tk.Entry(
        input_frame,
        font=("Calibri", 12),
        bg="#404040",
        fg="#F0F8FF",
        insertbackground="#F0F8FF",
        relief="flat",
        justify='center',
        width=30
    )
    num_vertices_entry.pack(pady=5)
    
    # Source node input
    source_label = tk.Label(
        input_frame,
        text="Sommet de Départ (ex: A):",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF"
    )
    source_label.pack(pady=5)
    
    source_entry = tk.Entry(
        input_frame,
        font=("Calibri", 12),
        bg="#404040",
        fg="#F0F8FF",
        insertbackground="#F0F8FF",
        relief="flat",
        justify='center',
        width=30
    )
    source_entry.pack(pady=5)
    
    # Target node input
    target_label = tk.Label(
        input_frame,
        text="Sommet d'Arrivée (ex: B):",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF"
    )
    target_label.pack(pady=5)
    
    target_entry = tk.Entry(
        input_frame,
        font=("Calibri", 12),
        bg="#404040",
        fg="#F0F8FF",
        insertbackground="#F0F8FF",
        relief="flat",
        justify='center',
        width=30
    )
    target_entry.pack(pady=5)
    
    # Result label
    result_label = tk.Label(
        container,
        text="",
        font=("Calibri", 12),
        bg="#303030",
        fg="#4CAF50",
        wraplength=800
    )
    result_label.pack(pady=10)
    
    # Graph display
    graph_frame = tk.Frame(container, bg="#303030")
    graph_frame.pack(fill="both", expand=True)
    
    fig = Figure(figsize=(8, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True, padx=10, pady=10)
    
    def generate_graph():
        try:
            start_time = time.time()
            
            num_vertices = int(num_vertices_entry.get())
            if num_vertices < 2:
                result_label.config(text="Veuillez entrer au moins 2 sommets", fg="#FF5252")
                return
                
            G = generate_directed_graph(num_vertices)
            source = source_entry.get().strip().upper()
            target = target_entry.get().strip().upper()
            
            if source not in G.nodes or target not in G.nodes:
                result_label.config(
                    text="Sommets invalides. Utilisez le format 'A', 'B', etc.",
                    fg="#FF5252"
                )
                return
            
            path, distance = bellman_ford_graph(G, source, target)
            end_time = time.time()
            
            if path:
                display_graph(
                    fig, G, path,
                    f"Plus Court Chemin de {source} vers {target}"
                )
                canvas.draw()
                result_label.config(
                    text=f"Distance de {source} à {target}: {distance} | Temps d'exécution: {end_time - start_time:.4f} secondes",
                    fg="#4CAF50"
                )
            else:
                display_graph(fig, G, title=f"Aucun chemin trouvé de {source} vers {target}")
                canvas.draw()
                result_label.config(
                    text=f"Aucun chemin n'existe de {source} vers {target} | Temps d'exécution: {end_time - start_time:.4f} secondes",
                    fg="#FF5252"
                )
                
        except ValueError:
            result_label.config(
                text="Veuillez entrer des valeurs numériques valides",
                fg="#FF5252"
            )
    
    # Generate button
    generate_btn = ttk.Button(
        container,
        text="Générer le Graphe",
        style="Custom.TButton",
        command=generate_graph
    )
    generate_btn.pack(pady=10)
    
    # Close button
    close_btn = ttk.Button(
        container,
        text="Fermer",
        style="Custom.TButton",
        command=window.destroy
    )
    close_btn.pack(pady=10)
    
    # Initial display
    display_graph(fig, generate_directed_graph(5))
    canvas.draw()
    
    window.mainloop()