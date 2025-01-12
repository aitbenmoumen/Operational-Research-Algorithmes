import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from datetime import datetime

class ModernDarkTheme:
    # Colors
    BG_COLOR = "#1e1e1e"  # Dark background
    SECONDARY_BG = "#252526"  # Slightly lighter background
    TEXT_COLOR = "#ffffff"  # White text
    SECONDARY_TEXT = "#cccccc"  # Slightly dimmed text
    ACCENT_COLOR = "#007acc"  # Blue accent
    ACCENT_HOVER = "#0098ff"  # Lighter blue for hover
    ERROR_COLOR = "#f44336"  # Error red
    SUCCESS_COLOR = "#4caf50"  # Success green
    
    # Fonts
    MAIN_FONT = ("Segoe UI", 12)
    TITLE_FONT = ("Segoe UI", 24, "bold")
    SUBTITLE_FONT = ("Segoe UI", 14)

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
        
        dates_tot = {0: 0}
        for node in nx.topological_sort(G):
            if node not in dates_tot:
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
        # Clear the previous figure
        plt.close('all')
        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        
        # Configure plot style
        canvas.figure.patch.set_facecolor(ModernDarkTheme.BG_COLOR)
        ax.set_facecolor(ModernDarkTheme.SECONDARY_BG)
        
        pos = nx.spring_layout(G)
        
        # Draw regular nodes
        nx.draw_networkx_nodes(G, pos,
                             ax=ax,
                             node_color=ModernDarkTheme.SECONDARY_BG,
                             node_size=700,
                             edgecolors=ModernDarkTheme.TEXT_COLOR)
        
        # Draw critical path nodes
        nx.draw_networkx_nodes(G, pos,
                             ax=ax,
                             nodelist=chemin_critique,
                             node_color=ModernDarkTheme.ACCENT_COLOR,
                             node_size=700,
                             edgecolors=ModernDarkTheme.TEXT_COLOR)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos,
                             ax=ax,
                             edge_color=ModernDarkTheme.SECONDARY_TEXT,
                             arrows=True,
                             arrowsize=20)
        
        # Add labels
        nx.draw_networkx_labels(G, pos,
                              ax=ax,
                              font_size=10,
                              font_weight='bold',
                              font_color=ModernDarkTheme.TEXT_COLOR)
        
        ax.set_title("Diagramme PERT",
                    color=ModernDarkTheme.TEXT_COLOR,
                    pad=20,
                    fontsize=14)
        
        # Remove axes
        ax.set_axis_off()
        
        # Update the canvas
        canvas.draw()

    def execute_pert():
        try:
            nombre_taches = int(nombre_taches_entry.get())
            if nombre_taches <= 0:
                raise ValueError("Le nombre de tâches doit être positif")
            
            # Clear previous results
            resultat_text.delete(1.0, tk.END)
            
            taches = generer_tableau_taches(nombre_taches)
            G, dates_tot, dates_tard, marges, chemin_critique = potentiel_metra(taches)
            
            # Update results
            current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            resultat_text.insert(tk.END, f"Date et heure: {current_time}\n", "timestamp")
            resultat_text.insert(tk.END, f"Utilisateur: {user_login}\n\n", "timestamp")
            
            resultat_text.insert(tk.END, "Tâches générées:\n", "header")
            for t in taches:
                resultat_text.insert(tk.END, 
                    f"Tâche {t['id']}: Durée = {t['duree']}, Antériorités = {t['anteriorite']}\n", 
                    "content")
            
            # Update critical path label
            chemin_critique_label.config(
                text=f"Chemin critique: {' → '.join(map(str, chemin_critique))}",
                bg=ModernDarkTheme.SECONDARY_BG,
                fg=ModernDarkTheme.ACCENT_COLOR
            )
            
            # Update graph
            afficher_diagramme(G, chemin_critique)
            
            # Update status
            status_label.config(
                text="Calcul terminé avec succès", 
                fg=ModernDarkTheme.SUCCESS_COLOR
            )
            
        except ValueError as e:
            resultat_text.delete(1.0, tk.END)
            resultat_text.insert(tk.END, f"Erreur: {str(e)}", "error")
            status_label.config(
                text=f"Erreur: {str(e)}", 
                fg=ModernDarkTheme.ERROR_COLOR
            )
            chemin_critique_label.config(text="")

    # Create main window
    window = tk.Toplevel()
    window.title("Méthode PERT")
    window.configure(bg=ModernDarkTheme.BG_COLOR)
    window.geometry("1200x800")

    # User information
    user_login = "aitbenmoumen"

    # Title
    title_label = tk.Label(
        window,
        text="Méthode PERT",
        font=ModernDarkTheme.TITLE_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.TEXT_COLOR
    )
    title_label.pack(pady=20)

    # Input frame
    input_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    input_frame.pack(pady=10)

    tk.Label(
        input_frame,
        text="Nombre de tâches:",
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.TEXT_COLOR
    ).pack(side=tk.LEFT, padx=5)

    nombre_taches_entry = tk.Entry(
        input_frame,
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.SECONDARY_BG,
        fg=ModernDarkTheme.TEXT_COLOR,
        insertbackground=ModernDarkTheme.TEXT_COLOR
    )
    nombre_taches_entry.pack(side=tk.LEFT, padx=5)

    # Submit button
    style = ttk.Style()
    style.theme_use("clam")
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

    submit_button = ttk.Button(
        window,
        text="Générer et Calculer",
        style="Modern.TButton",
        command=execute_pert
    )
    submit_button.pack(pady=10)

    # Critical path label
    chemin_critique_label = tk.Label(
        window,
        text="",
        font=ModernDarkTheme.SUBTITLE_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.ACCENT_COLOR,
        wraplength=800
    )
    chemin_critique_label.pack(pady=10)

    # Results text
    resultat_text = tk.Text(
        window,
        height=10,
        width=70,
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.SECONDARY_BG,
        fg=ModernDarkTheme.TEXT_COLOR,
        padx=10,
        pady=10
    )
    resultat_text.pack(pady=10)

    # Configure text tags
    resultat_text.tag_configure("header", foreground=ModernDarkTheme.ACCENT_COLOR, font=ModernDarkTheme.SUBTITLE_FONT)
    resultat_text.tag_configure("content", foreground=ModernDarkTheme.TEXT_COLOR)
    resultat_text.tag_configure("error", foreground=ModernDarkTheme.ERROR_COLOR)
    resultat_text.tag_configure("timestamp", foreground=ModernDarkTheme.SECONDARY_TEXT)

    # Status label
    status_label = tk.Label(
        window,
        text="",
        font=ModernDarkTheme.MAIN_FONT,
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.TEXT_COLOR
    )
    status_label.pack(pady=5)

    # Graph canvas
    canvas = FigureCanvasTkAgg(plt.Figure(figsize=(8, 6)), master=window)
    canvas.get_tk_widget().pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    # Footer with timestamp
    footer_frame = tk.Frame(window, bg=ModernDarkTheme.BG_COLOR)
    footer_frame.pack(fill=tk.X, pady=5)

    tk.Label(
        footer_frame,
        text=f"Current User: {user_login} | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        font=("Segoe UI", 8),
        bg=ModernDarkTheme.BG_COLOR,
        fg=ModernDarkTheme.SECONDARY_TEXT
    ).pack(side=tk.RIGHT, padx=10)

    return window

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app_window = create_pert_gui()
    app_window.mainloop()