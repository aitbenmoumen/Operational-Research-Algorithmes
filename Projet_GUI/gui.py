import tkinter as tk
from tkinter import ttk
from Ford_Fulkerson import display_ford_fulkerson_graph
from welsh_powel import display_welsh_powell_graph
from Kruskal import display_kruskal_graph
from Dijkstra import display_dijkstra_graph
from Bellman_ford import display_bellman_ford_graph
from NW_MC_SS import create_transportation_gui
from pert_gui import create_pert_gui  # Import the new Potentiel Métra GUI function

# Main Tkinter GUI
gui = tk.Tk()
gui.title("Network Flow Algorithms")

button_width = 20
button_height = 2

# Buttons
Ford_Fulkerson = tk.Button(gui, text="Ford Fulkerson", command=display_ford_fulkerson_graph, width=button_width, height=button_height)
Welsh_powel = tk.Button(gui, text="Welsh Powel", command=display_welsh_powell_graph, width=button_width, height=button_height)
Kruskal = tk.Button(gui, text="Kruskal", command=display_kruskal_graph, width=button_width, height=button_height)
Bellman_ford = tk.Button(gui, text="Bellman Ford", command=display_bellman_ford_graph, width=button_width, height=button_height)
Dijkstra = tk.Button(gui, text="Dijkstra", command=display_dijkstra_graph, width=button_width, height=button_height)
NW_MC_SS = tk.Button(gui, text="Stepping Stone", command=create_transportation_gui, width=button_width, height=button_height)
Potentiel_Metra = tk.Button(gui, text="Potentiel Métra (PERT)", command=create_pert_gui, width=button_width, height=button_height)

# Grid layout
Ford_Fulkerson.grid(row=0, column=0, padx=10, pady=10)
Welsh_powel.grid(row=0, column=1, padx=10, pady=10)
Kruskal.grid(row=1, column=0, padx=10, pady=10)
Bellman_ford.grid(row=1, column=1, padx=10, pady=10)
Dijkstra.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
NW_MC_SS.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
Potentiel_Metra.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Close button
close_btn = ttk.Button(gui, text="Close", command=gui.destroy, width=button_width)
close_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

gui.mainloop()
