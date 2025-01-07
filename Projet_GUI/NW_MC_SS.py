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
        frame = ttk.LabelFrame(parent, text=title)
        frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        table = ttk.Treeview(frame, columns=[f"C{i+1}" for i in range(cols)], show='headings', height=rows)
        for i in range(cols):
            table.heading(f"C{i+1}", text=f"C{i+1}")
            table.column(f"C{i+1}", width=50, anchor='center')
        
        table.pack(fill='both', expand=True, padx=5, pady=5)
        return table

    def update_table(table, data, total_cost):
        # Clear existing items
        for item in table.get_children():
            table.delete(item)
            
        # Insert new data
        for i, row in enumerate(data):
            table.insert('', 'end', values=[str(x) for x in row], text=f"S{i+1}")
            
        # Add total cost row
        table.insert('', 'end', values=[''] * len(data[0]))
        table.insert('', 'end', values=[f"Total Cost: {total_cost}"] + [''] * (len(data[0])-1))

    def solve_transportation_problem():
        try:
            rows = int(suppliers_entry.get())
            cols = int(consumers_entry.get())
            supply = list(map(int, supply_entry.get().split()))
            demand = list(map(int, demand_entry.get().split()))

            if len(supply) != rows or len(demand) != cols:
                result_label.config(text="Supply/Demand values do not match rows/columns.")
                return

            costs = generate_random_costs(rows, cols)
            
            # Update costs table
            update_table(costs_table, costs, None)
            
            # Northwest Corner Method
            nw_allocation = northwest_corner_method(supply.copy(), demand.copy(), costs)
            nw_total_cost = calculate_total_cost(nw_allocation, costs)
            update_table(nw_table, nw_allocation, nw_total_cost)
            
            # Least Cost Method
            lc_allocation = least_cost_method(supply.copy(), demand.copy(), costs)
            lc_total_cost = calculate_total_cost(lc_allocation, costs)
            update_table(lc_table, lc_allocation, lc_total_cost)
            
            # Stepping Stone Method
            optimized_allocation = stepping_stone_method(nw_allocation, costs)
            optimized_total_cost = calculate_total_cost(optimized_allocation, costs)
            update_table(ss_table, optimized_allocation, optimized_total_cost)

        except ValueError as e:
            result_label.config(text=f"Error: {e}")

    # Initialize GUI window
    window = tk.Tk()
    window.title("Transportation Problem Solver")
    window.geometry("1200x900")
    
    # Input frame
    input_frame = ttk.Frame(window)
    input_frame.pack(fill='x', padx=10, pady=5)
    
    # Left side inputs
    left_frame = ttk.Frame(input_frame)
    left_frame.pack(side='left', padx=5)
    
    ttk.Label(left_frame, text="Number of Suppliers:").pack()
    suppliers_entry = ttk.Entry(left_frame)
    suppliers_entry.pack()
    
    ttk.Label(left_frame, text="Supply Values:").pack()
    supply_entry = ttk.Entry(left_frame)
    supply_entry.pack()
    
    # Right side inputs
    right_frame = ttk.Frame(input_frame)
    right_frame.pack(side='left', padx=5)
    
    ttk.Label(right_frame, text="Number of Consumers:").pack()
    consumers_entry = ttk.Entry(right_frame)
    consumers_entry.pack()
    
    ttk.Label(right_frame, text="Demand Values:").pack()
    demand_entry = ttk.Entry(right_frame)
    demand_entry.pack()
    
    # Solve button
    ttk.Button(window, text="Solve", command=solve_transportation_problem).pack(pady=10)
    
    # Results frame
    results_frame = ttk.Frame(window)
    results_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Create tables for results
    costs_table = create_result_table(results_frame, 5, 5, "Cost Matrix")
    nw_table = create_result_table(results_frame, 5, 5, "Northwest Corner Method")
    lc_table = create_result_table(results_frame, 5, 5, "Least Cost Method")
    ss_table = create_result_table(results_frame, 5, 5, "Stepping Stone Method")
    
    # Error label
    result_label = ttk.Label(window, text="", foreground="red")
    result_label.pack(pady=5)
    
    close_btn = ttk.Button(window, text="Close", command=window.destroy)
    close_btn.pack(pady=10)
    
    window.mainloop()