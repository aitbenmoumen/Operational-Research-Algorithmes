import tkinter as tk
from tkinter import ttk
from Ford_Fulkerson import display_ford_fulkerson_graph
from welsh_powel import display_welsh_powell_graph
from Kruskal import display_kruskal_graph
from Dijkstra import display_dijkstra_graph
from Bellman_ford import display_bellman_ford_graph
from NW_MC_SS import create_transportation_gui
from pert_gui import create_pert_gui

def guiMenu():
    gui = tk.Tk()
    gui.title("Les Algorithmes")
    gui.configure(bg="#303030")
    gui.geometry("900x700")  # Increased size for better layout
    gui.resizable(False, False)

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure button style
    style.configure(
        "Algorithm.TButton",
        background="#3F51B5",
        foreground="white",
        font=("Calibri", 12, "bold"),
        padding=(20, 15),
        borderwidth=0,
        borderradius=20,
    )
    
    style.map(
        "Algorithm.TButton",
        background=[("active", "#5C6BC0")],
        foreground=[("active", "white")],
    )

    # Main container
    container = tk.Frame(gui, bg="#303030")
    container.pack(expand=True, fill="both", padx=40, pady=40)

    # Title section
    title_frame = tk.Frame(container, bg="#303030")
    title_frame.pack(fill="x", pady=(0, 30))

    title_label = tk.Label(
        title_frame,
        text="Algorithmes de Recherche Opérationnelle",
        font=("Calibri", 28, "bold"),
        bg="#303030",
        fg="#F0F8FF",
    )
    title_label.pack(pady=(0, 10))

    subtitle_label = tk.Label(
        title_frame,
        text="Sélectionnez un algorithme à exécuter",
        font=("Calibri", 14),
        bg="#303030",
        fg="#AAAAAA",
    )
    subtitle_label.pack()

    # Separator
    separator = ttk.Separator(container, orient="horizontal")
    separator.pack(fill="x", pady=(0, 30))

    # Buttons container
    button_frame = tk.Frame(container, bg="#303030")
    button_frame.pack(pady=20)

    # Create buttons with consistent styling
    algorithms = [
        ("Welsh Powell", display_welsh_powell_graph),
        ("Kruskal", display_kruskal_graph),
        ("Dijkstra", display_dijkstra_graph),
        ("Bellman Ford", display_bellman_ford_graph),
        ("Ford Fulkerson", display_ford_fulkerson_graph),
        ("Stepping Stone", create_transportation_gui),
        ("Potentiel Métra (PERT)", create_pert_gui)
    ]

    # Create grid layout
    for idx, (text, command) in enumerate(algorithms):
        row = idx // 2
        col = idx % 2
        button = ttk.Button(
            button_frame,
            text=text,
            command=command,
            style="Algorithm.TButton",
            width=25
        )
        button.grid(row=row, column=col, padx=20, pady=15)

    # Add close button at the bottom
    close_frame = tk.Frame(container, bg="#303030")
    close_frame.pack(side="bottom", pady=30)

    close_button = ttk.Button(
        close_frame,
        text="Fermer",
        style="Algorithm.TButton",
        command=gui.destroy,
        width=20
    )
    close_button.pack()

    # Version label
    version_label = tk.Label(
        container,
        text="Version 1.0",
        font=("Calibri", 10),
        bg="#303030",
        fg="#666666"
    )
    version_label.pack(side="bottom", pady=10)

    # Center window on screen
    window_width = 900
    window_height = 700
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    gui.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    gui.mainloop()