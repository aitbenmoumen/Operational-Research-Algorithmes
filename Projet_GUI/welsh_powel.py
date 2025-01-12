import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display_welsh_powell_graph():
    # Create a new window
    window = tk.Toplevel()
    window.title("Welsh-Powell Algorithm - Graph Coloring")
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
        text="Algorithme de Welsh-Powell",
        font=("Calibri", 24, "bold"),
        bg="#303030",
        fg="#F0F8FF",
    )
    title_label.pack(pady=(0, 5))
    
    subtitle_label = tk.Label(
        title_frame,
        text="Coloration de Graphe",
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
    
    num_nodes_entry = tk.Entry(
        input_frame,
        font=("Calibri", 12),
        bg="#404040",
        fg="#F0F8FF",
        insertbackground="#F0F8FF",  # Cursor color
        relief="flat",
        width=10
    )
    num_nodes_entry.pack(side="left", padx=10)
    
    def generate_graph():
        nonlocal canvas
        try:
            # Get input value
            num_nodes = int(num_nodes_entry.get())
            
            if num_nodes <= 0:
                raise ValueError("Number of vertices must be positive")
            
            # Generate random graph
            G = nx.gnp_random_graph(num_nodes, 0.5, directed=False)
            
            # Apply Welsh-Powell algorithm
            colors = nx.coloring.greedy_color(G, strategy="largest_first")
            min_colors = max(colors.values()) + 1
            
            # Create figure with dark theme
            plt.style.use('dark_background')
            fig, ax = plt.subplots(figsize=(10, 8))
            fig.patch.set_facecolor('#303030')
            ax.set_facecolor('#303030')
            
            # Draw graph
            pos = nx.spring_layout(G)
            nx.draw(
                G, pos,
                node_color=[colors[node] for node in G.nodes()],
                with_labels=True,
                node_size=500,
                cmap=plt.cm.rainbow,
                ax=ax,
                font_size=10,
                font_weight='bold',
                edge_color='#666666'
            )
            ax.set_title(
                f"Résultat de l'Algorithme Welsh-Powell\nNombre Minimal de Couleurs: {min_colors}",
                color='white',
                pad=20,
                fontsize=14
            )
            
            # Update canvas
            if canvas:
                canvas.get_tk_widget().destroy()
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Update result label
            result_label.config(
                text=f"Nombre Minimal de Couleurs Utilisées: {min_colors}",
                fg="#4CAF50"  # Success color
            )
            
        except ValueError as e:
            result_label.config(
                text="Erreur: Veuillez entrer un nombre entier positif",
                fg="#FF5252"  # Error color
            )
    
    # Button frame
    button_frame = tk.Frame(container, bg="#303030")
    button_frame.pack(fill="x", pady=10)
    
    submit_btn = ttk.Button(
        button_frame,
        text="Générer le Graphe",
        style="Custom.TButton",
        command=generate_graph
    )
    submit_btn.pack(pady=10)
    
    # Result label
    result_label = tk.Label(
        container,
        text="",
        font=("Calibri", 12),
        bg="#303030",
        fg="#F0F8FF"
    )
    result_label.pack(pady=10)
    
    # Graph frame
    graph_frame = tk.Frame(container, bg="#303030")
    graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Initialize canvas
    canvas = None
    
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
    
    
