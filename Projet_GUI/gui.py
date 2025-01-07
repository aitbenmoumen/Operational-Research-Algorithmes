import tkinter as tk
from Ford_Fulkerson import display_ford_fulkerson_graph
from welsh_powel import display_welsh_powell_graph
from Kruskal import  display_kruskal_graph
from Dijkstra import display_dijkstra_graph
from Bellman_ford import display_bellman_ford_graph
from NW_MC_SS import create_transportation_gui

from tkinter import ttk

# Main Tkinter GUI
gui = tk.Tk()
gui.title("Network Flow Algorithms")

# Unified button properties
button_width = 20
button_height = 2  # Used only for tk.Button, not ttk.Button

# Buttons with consistent size
Ford_Fulkerson = tk.Button(gui, text="Ford Fulkerson", command=display_ford_fulkerson_graph, width=button_width, height=button_height)
Welsh_powel = tk.Button(gui, text="Welsh Powel", command=display_welsh_powell_graph, width=button_width, height=button_height)
Kruskal = tk.Button(gui, text="Kruskal", command=display_kruskal_graph, width=button_width, height=button_height)
Bellman_ford = tk.Button(gui, text="Bellman Ford", command=display_bellman_ford_graph, width=button_width, height=button_height)
Dijkstra = tk.Button(gui, text="Dijkstra", command=display_dijkstra_graph, width=button_width, height=button_height)
NW_MC_SS = tk.Button(gui, text="Stepping stone", command=create_transportation_gui, width=button_width, height=button_height)


# Arrange buttons in a 2x3 grid layout
Ford_Fulkerson.grid(row=0, column=0, padx=10, pady=10)
Welsh_powel.grid(row=0, column=1, padx=10, pady=10)
Kruskal.grid(row=1, column=0, padx=10, pady=10)
Bellman_ford.grid(row=1, column=1, padx=10, pady=10)
Dijkstra.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
NW_MC_SS.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


# Close button using ttk (without height)
close_btn = ttk.Button(gui, text="Close", command=gui.destroy, width=button_width)
close_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

gui.mainloop()
