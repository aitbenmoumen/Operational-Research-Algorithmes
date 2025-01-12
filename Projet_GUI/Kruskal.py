import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import string
import time

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

def generer_graphe(nb_sommets):
    sommets = generer_etiquettes_sommets(nb_sommets)
    aretes = []
    for i in range(nb_sommets):
        for j in range(i + 1, nb_sommets):
            poids = random.randint(1, 1000)
            aretes.append((sommets[i], sommets[j], poids))
    return sommets, aretes

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

def visualiser_graphe(fig, sommets, aretes, acm=None, titre="Graphe"):
    G = nx.Graph()
    for sommet_u, sommet_v, poids in aretes:
        G.add_edge(sommet_u, sommet_v, weight=poids)

    pos = nx.spring_layout(G, seed=42)

    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_facecolor('#303030')
    fig.patch.set_facecolor('#303030')

    nx.draw(
        G, pos,
        with_labels=True,
        node_color='#4CAF50',
        node_size=500,
        font_size=10,
        font_weight='bold',
        font_color='white',
        edge_color='#666666',
        ax=ax
    )
    
    edge_labels = {(u, v): f'{poids}' for u, v, poids in aretes}
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=8,
        font_color='white',
        ax=ax
    )
    
    if acm:
        acm_edges = [(u, v) for u, v, _ in acm]
        nx.draw_networkx_edges(
            G, pos,
            edgelist=acm_edges,
            width=3,
            edge_color='#3F51B5',
            ax=ax
        )
    
    ax.set_title(titre, color='white', pad=20, fontsize=14)
    fig.tight_layout()

def display_kruskal_graph():
    window = tk.Toplevel()
    window.title("Algorithme de Kruskal - Arbre Couvrant Minimal")
    window.geometry("1000x800")
    window.configure(bg="#303030")
    
    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure(
        "Custom.TButton",
        background="#3F51B5",
        foreground="white",
        font=("Calibri", 12, "bold"),
        padding=(20, 10),
        borderwidth=0,
        borderradius=20,
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
        text="Algorithme de Kruskal",
        font=("Calibri", 24, "bold"),
        bg="#303030",
        fg="#F0F8FF",
    )
    title_label.pack(pady=(0, 5))
    
    subtitle_label = tk.Label(
        title_frame,
        text="Arbre Couvrant Minimal",
        font=("Calibri", 14),
        bg="#303030",
        fg="#AAAAAA",
    )
    subtitle_label.pack()
    
    # Separator
    separator = ttk.Separator(container, orient="horizontal")
    separator.pack(fill="x", pady=(0, 20))
    
    # Input section
    input_frame = tk.Frame(container, bg="#303030")
    input_frame.pack(fill="x", pady=10)
    
    tk.Label(
        input_frame,
        text="Nombre de Sommets:",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF"
    ).pack(side="left", padx=10)
    
    num_vertices_entry = tk.Entry(
        input_frame,
        font=("Calibri", 12),
        bg="#404040",
        fg="#F0F8FF",
        insertbackground="#F0F8FF",
        relief="flat",
        width=10
    )
    num_vertices_entry.pack(side="left", padx=10)
    
    def generate_graph():
        try:
            num_vertices = int(num_vertices_entry.get())
            if num_vertices <= 0:
                raise ValueError("Le nombre de sommets doit être positif")
                
            sommets, aretes = generer_graphe(num_vertices)
            
            start_time = time.time()
            acm, cout_total = kruskal(sommets, aretes)
            end_time = time.time()
            
            visualiser_graphe(
                fig,
                sommets,
                aretes,
                acm=acm,
                titre=f"Arbre Couvrant Minimal (Coût: {cout_total})"
            )
            canvas.draw()
            
            execution_time = end_time - start_time
            result_label.config(
                text=f"Coût Total: {cout_total} | Temps d'Exécution: {execution_time:.4f} secondes",
                fg="#4CAF50"
            )
        except ValueError as e:
            result_label.config(
                text="Erreur: Veuillez entrer un nombre entier positif",
                fg="#FF5252"
            )
    
    # Button frame
    button_frame = tk.Frame(container, bg="#303030")
    button_frame.pack(fill="x", pady=10)
    
    generate_btn = ttk.Button(
        button_frame,
        text="Générer le Graphe",
        style="Custom.TButton",
        command=generate_graph
    )
    generate_btn.pack(pady=10)
    
    # Result label
    result_label = tk.Label(
        container,
        text="",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF",
        wraplength=900
    )
    result_label.pack(pady=10)
    
    # Graph frame
    graph_frame = tk.Frame(container, bg="#303030")
    graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Initialize figure and canvas
    fig = plt.Figure(figsize=(10, 8))
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Bottom section
    bottom_frame = tk.Frame(container, bg="#303030")
    bottom_frame.pack(fill="x", pady=20)
    
    close_btn = ttk.Button(
        bottom_frame,
        text="Fermer",
        style="Custom.TButton",
        command=window.destroy
    )
    close_btn.pack(pady=5)
    
    # Version label
    version_label = tk.Label(
        container,
        text="Version 1.0",
        font=("Calibri", 10),
        bg="#303030",
        fg="#666666"
    )
    version_label.pack(side="bottom", pady=5)
    
    # Center window
    window_width = 1000
    window_height = 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")