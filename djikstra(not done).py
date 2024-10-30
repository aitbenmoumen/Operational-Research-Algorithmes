# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 17:03:28 2024

@author: aaitb
"""

import networkx as nx
import matplotlib.pyplot as plt 
import random
import string

def generate_labels():
    alphabet = string.ascii_lowercase
    i = 0
    while True:
        label = ""
        n = i
        while True:
            label = alphabet[n % 26] + label
            n = n // 26 - 1
            if n < 0:
                break
        yield label
        i += 1
        
def generate_random_graph(num_nodes, probability):
    G = nx.erdos_renyi_graph(num_nodes, probability)
    for (u, v) in G.edges():
        G[u][v]['weight'] = random.randint(1, 10)
    
    label_gen = generate_labels()
    labels = {node: next(label_gen) for node in G.nodes()}
    nx.set_node_attributes(G, labels, "label")
    return G

def display_graph(G, title="Graph"):
    pos = nx.spring_layout(G)
    labels = nx.get_node_attributes(G, "label")
    edge_labels = nx.get_edge_attributes(G, "weight")
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, labels=labels, with_labels=True, node_color='skyblue', edge_color='gray', node_size=700, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.show()

num_nodes = random.randint(5, 15)  
edge_probability = random.uniform(0.3, 0.7)  

G = generate_random_graph(num_nodes, edge_probability)
display_graph(G, "Original Random Graph with Weights")









