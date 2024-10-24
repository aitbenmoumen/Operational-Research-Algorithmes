# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:42:22 2024

@author: aaitb
"""
import networkx as nx
import random
import matplotlib.pyplot as plt


def increment_letter(letter):
    # Check if the letter is lowercase
    if 'a' <= letter <= 'z':
        # Increment and wrap around using modulo
        return chr((ord(letter) - ord('a') + 1) % 26 + ord('a'))
    # Check if the letter is uppercase
    elif 'A' <= letter <= 'Z':
        return chr((ord(letter) - ord('A') + 1) % 26 + ord('A'))
    else:
        return letter  # Return the letter unchanged if it's not a valid alphabet

nodes = int(input("Saisir le nombre de sommets :"))
G = nx.Graph()
letter = 'A'

for _ in range(nodes):
    G.add_node(letter)
    letter = increment_letter(letter)
    
# Generate random edges
num_edges = random.randint(nodes - 1, nodes * (nodes - 1) // 2)  # Random number of edges
edges = set()  # Use a set to avoid duplicate edges

while len(edges) < num_edges:
    node_a = random.choice(list(G.nodes()))
    node_b = random.choice(list(G.nodes()))
    
    # Ensure that the nodes are not the same
    if node_a != node_b:
        price = random.randint(0, 100)
        edges.add((node_a, node_b, price))

# Add edges to the graph with random prices
for node_a, node_b, price in edges:
    G.add_edge(node_a, node_b, weight=price)

pos = nx.spring_layout(G)  # Positioning for nodes
nx.draw(G,with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()
    