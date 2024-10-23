# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 23:48:38 2024

@author: aaitb
"""
import networkx as nx
import matplotlib as plt 

G = nx.Graph()

G.add_node("A")
G.add_node("B")
G.add_node("C")
G.add_node("D")
G.add_node("E")
G.add_node("F")

G.add_edge("A","C")
G.add_edge("A","D")
G.add_edge("B","D")
G.add_edge("A","C")
G.add_edge("A","F")
G.add_edge("F","E")
G.add_edge("E","C")

nx.draw(G,with_labels="true",node_color="green",node_size=500)
plt.margins(0.5)
plt.show()

