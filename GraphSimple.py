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

# To fix the position in order to have the same graph each time 
pos = {
       "A":(1,2),
       "B":(3,4),
       "C":(1,6),
       "D":(2,4.5),
       "E":(2,1),
       "F":(3,5)
       }

# Pass everything you need about drawing as a parametre in nx.draw()

nx.draw(G,pos=pos,with_labels="true",node_color="green",node_size=500)
plt.margins(0.5)
plt.show()

