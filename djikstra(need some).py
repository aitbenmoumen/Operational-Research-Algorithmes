# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 10:57:40 2024

@author: aaitb
"""

#implementationn djikstra 

import networkx as nx
import matplotlib.pyplot as plt 
import random


nodes = int(input("saisir le nombre de sommet:"))
edges =random.uniform(0,1)
G = nx.erdos_renyi_graph(nodes, edges)
for (u, v) in G.edges():
    G[u][v]['weight'] = random.randint(1, 100)
        
pos = nx.spring_layout(G)  # Use a layout algorithm for better positioning

    # Get edge labels as a dictionary
edge_labels = dict(nx.get_edge_attributes(G, "weight"))

source=int(input("Type source:"))
target = int(input("Type destination:"))
path = nx.dijkstra_path(G, source, target)

path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
plt.figure(figsize=(8, 6))  # Adjust figure size for better readability
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500)

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)  # Adjust label properties
#djikstra edges
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

plt.margins(0.1)

plt.show()



