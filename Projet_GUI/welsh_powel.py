import networkx as nx
import matplotlib.pyplot as plt
import random
import time

def generer_graphe_aleatoire(n, p):
    orienté = random.choice([True, False])
    if orienté:
        G = nx.gnp_random_graph(n, p, directed=True)
    else:
        G = nx.gnp_random_graph(n, p, directed=False)
    return G, orienté

def coloration_welsh_powell(G):
    # Appliquer l'algorithme Welsh-Powell pour la coloration
    colors = nx.coloring.greedy_color(G, strategy="largest_first")
    return colors

def afficher_graphe(G, couleurs_noeuds=None, titre="Graphe", orienté=False):
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G)

    if couleurs_noeuds is not None:
        node_colors = [couleurs_noeuds[n] for n in G.nodes()]
        nx.draw(
            G, pos, node_color=node_colors, with_labels=True,
            node_size=500, cmap=plt.cm.rainbow, arrows=orienté
        )
    else:
        nx.draw(G, pos, node_color='blue', with_labels=True, node_size=500)

    plt.title(titre)
    plt.show()

# Mesure du temps d'exécution total
start_time = time.time()

# Demande à l'utilisateur d'entrer le nombre de sommets
n = int(input("Entrez le nombre de sommets (n): "))

# La probabilité qu'un sommet soit lié à un autre
p = float(input("Entrez la probabilité d'arête (p, entre 0 et 1): "))

# Génération du graphe aléatoire
G, orienté = generer_graphe_aleatoire(n, p)

# Application de la coloration Welsh-Powell
couleurs_noeuds_après = coloration_welsh_powell(G)
min_couleur_après = max(couleurs_noeuds_après.values()) + 1  # Nombre de couleurs utilisées

# Affichage du graphe avec les couleurs attribuées
afficher_graphe(G, couleurs_noeuds=couleurs_noeuds_après, 
                titre='Graphe après Welsh-Powell', orienté=orienté)

# Résultats de coloration
print(f"Nombre minimum de couleurs (après Welsh-Powell) : {min_couleur_après}")
print(f"Formule selon Welsh-Powell : {min_couleur_après} <= Xi(G) <= {n}")

# Temps d'exécution total
end_time = time.time()
execution_time = end_time - start_time
print(f"Temps d'exécution total : {execution_time:.4f} secondes")
