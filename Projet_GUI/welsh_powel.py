import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def display_welsh_powell_graph():
    # Create a new window
    window = tk.Toplevel()
    window.title("Welsh-Powell Algorithm - Graph Coloring")
    window.geometry("800x600")
    
    # Function to generate and display the graph
    def generate_graph():
        nonlocal canvas
        try:
            # Get input value
            num_nodes = int(num_nodes_entry.get())
            
            # Generate random graph
            G = nx.gnp_random_graph(num_nodes, 0.5, directed=False)  # Edge probability fixed at 0.5
            
            # Apply Welsh-Powell algorithm
            colors = nx.coloring.greedy_color(G, strategy="largest_first")
            min_colors = max(colors.values()) + 1  # Number of colors used
            
            # Display the graph with node colors
            fig, ax = plt.subplots(figsize=(8, 6))
            pos = nx.spring_layout(G)
            nx.draw(
                G, pos, 
                node_color=[colors[node] for node in G.nodes()],
                with_labels=True, 
                node_size=500, 
                cmap=plt.cm.rainbow, 
                ax=ax
            )
            ax.set_title(f"Graph After Welsh-Powell (Min Colors: {min_colors})", fontsize=14)
            
            # Embed matplotlib figure in Tkinter window
            if canvas:
                canvas.get_tk_widget().destroy()  # Remove previous canvas
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

            # Display number of colors in the result label
            result_label.config(text=f"Minimum Colors Used: {min_colors}")
        except ValueError:
            result_label.config(text="Invalid input. Please enter a valid number.")
    
    # Input field for number of vertices
    tk.Label(window, text="Number of Vertices:").pack(pady=5)
    num_nodes_entry = tk.Entry(window)
    num_nodes_entry.pack(pady=5)

    # Submit button
    submit_btn = ttk.Button(window, text="Submit", command=generate_graph)
    submit_btn.pack(pady=10)

    # Label to display results
    result_label = tk.Label(window, text="", font=("Arial", 12))
    result_label.pack(pady=10)

    # Initialize canvas for graph visualization
    canvas = None

    # Close button
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)