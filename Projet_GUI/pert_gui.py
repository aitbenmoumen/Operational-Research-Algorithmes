import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def create_pert_gui():
    def generer_tableau_taches(nombre_taches):
        tableau = []
        for i in range(nombre_taches):
            duree = random.randint(1, 10)
            anteriorite = random.sample(range(1, nombre_taches + 1), random.randint(0, min(3, i)))
            anteriorite = [ant for ant in anteriorite if ant < i + 1]
            tableau.append({"id": i + 1, "duree": duree, "anteriorite": anteriorite})
        return tableau

    def potentiel_metra(taches):
        G = nx.DiGraph()
        for tache in taches:
            G.add_node(tache["id"], duree=tache["duree"])
            for ant in tache["anteriorite"]:
                G.add_edge(ant, tache["id"])
        G.add_node(0, duree=0)
        G.add_node(len(taches) + 1, duree=0)
        for tache in taches:
            if not list(G.predecessors(tache["id"])):
                G.add_edge(0, tache["id"])
            if not list(G.successors(tache["id"])):
                G.add_edge(tache["id"], len(taches) + 1)
        dates_tot = {}
        for node in nx.topological_sort(G):
            if node == 0:
                dates_tot[node] = 0
            else:
                pred_dates = [dates_tot[pred] + G.nodes[pred]['duree'] for pred in G.predecessors(node)]
                dates_tot[node] = max(pred_dates) if pred_dates else 0
        dates_tard = {}
        duree_totale = dates_tot[len(taches) + 1]
        for node in reversed(list(nx.topological_sort(G))):
            if node == len(taches) + 1:
                dates_tard[node] = duree_totale
            else:
                succ_dates = [dates_tard[succ] - G.nodes[node]['duree'] for succ in G.successors(node)]
                dates_tard[node] = min(succ_dates) if succ_dates else duree_totale
        marges = {n: dates_tard[n] - dates_tot[n] for n in G.nodes()}
        chemin_critique = [n for n in G.nodes() if marges[n] == 0]
        return G, dates_tot, dates_tard, marges, chemin_critique

    def afficher_diagramme(G, chemin_critique):
        fig.clear()
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
        nx.draw_networkx_nodes(G, pos, nodelist=chemin_critique, node_color='red', node_size=500)
        nx.draw_networkx_edges(G, pos, edge_color="gray")
        plt.title("Diagramme Potentiel Métra")
        canvas.draw()

    def execute_pert():
        try:
            # Get user input for the number of tasks
            nombre_taches = int(nombre_taches_entry.get())
            taches = generer_tableau_taches(nombre_taches)
            
            # Perform the Potentiel Métra calculations
            G, dates_tot, dates_tard, marges, chemin_critique = potentiel_metra(taches)
            
            # Update the results in the GUI
            resultat_taches.delete(1.0, tk.END)
            resultat_taches.insert(tk.END, "Tâches Générées:\n")
            for t in taches:
                resultat_taches.insert(tk.END, f"ID: {t['id']}, Durée: {t['duree']}, Antériorité: {t['anteriorite']}\n")
            
            resultat_details.delete(1.0, tk.END)
            resultat_details.insert(tk.END, "Détails (Dates & Marges):\n")
            for node in sorted(G.nodes()):
                if node != 0 and node != len(taches) + 1:
                    resultat_details.insert(tk.END, f"ID: {node}, Tôt: {dates_tot[node]}, Tard: {dates_tard[node]}, Marge: {marges[node]}\n")
            
            duree_totale.set(f"Durée Totale du Projet : {dates_tot[len(taches) + 1]}")
            chemin_critique_str.set(f"Chemin Critique : {' -> '.join(map(str, chemin_critique))}")
            
            # Display the diagram
            afficher_diagramme(G, chemin_critique)
        except Exception as e:
            duree_totale.set(f"Erreur : {e}")

    # Create a new Toplevel window for the Potentiel Métra GUI
    pert_window = tk.Toplevel()
    pert_window.title("Potentiel Métra (PERT)")
    pert_window.geometry("1200x800")

    # Input section for number of tasks
    tk.Label(pert_window, text="Nombre de Tâches :").pack(pady=5)
    nombre_taches_entry = tk.Entry(pert_window)
    nombre_taches_entry.pack(pady=5)

    pert_button = ttk.Button(pert_window, text="Exécuter Potentiel Métra", command=execute_pert)
    pert_button.pack(pady=10)

    # Display generated tasks
    resultat_taches = tk.Text(pert_window, height=10, width=80)
    resultat_taches.pack(pady=10)

    # Display computation details (dates and margins)
    resultat_details = tk.Text(pert_window, height=10, width=80)
    resultat_details.pack(pady=10)

    # Labels for duration and critical path
    duree_totale = tk.StringVar()
    chemin_critique_str = tk.StringVar()
    tk.Label(pert_window, textvariable=duree_totale, font=("Helvetica", 12, "bold")).pack(pady=5)
    tk.Label(pert_window, textvariable=chemin_critique_str, font=("Helvetica", 12, "bold")).pack(pady=5)

    # Canvas for the graph diagram
    fig = plt.Figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=pert_window)
    canvas.get_tk_widget().pack(pady=10)