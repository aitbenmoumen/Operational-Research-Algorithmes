# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 17:50:46 2025

@author: aaitb
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class ModernDarkTheme:
    # Colors
    BG_COLOR = "#1e1e1e"
    SECONDARY_BG = "#252526"
    TEXT_COLOR = "#ffffff"
    SECONDARY_TEXT = "#cccccc"
    ACCENT_COLOR = "#007acc"
    ACCENT_HOVER = "#0098ff"
    ERROR_COLOR = "#f44336"
    SUCCESS_COLOR = "#4caf50"
    
    # Fonts
    MAIN_FONT = ("Segoe UI", 12)
    TITLE_FONT = ("Segoe UI", 24, "bold")
    SUBTITLE_FONT = ("Segoe UI", 14)

# Functions for Transportation Problem Algorithms
def generate_random_costs(rows, cols):
    return np.random.randint(1, 21, size=(rows, cols))

def northwest_corner_method(supply, demand, costs):
    supply = supply.copy()
    demand = demand.copy()
    rows, cols = costs.shape
    allocation = np.zeros((rows, cols), dtype=int)
    i, j = 0, 0
    
    while i < rows and j < cols:
        quantity = min(supply[i], demand[j])
        allocation[i, j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
        
        if supply[i] == 0:
            i += 1
        if demand[j] == 0:
            j += 1
            
    return allocation

def least_cost_method(supply, demand, costs):
    supply = supply.copy()
    demand = demand.copy()
    rows, cols = costs.shape
    allocation = np.zeros((rows, cols), dtype=int)
    
    while True:
        # Find cell with minimum cost where allocation is possible
        min_cost = float('inf')
        min_i = min_j = -1
        
        for i in range(rows):
            if supply[i] <= 0:
                continue
            for j in range(cols):
                if demand[j] <= 0:
                    continue
                if costs[i, j] < min_cost:
                    min_cost = costs[i, j]
                    min_i, min_j = i, j
        
        if min_i == -1 or min_j == -1:
            break
            
        # Allocate maximum possible quantity
        quantity = min(supply[min_i], demand[min_j])
        allocation[min_i, min_j] = quantity
        supply[min_i] -= quantity
        demand[min_j] -= quantity
    
    return allocation

def calculate_total_cost(allocation, costs):
    return int(np.sum(allocation * costs))

def stepping_stone_method(allocation, costs):
    rows, cols = costs.shape
    
    def find_loop(start_i, start_j):
        def find_path(current_i, current_j, path):
            if len(path) > 0 and (current_i, current_j) == path[0]:
                return path if len(path) >= 4 else None
            
            for next_i in range(rows):
                if next_i != current_i and (allocation[next_i, current_j] > 0 or (next_i, current_j) == (start_i, start_j)):
                    new_path = path + [(next_i, current_j)]
                    result = find_path(next_i, current_j, new_path)
                    if result:
                        return result
            
            for next_j in range(cols):
                if next_j != current_j and (allocation[current_i, next_j] > 0 or (current_i, next_j) == (start_i, start_j)):
                    new_path = path + [(current_i, next_j)]
                    result = find_path(current_i, next_j, new_path)
                    if result:
                        return result
            
            return None
        
        for i in range(rows):
            for j in range(cols):
                if allocation[i, j] > 0:
                    path = find_path(i, j, [(i, j)])
                    if path:
                        return path
        return None
    
    while True:
        improvement = False
        min_cost_diff = float('inf')
        best_loop = None
        
        # Find entering variable
        for i in range(rows):
            for j in range(cols):
                if allocation[i, j] == 0:
                    loop = find_loop(i, j)
                    if loop:
                        # Calculate cost difference
                        cost_diff = 0
                        for idx, (loop_i, loop_j) in enumerate(loop):
                            cost_diff += costs[loop_i, loop_j] * (-1 if idx % 2 else 1)
                        
                        if cost_diff < min_cost_diff:
                            min_cost_diff = cost_diff
                            best_loop = loop
        
        if min_cost_diff >= 0 or not best_loop:
            break
            
        # Find minimum allocation in negative positions
        min_allocation = float('inf')
        for idx, (i, j) in enumerate(best_loop):
            if idx % 2:  # Negative position
                min_allocation = min(min_allocation, allocation[i, j])
        
        # Update allocations
        for idx, (i, j) in enumerate(best_loop):
            allocation[i, j] += min_allocation * (-1 if idx % 2 else 1)
        
        improvement = True
        
        if not improvement:
            break
    
    return allocation


# GUI Application
def create_transportation_gui():
    def create_result_table(parent, rows, cols, title):
        frame = ttk.LabelFrame(parent, text=title, style='Modern.TLabelframe')
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Configure style for the table
        style = ttk.Style()
        style.configure("Modern.Treeview",
                       background=ModernDarkTheme.SECONDARY_BG,
                       foreground=ModernDarkTheme.TEXT_COLOR,
                       fieldbackground=ModernDarkTheme.SECONDARY_BG,
                       font=ModernDarkTheme.MAIN_FONT)
        
        style.configure("Modern.Treeview.Heading",
                       background=ModernDarkTheme.BG_COLOR,
                       foreground=ModernDarkTheme.TEXT_COLOR,
                       font=ModernDarkTheme.MAIN_FONT)
        
        table = ttk.Treeview(frame, 
                            columns=[f"C{i+1}" for i in range(cols)],
                            show='headings',
                            height=rows,
                            style="Modern.Treeview")
        
        for i in range(cols):
            table.heading(f"C{i+1}", text=f"C{i+1}")
            table.column(f"C{i+1}", width=50, anchor='center')
        
        # Configure colors
        table.tag_configure('oddrow', background=ModernDarkTheme.BG_COLOR)
        table.tag_configure('evenrow', background=ModernDarkTheme.SECONDARY_BG)
        table.tag_configure('total', foreground=ModernDarkTheme.ACCENT_COLOR)
        
        table.pack(fill='both', expand=True, padx=5, pady=5)
        return table

    def update_table(table, data, total_cost):
        # Clear existing items
        for item in table.get_children():
            table.delete(item)
            
        # Insert new data with alternating row colors
        for i, row in enumerate(data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            table.insert('', 'end', 
                        values=[str(x) for x in row],
                        text=f"S{i+1}",
                        tags=(tag,))
            
        # Add separator
        table.insert('', 'end', values=['─' * 5] * len(data[0]), tags=('separator',))
        
        # Add total cost row with timestamp
        if total_cost is not None:
            current_time = datetime.utcnow().strftime('%H:%M:%S')
            table.insert('', 'end',
                        values=[f"Total Cost: {total_cost}"] + [''] * (len(data[0])-1),
                        tags=('total',))
            table.insert('', 'end',
                        values=[f"Updated: {current_time}"] + [''] * (len(data[0])-1),
                        tags=('timestamp',))

    def solve_transportation_problem():
        try:
            # Clear previous results
            result_label.config(text="")
            
            # Get and validate input
            rows = int(suppliers_entry.get())
            cols = int(consumers_entry.get())
            supply = list(map(int, supply_entry.get().split()))
            demand = list(map(int, demand_entry.get().split()))

            if len(supply) != rows or len(demand) != cols:
                raise ValueError("Supply/Demand values do not match rows/columns.")

            # Generate costs and update tables
            costs = generate_random_costs(rows, cols)
            update_table(costs_table, costs, None)
            
            # Calculate and update methods
            nw_allocation = northwest_corner_method(supply.copy(), demand.copy(), costs)
            nw_total_cost = calculate_total_cost(nw_allocation, costs)
            update_table(nw_table, nw_allocation, nw_total_cost)
            
            lc_allocation = least_cost_method(supply.copy(), demand.copy(), costs)
            lc_total_cost = calculate_total_cost(lc_allocation, costs)
            update_table(lc_table, lc_allocation, lc_total_cost)
            
            optimized_allocation = stepping_stone_method(nw_allocation.copy(), costs)
            optimized_total_cost = calculate_total_cost(optimized_allocation, costs)
            update_table(ss_table, optimized_allocation, optimized_total_cost)
            
            # Update status
            status_label.config(
                text="Calculation completed successfully",
                foreground=ModernDarkTheme.SUCCESS_COLOR
            )

        except ValueError as e:
            result_label.config(
                text=f"Error: {str(e)}",
                foreground=ModernDarkTheme.ERROR_COLOR
            )

    # Initialize main window
    window = tk.Tk()
    window.title("Transportation Problem Solver")
    window.geometry("1200x900")
    window.configure(bg=ModernDarkTheme.BG_COLOR)

    # Configure styles
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configure modern button style
    style.configure(
        "Modern.TButton",
        background=ModernDarkTheme.ACCENT_COLOR,
        foreground=ModernDarkTheme.TEXT_COLOR,
        font=ModernDarkTheme.MAIN_FONT,
        padding=(20, 10)
    )
    style.map(
        "Modern.TButton",
        background=[("active", ModernDarkTheme.ACCENT_HOVER)]
    )
    
    # Configure modern label style
    style.configure(
        "Modern.TLabel",
        background=ModernDarkTheme.BG_COLOR,
        foreground=ModernDarkTheme.TEXT_COLOR,
        font=ModernDarkTheme.MAIN_FONT
    )

    # Title Section
    title_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    title_frame.pack(fill="x", pady=20)
    
    tk.Label(
        title_frame,
        text="Probleme de transportation",
        font=ModernDarkTheme.TITLE_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.TEXT_COLOR
    ).pack()

    # Input Section
    input_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    input_frame.pack(fill="x", padx=40, pady=20)

    # Left side inputs
    left_frame = tk.Frame(input_frame, bg=ModernDarkTheme.BG_COLOR)
    left_frame.pack(side='left', padx=20)
    
    def create_input_field(parent, label_text):
        tk.Label(
            parent,
            text=label_text,
            font=ModernDarkTheme.MAIN_FONT,
            bg=ModernDarkTheme.BG_COLOR,
            fg=ModernDarkTheme.TEXT_COLOR
        ).pack(pady=5)
        
        entry = tk.Entry(
            parent,
            font=ModernDarkTheme.MAIN_FONT,
            bg=ModernDarkTheme.SECONDARY_BG,
            fg=ModernDarkTheme.TEXT_COLOR,
            insertbackground=ModernDarkTheme.TEXT_COLOR
        )
        entry.pack(pady=5)
        return entry

    suppliers_entry = create_input_field(left_frame, "Nombre des Usines:")
    supply_entry = create_input_field(left_frame, "Supply Values:")

    # Right side inputs
    right_frame = tk.Frame(input_frame, bg=ModernDarkTheme.BG_COLOR)
    right_frame.pack(side='left', padx=20)
    
    consumers_entry = create_input_field(right_frame, "Nombre des magasins:")
    demand_entry = create_input_field(right_frame, "Demand Values:")

    # Buttons
    button_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    button_frame.pack(pady=10)
    
    solve_btn = ttk.Button(
        button_frame,
        text="Solve",
        style="Modern.TButton",
        command=solve_transportation_problem
    )
    solve_btn.pack(side='left', padx=5)
    
    close_btn = ttk.Button(
        button_frame,
        text="Close",
        style="Modern.TButton",
        command=window.destroy
    )
    close_btn.pack(side='left', padx=5)

    # Results Section
    results_frame = ttk.Frame(window, style='Modern.TFrame')
    results_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Create result tables
    costs_table = create_result_table(results_frame, 5, 5, "Cost Matrix")
    nw_table = create_result_table(results_frame, 5, 5, "Northwest Corner Method")
    lc_table = create_result_table(results_frame, 5, 5, "Least Cost Method")
    ss_table = create_result_table(results_frame, 5, 5, "Stepping Stone Method")

    # Status labels
    result_label = tk.Label(
        window,
        text="",
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.ERROR_COLOR
    )
    result_label.pack(pady=5)
    
    status_label = tk.Label(
        window,
        text="",
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.SUCCESS_COLOR
    )
    status_label.pack(pady=5)

    # Footer
    footer_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    footer_frame.pack(fill="x", pady=5)
    
    footer_text = f"Current User: aitbenmoumen | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    tk.Label(
        footer_frame,
        text=footer_text,
        font=("Segoe UI", 8),
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.SECONDARY_TEXT
    ).pack(side="right", padx=10)

    return window

if __name__ == "__main__":
    app_window = create_transportation_gui()
    app_window.mainloop()